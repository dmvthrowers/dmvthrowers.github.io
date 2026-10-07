# Build plan: the rest of the roadmap

The order we build things in, across every repo. The *what* and *why* live in the roadmaps:

- this repo's [`ROADMAP.md`](ROADMAP.md): the club and contest pages, parity, gaps, fair and safe, research
- the registration template's `docs/CONTEST_APP_MASTER_PLAN.md` (item codes F, T, R, S, O, E, D, P)
  and `docs/HUB_ROADMAP.md`
- VA-States' and yoyo-player-map's `docs/ROADMAP.md`, and Scouts-Template-Site's `PARITY.md`

This file is the *how and when*. Written 2026-10-07. Update the status column as PRs open and merge.

## How we work

- **One item, one PR, one repo.** A port to a second repo is its own PR, linked from the first.
- **Every PR says its parity line** ("ports to …", "logged as a gap", or "live-only"), per
  `docs/PARITY.md` in the registration template.
- **Template first, then live.** New app features land in `yoyo-registration-template`, then port to
  VA-States. Static features land wherever they were found and port the other way in a follow-up.
- **Before every push:** the repo's own checks (`build.py` + `check_site.py`, or lint, typecheck,
  tests and build), a look at 360px, no `border-radius` or shadows on the club site, no tracking,
  no outside fonts, relative links. VA-States is production: schema, payment and auth changes get
  production care (additive migrations, nothing applied without the owner).
- **Status:** ☐ not started · ◐ PR open · ☑ merged · ⛔ blocked (says on what).

## In flight (waiting on review)

| PR | What | Item |
|---|---|---|
| site #138 | Stale JotForm notes in CSP comments and `AGENTS.md` | Roadmap Next 10 (part) |
| site #139 | Site check in CI (links, alt, nav and footer drift, JSON-LD) | Parity "automated site check", Next 4 (part) |
| site #140 | Meetup `.ics` feed, weekly job fixes | Gap 9 |
| yoyoclub-template #5 | Meetup `.ics` feed | Gap 9 |
| yoyoclub-template #6 | Optional contact form | Parity |
| yoyoclub-template #7 | Optional status link | Parity |
| yoyo-contest-template #5 | `redirects` setting | Parity |
| yoyo-contest-template #6 | Routine videos and a recap page | Parity, T13 (static side) |
| yoyo-map-template #3 | Search box | Parity, research |
| yoyo-registration-template #45 | Judge scores survive a dropped connection | T19 |
| yoyo-registration-template #46, VA-States #79 | Form labels tied to inputs | VA-States Next 11 |
| Girl-Scout-Troop-80301 #4 | Sync with the template's `build.py` and presets | Scouts parity |

Every one shows a red `github-advanced-security` check: the Copilot quota is used up (owner action
below), not a code problem.

## Wave 0: owner actions and decisions

These unblock later waves. Nothing in code waits on the ones marked *no code waits*.

