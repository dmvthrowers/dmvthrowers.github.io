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

## Decisions made (2026-10-07)

| Topic | Decision | Lands in |
|---|---|---|
| `github-advanced-security` red on every PR | Leave it red until the Copilot quota resets; merge anyway | — |
| Fonts | Self-host Playfair Display, DM Sans and Montserrat on the club site | 2.12 |
| Off-palette colors | Map them to brand colors (before/after screenshots in the PR) | 1.6b |
| Guides in the nav | Add one GUIDES item, same on every page, to a guides hub | 2.7 |
| Canonical VA-States repo | `dmvthrowers/VA-States` | 0.4 |
| JotForm on the privacy page | Remove it; no JotForm form is live | 1.21 |
| Pack 1125 | Self-host fonts; plain rank names instead of badge images | scouts parity |
| Full map app as a template | Yes, plan it as a level-2 template | 7.8 |
| Troop `DEPLOY.md`, `TEMPLATE-README.md` | Generalize into the scouts template | 1.19b |
| Site search | Yes: a static index (Pagefind) built in CI, club site and club template | 7.6 |
| Guide heading case | Title Case everywhere | 1.22 |
| Share cards | Regenerate both with the brand fonts | 1.23 |
| Kendama | Trick-deck battles and speed ladder first; a kendama division at VSYC-27 | 4.16, 4.17 |
| Girls divisions | $0 add-ons fed by the main division's results | 4.18 |
| Fan picks | Build it, off by default | wave 6 |
| Video prelims and online entries | Yes, in a later phase | wave 6 |
| Brackets from other tools | Support CSV import and export | wave 6 (R9) |
| Results on club sites | A public feed any club can use | wave 6 (T16) |
| Sponsor payments | Invoice only | — |
| Open books | Kept in the app's finance screens | 5.5 |
| Event hub and contest app | Two apps sharing one event format | 5.4, wave 7 |
| Juggling | Host our own convention (moves S8, R7, R8 earlier) | wave 6 |
| TypeScript 7 on the map | Wait for 7.1 | — |
| Payment records | Keep 7 years | 4.4 |
| Waivers and guardian consent | Until the minor turns 21; 3 years for adults | 4.4 |
| Registrant personal data | Anonymize after the archive merges; keep stats | 4.4 |
| Player accounts | Keep across seasons; purge each season's data | 4.4 |
| Past champions table | Yes, public names only | 4.4 |
| Dismissed sponsor inquiries | Delete after 1 year | sponsor extras |
| Troop git history | Leave it | — |
| GitHub topics on the templates | `yo-yo`, `skill-toys`, `github-pages`, `static-site`, `website-template` (owner sets them) | 0.13 |

## Wave 0: owner actions and decisions

These unblock later waves. Nothing in code waits on the ones marked *no code waits*.

