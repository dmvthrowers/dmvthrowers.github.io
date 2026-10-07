# dmvthrowers.club — Roadmap

Open work for the static site, in priority order. Built from the October 2026 audit; every
status was re-checked against the repo on 2026-10-02. VSYC-27 planning items live in GitHub
issues #76–#96 (contest-app items carry a `[VA-States]` prefix).

## Done since the audit

| Item | Where |
|---|---|
| Dependabot PR #67 (Actions SHA bumps) merged | #67 |
| Real club/contest photos replace AI images | #110 |
| `learn-yoyo.html` and `yoyo-gear.html` split into hub + 4 parts, with a deep-link forwarder | merged Oct 1 |
| Glossary "Read more" links all have descriptive `aria-label`s (28 already did; last 2 added) | this PR |
| Broken OSV-Scanner workflow deleted (failed at startup on every run; the repo has no lockfiles to scan) | this PR |
| `.pre-commit-config.yaml` was invalid YAML (`: ` inside an unquoted value), so no hook could ever run — fixed. Hooks bumped to `pre-commit-hooks` v6.0.0, and CNAME is now excluded from the whitespace/EOF fixers so a hook run can't touch it | this PR |
| `environment.yml` Python 3.10 (EOL this month) → 3.13 | this PR |
| Remaining `http://` links (unprld.com, kinopah.blogspot.com) upgraded to `https://` | this PR |

## Now

1. **#76 Archive VSYC-26 and reset the contest pages for VSYC-27** — target is October.
   Keep the date and venue of VSYC-26 exactly as they are on the archived pages.
2. **Stale post-event wording** on VSYC pages: `vsyc26.html` OG/Twitter descriptions still end
   "Free to spectate", and `vsyc26-dueling-stars.html` says "Stella Duellum returns to VA States".
   Fold into #76.
3. **Press kit says "Founded 2023"**; the club was founded in 2021. Fix the source and re-export
   `assets/documents/DMV Throwers Press Kit.pdf`.

## Next

4. **Replace the JotForm sponsor form (#77).** It's the site's only third-party script, loaded
   unpinned from `/latest/`, and ad blockers often block it. Until it's replaced, it's the
   biggest script-supply-chain risk on the site.
5. **Link checker in CI** (`lychee` against the staged site) — the hub ↔ part guide links,
   redirect stubs and JSON-LD URLs are all hand-maintained and drift silently.
6. **HTML validation in CI** (`vnu` / `html5validator`) for the copy-paste boilerplate.
7. **Guide part numbering.** Part intros say "Part N of 4", but body section headings keep the
   old global numbers (e.g. maintenance is "Part 2 of 4" with sections "PART 4–9"). Renumber the
   body headings per part, or drop the numbers.
8. **Guides aren't in the main nav.** The largest content (learn-yoyo, yoyo-gear, history,
   science, collecting) is reachable only through inline links. Adding a nav item means editing
   every page's nav identically — plan it as one change across all pages.
9. **`/.well-known/security.txt`** with a contact address.
10. **Cold-load flash on `vsyc26.html`**: hero title briefly renders in fallback fonts and the nav
    logo shows a broken-image glyph. Check font-display and the logo's `width`/`height`.

## Later

- Shared nav/footer styles drift between `main.css` and `vsyc26.css`; a small shared stylesheet
  would cut per-page edits without adding a build step.
- Security headers: GitHub Pages can't send HSTS/CSP headers; per-page CSP `<meta>` tags are the
  enforcement. Putting Cloudflare (free) in front would add real headers.
- Sitemap check in CI so a new page can't ship without a `sitemap.xml` entry.

- **Raw hex colors** remain in page `<style>` blocks. Convert them to `--red`, `--navy`, `--cream`
  and `--border`.

## Decisions needed (owner)

- **Heading case on the guide pages:** Title Case (the brand rule) or leave as is.
- **Share cards:** `dmvt-share.png` and `vsyc26-share.png` render in fallback system fonts.
  Regenerate them with Playfair Display?
- **GitHub topics and descriptions** on the six template repos (set by hand in each repo's
  settings). Suggested topics: `yo-yo`, `skill-toys`, `github-pages`, `static-site`,
  `website-template`.
- **Girl-Scout-Troop-80301 history:** volunteer names are still in git history. Rewriting
  history is only worth it if that matters.

## Discoverability (from the Oct 2 audit — not code)

- "DMV" collides with motor-vehicle results: always pair the name with "yo-yo club" in titles,
  H1s and the first lines of key pages.
- GitHub repos outrank the site for "DMV Throwers"; make sure the GitHub profile links to the site
  prominently.
- No Google Business Profile — create one at Arlington Central Library (free; biggest win for
  "yoyo club near me").
- A third-party listing (ngos1.com) shows the wrong phone number; request a correction.
- Submit VSYC-27 to the NYYL calendar (yoyocontest.com) once it's dated.

## Other club repos (tracked here)

### yoyo-player-map: dependency majors

Each is its own migration and PR:

- react 18 → 19, with `@types/react` and `@types/react-dom`
- eslint 9 → 10
- react-leaflet 4 → 5, and react-leaflet-cluster 3 → 4
- typescript 6 → 7
- workflow 4 → 5. It also warns about an unmet peer (`@swc/core` 1.15.3 wanted, 1.16.13
  installed); harmless today.
- `@types/node` 25 → 26
- `braces` stays allow-listed (GHSA-vfj7-8cjw-p6xm). Drop the entry once a patched release exists.

### yoyo-player-map: product

- About 43% of the non-English map strings are untranslated.
- Confirm Googlebot gets past the Vercel checkpoint on `map.dmvthrowers.club`; if not, the map
  can't be indexed.

### Generated and template sites

- Some generated pages skip from h1 to h3.
- The troop site's `build.py` hasn't been synced back to the upstream template.
- The map template has no `og:image`.
- No deploy guard stops sample data from shipping to a live site.

### VA-States and the registration template

- Refactor inline styles and large components.
- Remove the legacy `/admin` pages.
- Contest app features (formats, contest-day tools, spectator pages): see the registration
  template's `docs/CONTEST_APP_PLAN.md`, with its sources `CONTEST_APP_MASTER_PLAN.md` and
  `FORMAT_RESEARCH.md`, linked from `docs/HUB_ROADMAP.md`.