| # | Action or decision | Unblocks |
|---|---|---|
| 0.1 | Fix the Copilot quota or turn off `github-advanced-security` | Green checks everywhere |
| 0.2 | VA-States "Now" list: close VSYC-26 registration, remove dead env vars, Stripe webhook events, backups and a test restore, rotate staff accounts | *no code waits* |
| 0.3 | Map "Now" list: confirm the service-role key rotation, secret scanning, Vercel storage cleanup | *no code waits* |
| 0.4 | Which VA-States repo is canonical; second owner or org move (Gap 1) | 6.x ports stay simple |
| 0.5 | Archive and purge retention (`docs/specs/season-archive.md` in VA-States) | 4.4 purge and reset, D1, D2 |
| 0.6 | VSYC-27 date and venue | 1.20 contest page reset (#76) |
| 0.7 | Conduct team names (at least two) and response time | 2.8 conduct page, P2 |
| 0.8 | Sponsor questions (17, `docs/SPONSOR_FORM.md`) | Sponsor extras |
| 0.9 | Contest app decisions (master plan Part 7): kendama formats, girls divisions, fan picks, video prelims, results on club sites | F-items, R1, R2, T9, T16 |
| 0.10 | Privacy page JotForm line wording; pack Google Fonts and rank badges; troop `DEPLOY.md`; full map app as a template | 1.x site cleanups, scouts parity |
| 0.11 | Press kit source file (to fix "Founded 2023") | 1.19 |
| 0.12 | Add `dmvt-event-hub` and `DMVT-Design` to the agent's repo access | Wave 7, 3.9 |

## Wave 1: small, decision-free, static (start now)

Each is a few hours or less. Ordered by value.

| # | Repo | Item | Status |
|---|---|---|---|
| 1.1 | site | `/.well-known/security.txt` with the contact address (Next 8) | ◐ #142 |
| 1.2 | site | Status link in every footer, not only contact (Next 11) | ◐ #143 |
| 1.3 | site | Sitemap check in the site check (every page in `sitemap.xml`, no dead entries) — after #139 | ☐ |
| 1.4 | site | Guide part numbering: renumber body headings per part (Next 6) | ◐ #144 |
| 1.5 | site | Cold-load flash on `vsyc26.html`: logo size (Next 9); fonts are 2.12 | ◐ #145 |
| 1.6 | site | Raw hex colors in page `<style>` blocks → brand variables (Later) | ☐ |
| 1.7 | site | Headings that skip a level (h1 → h3) | ☐ |
| 1.8 | all three static templates | Deploy guard: the build warns, and CI fails, when sample data (example.org email, "Jordan Example") would ship to a real site | ☐ |
| 1.9 | yoyo-map-template | `og:image`, a privacy page, h1→h3 fix | ☐ |
| 1.10 | yoyo-map-template | Marker clustering (vendored Leaflet.markercluster, MIT) | ☐ |
| 1.11 | yoyo-map-template | Browse-by-place pages (one static page per region) | ☐ |
| 1.12 | yoyo-map-template | Visibility per entry: city, region, or listed but not pinned | ☐ |
| 1.13 | yoyoclub-template | Conduct settings: team, report link, steps, version, effective date | ☐ |
| 1.14 | yoyo-contest-template | Same conduct settings | ☐ |
| 1.15 | Scouts-Template-Site | Photo permission and first-names-only settings, with `check_site.py` flagging full names | ☐ |
| 1.16 | Scouts-Template-Site | Youth protection section (two-adult rule, official training links) as a setting | ☐ |
| 1.17 | Scouts-Template-Site | Forms library page (permission, medical, registration forms with dates) | ☐ |
| 1.18 | yoyoclub-template | Optional "For schools" page (parity with `teachers.html`) and loaner program page | ☐ |
| 1.19 | site | Press kit "Founded 2021" | ⛔ 0.11 |
| 1.20 | site | #76: archive VSYC-26 pages and reset for VSYC-27, stale post-event wording | ⛔ 0.6 |

## Wave 2: medium static features

| # | Repo | Item | Status |
|---|---|---|---|
| 2.1 | yoyo-contest-template | Bracket page built from config (no outside embed) | ☐ |
| 2.2 | yoyo-contest-template | Optional merch and side-event pages | ☐ |
| 2.3 | yoyoclub-template | Long-form guides: hub plus parts from `content/`, shared references, deep-link forwarder | ☐ |
| 2.4 | site + templates | One shared JS: pick `mobile-enhancements.js` as the source, port `site.js` improvements both ways | ☐ |
| 2.5 | site | HTML validation in CI (`vnu`) (Next 5) | ☐ |
| 2.6 | site | External link checker (`lychee`, weekly, not per PR) (Next 4) | ☐ |
| 2.7 | site | Guides in the main nav, one change across every page (Next 7) | ☐ |
| 2.8 | site | Conduct page: named team, steps, response time, changelog | ⛔ 0.7 |
| 2.9 | all templates | Releases: tag v1.0.0, `CHANGELOG.md`, an "update your copy" guide (Gap 2) | ☐ |
| 2.10 | all templates | Showcase smoke test in CI: build every example, click every page in Chromium (Gap 5) | ☐ |
| 2.11 | all static repos | Automated accessibility check (axe) in CI, then fix what it finds (Gap 3) | ☐ |
| 2.12 | site | Self-host Playfair Display, DM Sans and Montserrat (OFL): ends the font swap flash and removes Google Fonts from every page's CSP | ☐ |

## Wave 3: the player map app (`yoyo-player-map`)

Its own roadmap's "Next" list, all decision-free. One PR each.

| # | Item | Status |
|---|---|---|
| 3.1 | Error envelope on the 11 routes still returning bare `{ error }` | ☐ |
| 3.2 | hreflang alternates and per-page canonicals for the 11 locales | ☐ |
| 3.3 | Idempotency key and 24h dedupe on `POST /api/submit` | ☐ |
| 3.4 | Map accessibility: container label, link to `/players` for keyboard and screen readers | ☐ |
| 3.5 | Re-enable the React Compiler lint rules and fix what they flag | ☐ |
| 3.6 | Split the 820-line admin page into components | ☐ |
| 3.7 | OSV-Scanner workflow: delete if broken (as on the site) | ☐ |
| 3.8 | Remove unused `wouter`, unmounted analytics packages; `@types/node@22` | ☐ |
| 3.9 | Free vector tiles (OpenFreeMap) for both maps | ☐ |

## Wave 4: the contest app, Phase 1 (template first, then VA-States)

From the master plan's Phase 1, ordered so each builds on the last. Every item: lib with unit
tests, additive migration if any, UI at 360px, then a port PR to VA-States.

| # | Item | Notes | Status |
|---|---|---|---|
| 4.1 | Port score status, round plans, split, prizes, DJ battle view, disputes, bot check, champion rule into the template | Parity (VA-States → template). Prerequisite for T1 and the rest | ☐ |
| 4.2 | Port roles and `/staff`, migration replay in CI, setup scripts, three tests into VA-States | Parity (template → VA-States). Production care | ☐ |
| 4.3 | Migration number map (0037–0049) and the survey table name | Parity "Both". Docs plus one rename | ☐ |
| 4.4 | Season archive purge and reset | ⛔ 0.5 | ⛔ |
| 4.5 | T19 port to VA-States | After template #45 merges | ☐ |
| 4.6 | T1 scores-in board | Builds on score status | ☐ |
| 4.7 | T2 release gates (run order gate, head-judge "checked") | | ☐ |
| 4.8 | P4 published draws (recorded seed, re-checkable) | | ☐ |
| 4.9 | P1 code of conduct version recorded per person, re-accept on change | | ☐ |
| 4.10 | R11 photo and video consent at registration, honored on results videos | Before any video work ships in the app | ☐ |
| 4.11 | T11 how it was scored + T12 score shading | Frontend only | ☐ |
| 4.12 | T4 MC cards (say-it-like-this name, intro line) | | ☐ |
| 4.13 | O5 rules with a changelog · O4 open books (public budget page) | | ☐ |
| 4.14 | T18 contest guide page + O1 first contest path | | ☐ |
| 4.15 | E8 email log stub · E9 first admin once | Setup safety | ☐ |
| 4.16 | F1 bracket match scores | Kendama payoff; format steps in master plan Part 6 | ☐ |
| 4.17 | S2 trick list page, S3 prize table, S7 kendama preset | Kendama choices ⛔ 0.9 for S7 | ☐ |
| 4.18 | R2 $0 add-on divisions | ⛔ 0.9 (girls divisions) | ⛔ |
| 4.19 | VA-States leftovers: admin route rate limit (Next 8), money-path route tests (Next 9) | | ☐ |
| 4.20 | VA-States results data gaps on `/results` (Next 12) | Needs a read of the import rows | ☐ |

## Wave 5: platform pieces

| # | Item | Notes |
|---|---|---|
| 5.1 | Forms on our own system (config plus one submission table), sponsor form as the first instance | Unblocks P2 and the conduct report form |
| 5.2 | P2 confidential conduct reports on the forms system, linked from every footer (site, templates, app) | Needs 0.7 for routing |
| 5.3 | Scoring-format interface and registry (hub "next steps" 1) | Before any new format in wave 6 |
| 5.4 | Stage 1: `event_id` with a default, `events` in config, per-event routes and results (hub steps 2–4), E2 one event shape | |
| 5.5 | Finance and budget upgrade (feeds O4) | |
| 5.6 | E4 daily housekeeping, E5 report a problem, E6 status page, E1 filtered feeds | |
| 5.7 | Move VSYC wording in VA-States into config until shared files match the template | Parity "Both", ongoing |

## Wave 6: contest app Phase 2 and 3

Formats (F3, F6, F7, F9, then F2, F4, F5, F8, F10), the public side (T10, T13, T14, T15, T17, R10),
music desk (T5), player page (O2), video prelims (R1), volunteer shifts (T8), the research items
(D3, D4, D6, then D1, D2, D5), the remaining fair-and-safe items (P3, P5–P9), and the convention
items (S8, R7, R8). Ordered as in the master plan Part 6. Plan each one in its own PR description
when we get there; most wait on wave 5.

## Wave 7: event hub, languages, brand

| # | Item | Notes |
|---|---|---|
| 7.1 | Event hub launch: real email provider, untrack `.env`, fix `skills/`, point `events.dmvthrowers.club` | ⛔ 0.12 |
| 7.2 | Hub archive, search, open data, embeds | After 7.1 |
| 7.3 | Club events page reads the hub's feed | After 7.1 |
| 7.4 | Spanish on the club and contest pages; a `language` setting with translatable strings in the templates (Gap 4) | |
| 7.5 | Brand parity check against DMVT-Design tokens (Gap 8) | ⛔ 0.12 |
| 7.6 | Site search with a static index (Pagefind) | Needs a CI step that writes the index; owner nod since the site has no build step |
| 7.7 | News archive with RSS, supporters page | Content from the owner |

## What we're chipping first

Wave 1 top to bottom, then wave 3 (the map app's list is self-contained), with wave 4's parity
ports (4.1–4.3) starting once the open registration-template PRs merge, so each port starts from
a clean base.
