#!/usr/bin/env python3
"""Check that the outside links on every page still work. Meant for a weekly run, not every pull request:
the web changes on its own schedule, and a slow or rude site shouldn't block a change.

    python3 scripts/check_links.py              # every page
    python3 scripts/check_links.py --limit 20   # the first 20 links (a quick try)
    python3 scripts/check_links.py --host yoyotricks.com

A link fails the run only when it is clearly gone: 404 or 410, a name that no longer exists, or a bad
certificate. Sites that block bots (401, 403, 429), timeouts and server errors are listed as warnings,
since they say nothing certain. Links to this site itself are left to scripts/check_site.py.
Politeness: two requests at a time per host, with a short pause. Standard library only.
"""
import argparse
import concurrent.futures as cf
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OWN_HOSTS = {"dmvthrowers.club", "www.dmvthrowers.club", "register.dmvthrowers.club", "map.dmvthrowers.club"}
UA = "Mozilla/5.0 (compatible; dmvthrowers-linkcheck; +https://dmvthrowers.club/)"
GONE = {404, 410}
UNSURE = {401, 403, 405, 406, 429, 451, 999}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and (a.get("rel") or "") in ("preconnect", "dns-prefetch"):
            return
        for key in ("href", "src"):
            v = (a.get(key) or "").strip()
            if v.lower().startswith(("http://", "https://")):
                self.urls.append(v)


def collect(host=None):
    found = defaultdict(set)
    for page in sorted(ROOT.glob("*.html")):
        p = Links()
        p.feed(page.read_text(encoding="utf-8"))
        for u in p.urls:
            h = urlparse(u).hostname or ""
            if h in OWN_HOSTS or (host and h != host and not h.endswith("." + host)):
                continue
            found[u].add(page.name)
    return found


_locks = defaultdict(lambda: threading.Semaphore(2))
_last = defaultdict(float)
_gate = threading.Lock()


def fetch(url, tries=3):
    host = urlparse(url).hostname or ""
    result = ("warn", "no answer")
    for attempt in range(tries):
        with _locks[host]:
            with _gate:
                wait = _last[host] + 0.3 - time.monotonic()
                _last[host] = time.monotonic() + max(wait, 0)
            if wait > 0:
                time.sleep(wait)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    return ("ok", f"{r.status}" + (f" (moved to {r.geturl()})" if r.geturl().rstrip("/") != url.rstrip("/") else ""))
            except urllib.error.HTTPError as e:
                if e.code in GONE:
                    return ("gone", f"HTTP {e.code}")
                result = ("warn", f"HTTP {e.code}" + (" (blocks bots?)" if e.code in UNSURE else ""))
                if e.code in UNSURE:
                    return result
            except urllib.error.URLError as e:
                reason = e.reason
                if isinstance(reason, ssl.SSLCertVerificationError):
                    return ("gone", f"bad certificate: {reason.verify_message}")
                if isinstance(reason, socket.gaierror) and reason.errno in (socket.EAI_NONAME, -2):
                    return ("gone", "the name no longer exists")
                result = ("warn", f"{reason}")
            except (TimeoutError, socket.timeout):
                result = ("warn", "timed out")
            except Exception as e:  # noqa: BLE001  (anything odd is a warning, never a crash)
                result = ("warn", f"{type(e).__name__}: {e}")
        time.sleep(1.5 * (attempt + 1))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=0, help="only check this many links")
    ap.add_argument("--host", default=None, help="only check links to this host")
    args = ap.parse_args()
    links = collect(args.host)
    urls = sorted(links)
    if args.limit:
        urls = urls[:args.limit]
    print(f"Checking {len(urls)} outside links from {len({p for u in urls for p in links[u]})} pages...", flush=True)
    results = {}
    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        for url, res in zip(urls, pool.map(fetch, urls)):
            results[url] = res
    gone = [(u, r[1]) for u, r in results.items() if r[0] == "gone"]
    warn = [(u, r[1]) for u, r in results.items() if r[0] == "warn"]
    moved = [(u, r[1]) for u, r in results.items() if r[0] == "ok" and "moved to" in r[1]]
    def show(title, rows):
        if rows:
            print(f"\n{title} ({len(rows)})")
            for u, why in rows:
                pages = sorted(links[u])
                on = ", ".join(pages[:3]) + (f" and {len(pages) - 3} more" if len(pages) > 3 else "")
                print(f"  - {u}\n      {why}; on {on}")
    show("BROKEN", gone)
    show("Can't tell (blocked, slow or erroring)", warn)
    show("Moved (worth updating)", moved)
    print(f"\n{len(urls) - len(gone) - len(warn)} ok, {len(warn)} unsure, {len(gone)} broken.")
    sys.exit(1 if gone else 0)


if __name__ == "__main__":
    main()
