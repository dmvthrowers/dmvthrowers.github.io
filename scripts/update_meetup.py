#!/usr/bin/env python3
"""
DMV Throwers — Update 3rd Sunday meetup dates and clear past meetup events.

Run this the Monday after each 3rd Sunday meetup to keep the site current:
  1. Update the "NEXT MEET" top bar on every page that has one
  2. Remove past monthly meetup event cards from events.html
  3. Remove past monthly meetup entries from the JSON-LD in events.html
  4. Update sitemap.xml lastmod for every page that changed
  5. Rewrite meetups.ics (the next 12 meetups) for calendar subscriptions

Usage:
  python scripts/update_meetup.py
  python scripts/update_meetup.py --repo /path/to/repo
  python scripts/update_meetup.py --dry-run
"""

import argparse
import json
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


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


def fmt_banner(d: date) -> str:
    """Return 'SUNDAY, OCTOBER 18' (the current top-bar style), uppercased."""
    return f"{d.strftime('%A')}, {d.strftime('%B')} {d.day}".upper()


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


# The current top bar: "NEXT MEET: SUNDAY, OCTOBER 18 · 1–4 PM · ARLINGTON CENTRAL LIBRARY".
_BANNER_RE = re.compile(
    r"(NEXT MEET:\s*)"
    r"((?:MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),\s*"
    r"(?:JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|"
    r"OCTOBER|NOVEMBER|DECEMBER)\s+\d{1,2})(?!,\s*\d{4})",
    re.IGNORECASE,
)


def update_topbar(html_path: Path, next_date: date, dry_run: bool = False, quiet: bool = False) -> bool:
    """Replace the date in the 'NEXT MEET: …' top-bar span (either style)."""
    text = html_path.read_text(encoding="utf-8")

    if _BANNER_RE.search(text):
        new_str = fmt_banner(next_date)
        new_text = _BANNER_RE.sub(lambda m: m.group(1) + new_str, text)
    elif _TOPBAR_RE.search(text):
        new_str = fmt_upper(next_date)
        new_text = _TOPBAR_RE.sub(lambda m: m.group(1) + new_str, text)
    else:
        if not quiet:
            print(f"  [!] NEXT MEET pattern not found in {html_path.name}")
        return False
    if new_text == text and quiet:
        return False
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

# Matches a meetup card: <div class="event-card"> or the highlighted
# <div class="event-card event-card-next">. Holiday and special-event cards
# carry other classes and are left alone.
# Event-card divs sit at 4-space indent; inner divs are 6+ spaces, so
# \n    </div> reliably marks only the outermost closing tag.
_MEETUP_CARD_RE = re.compile(
    r"\n    <div class=\"event-card(?: event-card-next)?\">\n(.*?)\n    </div>",
    re.DOTALL,
)
_MEETUP_LABELS = ("● MONTHLY MEETUP", "● NEXT MEETUP")
_FIRST_TIME_LINE = ('          <div class="event-loc">First time? Just show up. We have loaners, '
                    'and someone will teach you your first throw.</div>')


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
    except (ValueError, IndexError):
        return None

    # Cards omit the year; infer it from proximity to today.
    # Two year-boundary cases need correction:
    #
    #   delta < -180  (>6 months in the past with today.year)
    #     → probably a future card for next year.
    #       e.g. a January 2027 card added in November 2026 reads as Jan 2026.
    #       Threshold: 180 days comfortably clears the ~1-month "just-past" zone.
    #
    #   delta > 330  (>11 months in the future with today.year)
    #     → probably a stale card from last year.
    #       e.g. a December 2026 card still in the file in January 2027 reads
    #       as December 2027. Threshold: 330 avoids false positives for
    #       legitimately scheduled meetups 6–10 months out (e.g. a November
    #       card encountered in May is only ~193 days away).
    try:
        candidate = date(today.year, month_num, day)
    except ValueError:
        return None
    delta = (candidate - today).days
    if delta > 330:
        try:
            candidate = date(today.year - 1, month_num, day)
        except ValueError:
            return None
    elif delta < -180:
        try:
            candidate = date(today.year + 1, month_num, day)
        except ValueError:
            return None
    return candidate


