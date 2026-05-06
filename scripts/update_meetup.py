#!/usr/bin/env python3
"""
DMV Throwers — Update 3rd Sunday meetup dates and clear past meetup events.

Run this the Monday after each 3rd Sunday meetup to keep the site current:
  1. Update "NEXT MEET" top bar in index.html and events.html
  2. Remove past monthly meetup event cards from events.html
  3. Remove past monthly meetup entries from the JSON-LD in events.html
  4. Update sitemap.xml lastmod for index and events pages

Usage:
  python scripts/update_meetup.py
  python scripts/update_meetup.py --repo /path/to/repo
  python scripts/update_meetup.py --dry-run
"""

import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET


MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def third_sunday(year: int, month: int) -> date:
    """Return the 3rd Sunday of the given year/month."""
    d = date(year, month, 1)
    days_to_first_sunday = (6 - d.weekday()) % 7
    first_sunday = d + timedelta(days=days_to_first_sunday)
    return first_sunday + timedelta(weeks=2)


def upcoming_third_sundays(n: int = 12, today: date | None = None) -> list[date]:
    """Return the next *n* third Sundays on or after *today*."""
    if today is None:
        today = date.today()
    results: list[date] = []
    y, m = today.year, today.month
    while len(results) < n:
        ts = third_sunday(y, m)
        if ts >= today:
            results.append(ts)
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return results


def fmt_upper(d: date) -> str:
    """Return 'MONTH D, YYYY' with no leading zero, uppercased."""
    return d.strftime("%B %d, %Y").replace(" 0", " ").upper()


# ---------------------------------------------------------------------------
# index.html + events.html — top-bar banner
# ---------------------------------------------------------------------------

_TOPBAR_RE = re.compile(
    r"(NEXT MEET:\s*)"
    r"((?:JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|"
    r"OCTOBER|NOVEMBER|DECEMBER)\s+\d{1,2},\s*\d{4})",
    re.IGNORECASE,
)


def update_topbar(html_path: Path, next_date: date, dry_run: bool = False) -> bool:
    """Replace the date in the 'NEXT MEET: …' top-bar span."""
    text = html_path.read_text(encoding="utf-8")
    new_str = fmt_upper(next_date)

    if not _TOPBAR_RE.search(text):
        print(f"  [!] NEXT MEET pattern not found in {html_path.name}")
        return False

    new_text = _TOPBAR_RE.sub(r"\g<1>" + new_str, text)
    if new_text == text:
        print(f"  [=] {html_path.name}: top bar already shows {new_str}")
        return False

    if not dry_run:
        html_path.write_text(new_text, encoding="utf-8")
    print(f"  [ok] {html_path.name}: top bar -> {new_str}")
    return True


# ---------------------------------------------------------------------------
# events.html — remove past monthly meetup cards
# ---------------------------------------------------------------------------

# Matches exactly <div class="event-card"> (no extra classes).
# Event-card divs sit at 4-space indent; inner divs are 6+ spaces, so
# \n    </div> reliably marks only the outermost closing tag.
_MEETUP_CARD_RE = re.compile(
    r"\n    <div class=\"event-card\">\n(.*?)\n    </div>",
    re.DOTALL,
)


def _parse_card_date(card_body: str, today: date) -> date | None:
    """Extract the event date from a monthly meetup card body."""
    m = re.search(
        r'<div class="event-date">'
        r"((?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{1,2})</div>",
        card_body,
    )
    if not m:
        return None
    parts = m.group(1).split()
    try:
        month_num = MONTH_NAMES.index(parts[0]) + 1
        day = int(parts[1])
        # Cards don't carry a year; assume current year.
        # If that date would already be many months behind, it might be next year —
        # but since we remove past cards, only "recently past" dates matter.
        return date(today.year, month_num, day)
    except (ValueError, IndexError):
        return None


def remove_past_meetup_cards(events_path: Path, today: date | None = None, dry_run: bool = False) -> bool:
    """Remove monthly meetup cards whose dates precede *today*."""
    if today is None:
        today = date.today()

    text = events_path.read_text(encoding="utf-8")
    removed = 0

    def replacer(m: re.Match) -> str:
        nonlocal removed
        body = m.group(1)
        if "● MONTHLY MEETUP" not in body:
            return m.group(0)  # keep (shouldn't happen with this exact class)
        card_date = _parse_card_date(body, today)
        if card_date is not None and card_date < today:
            removed += 1
            return ""
        return m.group(0)

    new_text = _MEETUP_CARD_RE.sub(replacer, text)

    if removed == 0:
        print(f"  [=] {events_path.name}: no past meetup cards to remove")
        return False

    if not dry_run:
        events_path.write_text(new_text, encoding="utf-8")
    print(f"  [ok] {events_path.name}: removed {removed} past meetup card(s)")
    return True


