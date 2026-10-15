#!/usr/bin/env python3
"""Check the brand and site guardrails that check_site.py doesn't cover. Runs before every deploy.

    python3 scripts/check_brand.py
    BASE_SHA=<commit> python3 scripts/check_brand.py   # also check sitemap lastmod against that commit

Checks:
  - Square corners: no non-zero border-radius in assets/css/*.css or any page (style blocks and
    style="" attributes). assets/printables/ is left out: the kids' worksheets are print handouts
    with their own look, not site pages.
  - No shadows: no box-shadow, except on :focus / :focus-visible / :focus-within rules, where it is
    a keyboard focus ring (the skip link and the contact form inputs use one).
  - No animations: no @keyframes or animation property. Short hover transitions are fine.
  - No external fonts: no Google Fonts, Typekit, Bunny or Font Awesome CDN. Fonts are self-hosted.
  - No tracking: no analytics or ad-pixel scripts.
  - Relative links: no absolute https://dmvthrowers.club link to a file that lives in this repo.
    (Links to the template sites served under the same domain from other repos are fine.)
  - Image weight: every image a page or stylesheet actually loads is under 500 KB. Unreferenced
    source masters (assets/images/gallery/originals/, raw logos) are not checked and must not be
    deleted.
  - Sitemap lastmod: valid YYYY-MM-DD, not in the future, and, when BASE_SHA is set, bumped for every
    listed page that changed since that commit.

Exits non-zero if anything fails. Standard library only.
"""
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
MAX_IMAGE_BYTES = 500 * 1024
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif", ".ico"}
FONT_HOSTS = re.compile(r"fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net|p\.typekit\.net"
                        r"|fonts\.bunny\.net|use\.fontawesome\.com|kit\.fontawesome\.com", re.I)
TRACKERS = re.compile(r"googletagmanager\.com|google-analytics\.com|plausible\.io|connect\.facebook\.net"
                      r"|static\.hotjar\.com|clarity\.ms|cdn\.segment\.com|cdn\.mxpnl\.com|matomo\.(js|php)"
                      r"|umami\.is|stats\.wp\.com|doubleclick\.net|snap\.licdn\.com|analytics\.tiktok\.com", re.I)
# <a> links only: canonical <link> tags and og:url are absolute by design.
SELF = re.compile(r'<a\s[^>]*href="(https?://(?:www\.)?dmvthrowers\.club/[^"#?]*)', re.I)

errors = []
pages = sorted(ROOT.glob("*.html"))
stylesheets = sorted((ROOT / "assets" / "css").glob("*.css"))
deployed_text = pages + stylesheets + sorted((ROOT / "assets").rglob("*.html")) + sorted((ROOT / "assets" / "js").glob("*.js"))