def remove_past_meetup_cards(events_path: Path, today: date | None = None, dry_run: bool = False) -> bool:
    """Remove monthly meetup cards whose dates precede *today*."""
    if today is None:
        today = date.today()

    text = events_path.read_text(encoding="utf-8")
    removed = 0

    def replacer(m: re.Match) -> str:
        nonlocal removed
        body = m.group(1)
        if not any(label in body for label in _MEETUP_LABELS):
            return m.group(0)  # not a meetup card
        card_date = _parse_card_date(body, today)
        if card_date is not None and card_date < today:
            removed += 1
            return ""
        return m.group(0)

    new_text = _MEETUP_CARD_RE.sub(replacer, text)

    if removed == 0:
        print(f"  [=] {events_path.name}: no past meetup cards to remove")
        return False

    # The highlighted "NEXT MEETUP" card was the one that just passed:
    # promote the next monthly meetup card in its place.
    if 'class="event-card event-card-next"' not in new_text:
        def promote(m: re.Match) -> str:
            body = m.group(1)
            if "● MONTHLY MEETUP" not in body:
                return m.group(0)
            body = body.replace("● MONTHLY MEETUP", "● NEXT MEETUP", 1)
            lines = body.split("\n")
            last_loc = max((i for i, l in enumerate(lines) if 'class="event-loc"' in l), default=None)
            if last_loc is not None and "First time?" not in body:
                lines.insert(last_loc + 1, _FIRST_TIME_LINE)
            return '\n    <div class="event-card event-card-next">\n' + "\n".join(lines) + "\n    </div>"
        new_text = _MEETUP_CARD_RE.sub(promote, new_text, count=1)

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
# meetups.ics — calendar subscription (webcal://dmvthrowers.club/meetups.ics)
# ---------------------------------------------------------------------------

MEETUP_TZ = ZoneInfo("America/New_York")
MEETUP_START, MEETUP_END = time(13, 0), time(16, 0)
MEETUP_WHERE = "Arlington Central Library, 1015 N Quincy St, Arlington, VA 22201"
MEETUP_DESC = ("Free monthly yo-yo and skill toy meetup. All ages, all levels, always free. "
               "Loaner yo-yos available. No registration required.")


def _ics_text(v: str) -> str:
    return v.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _ics_fold(line: str) -> str:
    out, b = [], line.encode("utf-8")
    while len(b) > 75:
        cut = 75
        while (b[cut] & 0xC0) == 0x80:  # don't split a UTF-8 character
            cut -= 1
        out.append(b[:cut].decode("utf-8"))
        b = b" " + b[cut:]
    out.append(b.decode("utf-8"))
    return "\r\n".join(out)


