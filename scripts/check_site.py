#!/usr/bin/env python3
"""Check every page of the hand-written site for the problems that creep in when the same
boilerplate is copied across 40+ files. Ported from the club and contest templates'
check_site.py, minus their no-inline-styles rule (pages here use a per-page <style> block and
small inline scripts on purpose).

    python3 scripts/check_site.py

Checks: broken internal links and images (paths resolve from the repo root, because every page
has <base href="/">), images without alt text, missing title or description, the CSP meta tag,
the skip link and main#main-content, valid JSON-LD with a BreadcrumbList, no http:// links, and
that the main nav and footer are identical across each group of pages (club pages, VSYC pages).
Redirect stubs are skipped, and 404.html is left out of the nav and footer comparison
(it has a deliberately minimal nav and no footer). Exits non-zero if anything fails. Standard library only.
"""
import html as htmllib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.imgs, self.ids, self.ld = [], [], set(), []
        self._ld = False
        self.title = False
        self.meta = {}
        self.csp = None
        self.http = []
        self.refresh = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if a.get(k) and tag not in ("iframe", "base"):
                self.refs.append(a[k])
            if (a.get(k) or "").strip().lower().startswith("http:"):
                self.http.append(a[k])
        if tag == "img":
            self.imgs.append(a)
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = a.get("content", "")
        equiv = (a.get("http-equiv") or "").lower()
        if tag == "meta" and equiv == "content-security-policy":
            self.csp = a.get("content") or ""
        if tag == "meta" and equiv == "refresh":
            self.refresh = True
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False

    def handle_data(self, d):
        if self._ld:
            self.ld[-1] += d


def block(html, start_pat, end):
    """The first element matching start_pat through its closing tag, normalized for comparison."""
    m = re.search(start_pat, html)
    if not m:
        return ""
    j = html.find(end, m.start())
    chunk = html[m.start():j + len(end)] if j >= 0 else ""
    chunk = chunk.replace(' aria-current="page"', "").replace('nav-link active', 'nav-link')
    return re.sub(r"\s+", " ", htmllib.unescape(chunk)).strip()


def resolves(ref):
    u = urlparse(ref)
    if u.scheme or ref.startswith(("#", "mailto:", "tel:", "data:", "//")):
        return True
    path = unquote(u.path).lstrip("/")
    if not path:
        return True
    target = ROOT / path
    return target.exists() or (target.with_suffix(".html")).exists() or (target / "index.html").exists()


groups = {}
pages = sorted(ROOT.glob("*.html"))
for page in pages:
    html = page.read_text(encoding="utf-8")
    p = Page()
    p.feed(html)
    err = lambda msg, n=page.name: errors.append(f"{n}: {msg}")
    if p.refresh:
        continue  # redirect stub
    if not p.title:
        err("missing <title>")
    if not p.meta.get("description"):
        err("missing meta description")
    if p.csp is None:
        err("missing Content-Security-Policy meta tag")
    if 'class="skip-link"' not in html:
        err("missing skip link")
    if not re.search(r'<main[^>]*id="main-content"', html):
        err('missing <main id="main-content">')
    for ref in p.http:
        err(f"insecure http:// link: {ref}")
    for ref in p.refs:
        if not resolves(ref):
            err(f"broken link or image: {ref}")
    for img in p.imgs:
        if "alt" not in img:
            err(f"img without alt: {img.get('src')}")
    crumbs = False
    for raw in p.ld:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            err(f"invalid JSON-LD: {e}")
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        crumbs = crumbs or any(isinstance(i, dict) and i.get("@type") == "BreadcrumbList" for i in items)
    if page.name != "404.html" and not crumbs:
        err("no BreadcrumbList JSON-LD")
    group = "vsyc26" if page.name.startswith("vsyc26") else "club"
    nav = block(html, r'<nav aria-label="Main navigation"', "</nav>")
    foot = block(html, r"<footer[ >]", "</footer>")
    if page.name != "404.html":  # the error page has a deliberately minimal nav and no footer
        groups.setdefault(group, []).append((page.name, nav, foot))

for group, members in groups.items():
    for i, label in ((1, "main nav"), (2, "footer")):
        variants = {}
        for m in members:
            variants.setdefault(m[i], []).append(m[0])
        if len(variants) > 1:
            common = max(variants.values(), key=len)
            for names in variants.values():
                if names is not common:
                    errors.append(f"{group} pages: {label} differs from the {len(common)}-page majority on {', '.join(names)}")

if errors:
    print("\n".join(errors))
    print(f"\nFAILED: {len(errors)} problem(s) across {len(pages)} pages.")
    sys.exit(1)
print(f"OK: {len(pages)} pages checked, no problems found.")