def rel(p):
    return p.relative_to(ROOT).as_posix()


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_sources(path):
    """(label, css) pairs: the whole file for .css; each <style> block and style="" attribute for .html."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".css":
        return [(rel(path), strip_comments(text))]
    out = [(f"{rel(path)} <style>", strip_comments(m)) for m in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S | re.I)]
    out += [(f"{rel(path)} style=\"\"", "{" + m + "}") for m in re.findall(r'\sstyle="([^"]*)"', text, re.I)]
    return out


def is_zero(value):
    value = value.replace("!important", "").strip()
    return all(re.fullmatch(r"0(\.0+)?(px|rem|em|%)?", t) for t in re.split(r"[\s/]+", value) if t)


# ---- CSS rules: corners, shadows, animations
for path in stylesheets + pages:
    for label, css in css_sources(path):
        if re.search(r"@keyframes\b", css):
            errors.append(f"{label}: @keyframes animation (no animations)")
        for selector, body in re.findall(r"([^{}]*)\{([^{}]*)\}", css):
            selector = " ".join(selector.split())
            for prop, value in re.findall(r"(?:^|;)\s*([a-z-]+)\s*:\s*([^;]+)", body, re.I):
                prop = prop.lower()
                if prop.endswith("border-radius") or prop in ("border-top-left-radius", "border-top-right-radius",
                                                              "border-bottom-left-radius", "border-bottom-right-radius"):
                    if not is_zero(value):
                        errors.append(f"{label}: {selector or '(inline)'} has border-radius: {value.strip()} (corners stay square)")
                elif prop == "box-shadow":
                    if value.strip().lower() in ("none", "0", "unset", "initial") or ":focus" in selector:
                        continue
                    errors.append(f"{label}: {selector or '(inline)'} has box-shadow: {value.strip()} (no shadows)")
                elif prop in ("animation", "animation-name") and value.strip().lower() not in ("none", "unset", "initial"):
                    errors.append(f"{label}: {selector or '(inline)'} has {prop}: {value.strip()} (no animations)")

# ---- Fonts and trackers, in everything that ships
for path in deployed_text:
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in sorted(set(FONT_HOSTS.findall(text))):
        errors.append(f"{rel(path)}: loads an external font host ({m}); fonts are self-hosted in assets/fonts/")
    for m in re.finditer(r'(?:src|href)\s*=\s*"([^"]+)"', text):
        if TRACKERS.search(m.group(1)):
            errors.append(f"{rel(path)}: tracking script or pixel: {m.group(1)}")

# ---- Absolute links to our own files
for path in pages:
    for url in SELF.findall(path.read_text(encoding="utf-8")):
        local = unquote(urlparse(url).path).lstrip("/") or "index.html"
        target = ROOT / local
        if target.is_file() or (target / "index.html").is_file() or target.with_suffix(".html").is_file():
            errors.append(f"{rel(path)}: absolute link {url}; use a relative link ({local})")


# ---- Image weight, for images that are actually loaded
def image_refs(path):
    text = path.read_text(encoding="utf-8")
    refs = re.findall(r"url\(\s*['\"]?([^'\")]+)", text)
    if path.suffix == ".html":
        refs += re.findall(r'\ssrc="([^"]+)"', text)
        refs += re.findall(r'<link[^>]+href="([^"]+)"', text)
        refs += re.findall(r'<meta[^>]+content="(https?://(?:www\.)?dmvthrowers\.club/[^"]+)"', text)
        for srcset in re.findall(r'\ssrcset="([^"]+)"', text):
            refs += [c.strip().split()[0] for c in srcset.split(",") if c.strip()]
    return refs


checked = set()
for path in pages + stylesheets:
    for ref in image_refs(path):
        u = urlparse(ref.strip())
        if ref.startswith("data:") or (u.netloc and "dmvthrowers.club" not in u.netloc.lower()):
            continue
        local = unquote(u.path)
        if Path(local).suffix.lower() not in IMAGE_EXT:
            continue
        # Stylesheets resolve relative to themselves; pages resolve from the root (<base href="/">).
        target = (path.parent / local).resolve() if path.suffix == ".css" and not local.startswith("/") else ROOT / local.lstrip("/")
        if target in checked or not target.is_file():
            continue  # missing files are check_site.py's job
        checked.add(target)
        size = target.stat().st_size
        if size > MAX_IMAGE_BYTES:
            errors.append(f"{rel(target)}: {size // 1024} KB, over the 500 KB limit (loaded by {rel(path)})")

# ---- Sitemap lastmod
sitemap = ROOT / "sitemap.xml"


def lastmods(xml):
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", block)
        mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block)
        if loc:
            out[urlparse(loc.group(1)).path.lstrip("/") or "index.html"] = mod.group(1) if mod else None
    return out


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


if sitemap.exists():
    now = lastmods(sitemap.read_text(encoding="utf-8"))
    tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    for name, mod in now.items():
        if not mod:
            errors.append(f"sitemap.xml: {name} has no <lastmod>")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}(T[\d:.+-]+Z?)?", mod):
            errors.append(f"sitemap.xml: {name} lastmod '{mod}' is not YYYY-MM-DD")
        elif mod[:10] > tomorrow:
            errors.append(f"sitemap.xml: {name} lastmod {mod} is in the future")

    base = os.environ.get("BASE_SHA", "").strip()
    if base and set(base) != {"0"} and git("cat-file", "-e", f"{base}^{{commit}}") is not None:
        old_xml = git("show", f"{base}:sitemap.xml") or ""
        old = lastmods(old_xml)
        changed = set((git("diff", "--name-only", base, "HEAD") or "").split())
        for name in sorted(changed & set(now)):
            if name in old and (now[name] or "")[:10] <= (old[name] or "")[:10]:
                errors.append(f"sitemap.xml: {name} changed but its lastmod is still {now[name]}; bump it to today")
    elif base:
        print(f"note: BASE_SHA {base[:12]} not available here; skipped the lastmod-bump check")

if errors:
    print("\n".join(errors))
    print(f"\nFAILED: {len(errors)} brand or guardrail problem(s).")
    sys.exit(1)
print(f"OK: brand and guardrails pass ({len(pages)} pages, {len(stylesheets)} stylesheets, {len(checked)} images under 500 KB).")