| # | Action or decision | Unblocks |
|---|---|---|
| 0.1 | ~~Copilot quota~~ Decided: leave red until it resets | — |
| 0.2 | VA-States "Now" list: close VSYC-26 registration, remove dead env vars, Stripe webhook events, backups and a test restore, rotate staff accounts | *no code waits* |
| 0.3 | Map "Now" list: confirm the service-role key rotation, secret scanning, Vercel storage cleanup | *no code waits* |
| 0.4 | Canonical repo decided (`dmvthrowers/VA-States`); still open: a second owner or org move (Gap 1) | Bus factor |
| 0.5 | ~~Archive and purge retention~~ Decided (see above) | 4.4 unblocked |
| 0.6 | VSYC-27 date and venue | 1.20 contest page reset (#76) |
| 0.7 | Conduct team names (at least two) and response time | 2.8 conduct page, P2 |
| 0.8 | Sponsor questions (17, `docs/SPONSOR_FORM.md`) | Sponsor extras |
| 0.9 | ~~Contest app decisions~~ Decided (see above) | F1, S7, R2 unblocked |
| 0.10 | ~~Privacy JotForm, pack fonts and badges, troop docs, map template~~ Decided (see above) | — |
| 0.11 | Press kit source file (to fix "Founded 2023") | 1.19 |
| 0.12 | Add `dmvt-event-hub` and `DMVT-Design` to the agent's repo access | Wave 7, 3.9 |
| 0.13 | Set GitHub topics on the six template repos (Settings → About) | Discoverability |

## Wave 1: small, decision-free, static (start now)

Each is a few hours or less. Ordered by value.

| # | Repo | Item | Status |
|---|---|---|---|
| 1.1 | site | `/.well-known/security.txt` with the contact address (Next 8) | ◐ #142 |
| 1.2 | site | Status link in every footer, not only contact (Next 11) | ◐ #143 |
| 1.3 | site | Sitemap check in the site check (every page in `sitemap.xml`, no dead entries) — after #139 | ◐ #150 |
| 1.4 | site | Guide part numbering: renumber body headings per part (Next 6) | ◐ #144 |
| 1.5 | site | Cold-load flash on `vsyc26.html`: logo size (Next 9); fonts are 2.12 | ◐ #145 |
| 1.6 | site | Raw hex colors in page `<style>` blocks → brand variables (Later); off-palette ones need a design call | ◐ #146 |
| 1.7 | site + templates | Headings that skip a level (h1 → h3) | ◐ #147, club #8, scouts #6 |
| 1.8 | all four static templates | Deploy guard: a copy's CI fails while sample data (example.org, the sample names) would ship | ◐ club #9, contest #7, scouts #7, map #4 |
| 1.9 | yoyo-map-template | `og:image`, a privacy page, h1→h3 fix | ◐ map #5 |
| 1.10 | yoyo-map-template | Marker clustering (vendored Leaflet.markercluster, MIT) | ◐ map #6 |
| 1.11 | yoyo-map-template | Browse-by-place pages (one static page per region) | ◐ map #7 |
| 1.12 | yoyo-map-template | Visibility per entry: city, region, or listed but not pinned | ◐ map #8 |
| 1.13 | yoyoclub-template | Conduct settings: team, report link, steps, version, effective date | ◐ club #10 |
| 1.14 | yoyo-contest-template | Same conduct settings | ◐ contest #8 |
| 1.15 | Scouts-Template-Site | Photo permission and first-names-only settings, with `check_site.py` flagging full names | ◐ scouts #8 |
| 1.16 | Scouts-Template-Site | Youth protection section (two-adult rule, official training links) as a setting | ◐ scouts #9 |
| 1.17 | Scouts-Template-Site | Forms library page (permission, medical, registration forms with dates) | ◐ scouts #10 |
| 1.18 | yoyoclub-template | Optional "For schools" page (parity with `teachers.html`) and loaner program page | ◐ club #11 |
| 1.19 | site | Press kit "Founded 2021" | ⛔ 0.11 |
| 1.20 | site | #76: archive VSYC-26 pages and reset for VSYC-27, stale post-event wording | ⛔ 0.6 |
| 1.6b | site | Map off-palette colors to brand colors (events, team, index, terms, about) | ◐ #151 |
| 1.19b | Scouts-Template-Site | Generalized `DEPLOY.md` from the troop repo | ◐ scouts #11 |
| 1.21 | site | Remove JotForm from `privacy.html` | ◐ #148 |
| 1.22 | site | Title Case on guide headings | ◐ #152 |
| 1.23 | site | Regenerate `dmvt-share.png` and `vsyc26-share.png` with the brand fonts | ◐ #153 |

## Wave 2: medium static features

| # | Repo | Item | Status |
|---|---|---|---|
| 2.1 | yoyo-contest-template | Bracket page built from config (no outside embed) | ◐ contest #9 |
| 2.2 | yoyo-contest-template | Optional merch and side-event pages | ◐ contest #10 |
| 2.3 | yoyoclub-template | Long-form guides: hub plus parts from `content/`, shared references, deep-link forwarder | ☐ |
| 2.4 | site + templates | One shared JS: pick `mobile-enhancements.js` as the source, port `site.js` improvements both ways | ☐ |
| 2.5 | site | HTML validation in CI (`vnu`) (Next 5) | ◐ #154 |
| 2.6 | site | External link checker (`lychee`, weekly, not per PR) (Next 4) | ◐ #157 |
| 2.7 | site | Guides in the main nav, one change across every page (Next 7) | ◐ #155 |
| 2.8 | site | Conduct page: named team, steps, response time, changelog | ⛔ 0.7 |
| 2.9 | all templates | Releases: tag v1.0.0, `CHANGELOG.md`, an "update your copy" guide (Gap 2) | ◐ club #12, contest #11, scouts #12, map #9; tag is owner |
| 2.10 | all templates | Showcase smoke test in CI: build every example, click every page in Chromium (Gap 5) | ◐ club #13, contest #12, scouts #13, map #10 |
| 2.11 | all static repos | Automated accessibility check (axe) in CI, then fix what it finds (Gap 3) | ☐ |
| 2.12 | site | Self-host Playfair Display, DM Sans and Montserrat (OFL): ends the font swap flash and removes Google Fonts from every page's CSP | ◐ #149 |

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
| 4.4 | Season archive purge and reset, with the retention decisions above | Production care | ☐ |
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
| 4.17 | S2 trick list page, S3 prize table, S7 kendama preset (trick-deck battles + speed ladder) | | ☐ |
| 4.18 | R2 $0 add-on divisions (girls divisions as $0 add-ons) | | ☐ |
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
| 7.8 | Full map app as a level-2 template (like the registration app) | After wave 3 |

## What we're chipping first

Wave 1 top to bottom, then wave 3 (the map app's list is self-contained), with wave 4's parity
ports (4.1–4.3) starting once the open registration-template PRs merge, so each port starts from
a clean base.