def _ics_utc(d: date, t: time) -> str:
    return datetime.combine(d, t, tzinfo=MEETUP_TZ).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_ics(dates: list[date]) -> str:
    """The next meetups as an iCalendar file. Times are written in UTC so daylight saving is right
    in every calendar app. DTSTAMP is derived from the dates, not the clock, so the file only
    changes (and the workflow only commits) when the list of dates moves on."""
    stamp = datetime.combine(dates[0] - timedelta(days=31), time(0, 0), tzinfo=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//DMV Throwers//Meetups//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:DMV Throwers meetups",
             "X-WR-TIMEZONE:America/New_York"]
    for d in dates:
        lines += ["BEGIN:VEVENT", f"UID:{d.isoformat()}-meetup@dmvthrowers.club", f"DTSTAMP:{stamp}",
                  f"SUMMARY:{_ics_text('DMV Throwers monthly meetup')}",
                  f"DTSTART:{_ics_utc(d, MEETUP_START)}", f"DTEND:{_ics_utc(d, MEETUP_END)}",
                  f"LOCATION:{_ics_text(MEETUP_WHERE)}", f"DESCRIPTION:{_ics_text(MEETUP_DESC)}",
                  "URL:https://dmvthrowers.club/events.html", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(_ics_fold(l) for l in lines) + "\r\n"


def write_ics(ics_path: Path, dates: list[date], dry_run: bool = False) -> bool:
    new = build_ics(dates)
    old = ics_path.read_text(encoding="utf-8", newline="") if ics_path.exists() else ""
    if new == old:
        print(f"  [=] {ics_path.name}: already current")
        return False
    if not dry_run:
        ics_path.write_text(new, encoding="utf-8", newline="")
    print(f"  [ok] {ics_path.name}: {len(dates)} meetups from {dates[0].isoformat()}")
    return True


# ---------------------------------------------------------------------------
# sitemap.xml — bump lastmod for index/events URLs
# ---------------------------------------------------------------------------

# Pages whose lastmod should be refreshed after a meetup update.
# Use exact URL strings to avoid false matches (e.g. "index" in a path).
_SITEMAP_TARGETS = (
    "https://dmvthrowers.club/",          # homepage — trailing slash, no "index"
    "https://dmvthrowers.club/events.html",
)

# Matches a <loc>TARGET</loc> block followed (anywhere in the same <url>
# element) by a <lastmod>YYYY-MM-DD</lastmod> to be replaced.
# We do a text-level substitution to preserve the file's formatting,
# comments, and XML declaration exactly — ET.write() would rewrite all of
# that and add namespace prefixes on a first run.
def _make_lastmod_re(url: str) -> re.Pattern[str]:
    return re.compile(
        r"(<loc>" + re.escape(url) + r"</loc>(?:(?!</url>).)*?<lastmod>)"
        r"\d{4}-\d{2}-\d{2}"
        r"(</lastmod>)",
        re.DOTALL,
    )


def page_url(name: str) -> str:
    return "https://dmvthrowers.club/" if name == "index.html" else f"https://dmvthrowers.club/{name}"


def update_sitemap(sitemap_path: Path, dry_run: bool = False, pages: list[str] | None = None) -> bool:
    """
    Update <lastmod> in sitemap.xml for the pages that changed (default: the
    homepage and events page). Uses text-level substitution so the file's
    formatting and XML declaration are preserved unchanged.
    """
    if not sitemap_path.exists():
        return False
    try:
        text = sitemap_path.read_text(encoding="utf-8")
        today_str = date.today().isoformat()
        new_text = text
        targets = [page_url(p) for p in pages] if pages else _SITEMAP_TARGETS
        for target_url in targets:
            new_text = _make_lastmod_re(target_url).sub(
                r"\g<1>" + today_str + r"\2", new_text
            )
        if new_text == text:
            print("  [=] sitemap.xml: lastmod already current")
            return False
        if not dry_run:
            sitemap_path.write_text(new_text, encoding="utf-8")
        print(f"  [ok] sitemap.xml: lastmod -> {today_str}")
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
    parser.add_argument(
        "--today",
        help="Pretend today is YYYY-MM-DD (for testing)",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    today = date.fromisoformat(args.today) if args.today else date.today()
    dates = upcoming_third_sundays(12, today)
    next_date = dates[0]

    print(f"Today       : {today.isoformat()}")
    print(f"Next meetup : {next_date.strftime('%A, %B %d, %Y').replace(' 0', ' ')}")
    if args.dry_run:
        print("(dry-run - no files will be modified)\n")

    events_html = repo / "events.html"
    changed: list[str] = []

    print("\nTop bar (every page):")
    for page in sorted(repo.glob("*.html")):
        if update_topbar(page, next_date, args.dry_run, quiet=True):
            changed.append(page.name)
    if not changed:
        print("  [=] already current everywhere")

    print("\nevents.html:")
    if events_html.exists():
        if remove_past_meetup_cards(events_html, today, args.dry_run) | \
           remove_past_meetup_jsonld(events_html, today, args.dry_run):
            if "events.html" not in changed:
                changed.append("events.html")
    else:
        print("  [!] file not found")

    # Only bump sitemap lastmod for pages that actually changed. Updating it
    # unconditionally would cause a commit every Monday even when the
    # banner and cards were already current.
    print("\nsitemap.xml:")
    if changed:
        update_sitemap(repo / "sitemap.xml", args.dry_run, changed)
    else:
        print("  [=] skipped (no page content changed)")

    print("\nmeetups.ics:")
    write_ics(repo / "meetups.ics", dates, args.dry_run)

    print("\nUpcoming meetups:")
    for d in dates[:6]:
        print(f"  {d.strftime('%A, %B %d, %Y').replace(' 0', ' ')}")


if __name__ == "__main__":
    main()