# ---------------------------------------------------------------------------
# events.html — prune past monthly meetup entries from JSON-LD
# ---------------------------------------------------------------------------

_JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json">)\s*(.*?)\s*(</script>)',
    re.DOTALL,
)


def remove_past_meetup_jsonld(events_path: Path, today: date | None = None, dry_run: bool = False) -> bool:
    """
    Parse the JSON-LD array in events.html and drop Event entries whose
    name contains 'Monthly Meetup' and whose startDate is before *today*.
    """
    if today is None:
        today = date.today()

    text = events_path.read_text(encoding="utf-8")
    m = _JSONLD_RE.search(text)
    if not m:
        print(f"  [!] {events_path.name}: JSON-LD block not found")
        return False

    try:
        data = json.loads(m.group(2))
    except json.JSONDecodeError as exc:
        print(f"  [!] {events_path.name}: JSON-LD parse error - {exc}")
        return False

    if not isinstance(data, list):
        print(f"  [!] {events_path.name}: JSON-LD is not an array, skipping")
        return False

    before = len(data)
    filtered = []
    for entry in data:
        if entry.get("@type") == "Event" and "Monthly Meetup" in entry.get("name", ""):
            start_iso = entry.get("startDate", "")[:10]  # YYYY-MM-DD
            try:
                event_date = date.fromisoformat(start_iso)
            except ValueError:
                filtered.append(entry)
                continue
            if event_date < today:
                continue  # drop past entry
        filtered.append(entry)

    removed = before - len(filtered)
    if removed == 0:
        print(f"  [=] {events_path.name}: no past meetup JSON-LD entries to remove")
        return False

    new_json = json.dumps(filtered, indent=2, ensure_ascii=False)
    new_text = (
        text[: m.start()]
        + m.group(1) + "\n"
        + new_json + "\n"
        + m.group(3)
        + text[m.end() :]
    )

    if not dry_run:
        events_path.write_text(new_text, encoding="utf-8")
    print(f"  [ok] {events_path.name}: removed {removed} past meetup JSON-LD entry(ies)")
    return True


# ---------------------------------------------------------------------------
# sitemap.xml — bump lastmod for index/events URLs
# ---------------------------------------------------------------------------

def update_sitemap(sitemap_path: Path, dry_run: bool = False) -> bool:
    if not sitemap_path.exists():
        return False
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        today_str = date.today().isoformat()
        for url in root.findall("sm:url", ns):
            loc = url.find("sm:loc", ns)
            if loc is None:
                continue
            if any(tok in loc.text for tok in ("index", "events")):
                lastmod = url.find("sm:lastmod", ns)
                if lastmod is None:
                    lastmod = ET.SubElement(
                        url,
                        "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod",
                    )
                lastmod.text = today_str
        if not dry_run:
            tree.write(str(sitemap_path), encoding="unicode", xml_declaration=False)
        print(f"  [ok] sitemap.xml: lastmod updated to {today_str}")
        return True
    except Exception as exc:
        print(f"  [!] sitemap.xml update skipped: {exc}")
        return False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update DMV Throwers meetup dates and clear past events."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the repo root (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing any files",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    today = date.today()
    dates = upcoming_third_sundays(12, today)
    next_date = dates[0]

    print(f"Today       : {today.isoformat()}")
    print(f"Next meetup : {next_date.strftime('%A, %B %d, %Y').replace(' 0', ' ')}")
    if args.dry_run:
        print("(dry-run - no files will be modified)\n")

    index_html = repo / "index.html"
    events_html = repo / "events.html"

    print("\nindex.html:")
    if index_html.exists():
        update_topbar(index_html, next_date, args.dry_run)
    else:
        print("  [!] file not found")

    print("\nevents.html:")
    if events_html.exists():
        update_topbar(events_html, next_date, args.dry_run)
        remove_past_meetup_cards(events_html, today, args.dry_run)
        remove_past_meetup_jsonld(events_html, today, args.dry_run)
    else:
        print("  [!] file not found")

    print("\nsitemap.xml:")
    update_sitemap(repo / "sitemap.xml", args.dry_run)

    print("\nUpcoming meetups:")
    for d in dates[:6]:
        print(f"  {d.strftime('%A, %B %d, %Y').replace(' 0', ' ')}")


if __name__ == "__main__":
    main()
