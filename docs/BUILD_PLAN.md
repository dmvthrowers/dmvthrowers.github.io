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

Nothing from the first build session: every PR it opened (site #138–#149, #158; templates; map
#258–#270; registration #45, #46; VA-States #79; troop #4) merged by 2026-10-10. What's left for
the owner is in Wave 0 below.

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
| Turnstile bot check | On everywhere, behind a setting; goes live when the Cloudflare keys are added | 4.1 |
| Champion rule | Port it into the template as a config option; collect the home address only when a contest uses a state champion | 4.1 |
| Roles and `/staff` | In the template, no personal data lives there (checked 2026-10-10). Also port them into the live app, as part of the parity rule | 4.2, 8.9 |
| Girls division | An option any contest can switch on: a $0 add-on, self-tick, optional age limits. A ready-to-copy example goes in the template docs | 4.18 |
| Per-judge public score sheet | Build it, named "Judges' Scores", off by default | 4.11 |
| Audit-log retention | 12 months after the event, then purged with the season | 4.4 |
| Who reads form answers | Admins, plus staff an admin explicitly grants `forms.review` | 5.1 |
| Multi-event | Every event is treated as multi-event, and an event can have its own organizers. Designed first (`docs/MULTI_EVENT.md`), then built in stages | 5.4 |
| Survey table name | Not renamed now; rename `vsyc26_survey_responses` when a contest is archived | 4.3 |
| Photo release | Mandatory for competitors: no acceptance, no entry (as built). Migration 0055 stays unused | 4.10 |
| Shared JS across the site and templates | Keep them separate; port improvements by hand | 2.4 |

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
| 0.14 | Player map: look at OpenFreeMap tiles (`NEXT_PUBLIC_MAP_TILES=openfreemap` in `pnpm dev`), then set it in Vercel if you like it | 3.9 goes live |
| 0.15 | Map template tiles: OpenFreeMap needs ~1 MB of MapLibre in every copy. Recommendation: keep OpenStreetMap raster | 3.9 template half |
| 0.16 | Close Dependabot map #251 and #245 (`@types/node` 26); #263 pinned the runtime's 22 and ignores majors | Dependabot noise |
| 0.17 | Production check of submit dedupe (#259): submit the same form twice, expect the same message and one row in `entries` | Confirms 3.3 |
| 0.18 | Prize scale for VSYC-27 | Real amounts in the S3 prize table (template #68) |

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
| 2.3 | yoyoclub-template | Long-form guides: hub plus parts from `content/`, shared references, deep-link forwarder | ◐ yoyoclub-template #15 (merged) |
| 2.4 | site + templates | One shared JS: pick `mobile-enhancements.js` as the source, port `site.js` improvements both ways | ☑ decided: keep them separate, port by hand |
| 2.5 | site | HTML validation in CI (`vnu`) (Next 5) | ◐ #154 |
| 2.6 | site | External link checker (`lychee`, weekly, not per PR) (Next 4) | ◐ #157 |
| 2.7 | site | Guides in the main nav, one change across every page (Next 7) | ◐ #155 |
| 2.8 | site | Conduct page: named team, steps, response time, changelog | ⛔ 0.7 |
| 2.9 | all templates | Releases: tag v1.0.0, `CHANGELOG.md`, an "update your copy" guide (Gap 2) | ◐ club #12, contest #11, scouts #12, map #9; tag is owner |
| 2.10 | all templates | Showcase smoke test in CI: build every example, click every page in Chromium (Gap 5) | ◐ club #13, contest #12, scouts #13, map #10 |
| 2.11 | all static repos | Automated accessibility check (axe) in CI, then fix what it finds (Gap 3) | ◐ club #14, contest #13, scouts #14 (merged); map #11, site #159 |
| 2.12 | site | Self-host Playfair Display, DM Sans and Montserrat (OFL): ends the font swap flash and removes Google Fonts from every page's CSP | ◐ #149 |

## Wave 3: the player map app (`yoyo-player-map`)

Its own roadmap's "Next" list, all decision-free. One PR each.

| # | Item | Status |
|---|---|---|
| 3.1 | Error envelope on the 11 routes still returning bare `{ error }` | ☑ map #258 |
| 3.2 | hreflang alternates and per-page canonicals for the 11 locales | ☑ already done (map `5587eb2`) |
| 3.3 | Idempotency key and 24h dedupe on `POST /api/submit` | ☑ map #259 |
| 3.4 | Map accessibility: container label, link to `/players` for keyboard and screen readers | ☑ map #260 |
| 3.5 | Re-enable the React Compiler lint rules and fix what they flag | ☑ map #261 |
| 3.6 | Split the 820-line admin page into components | ☑ map #269 |
| 3.7 | OSV-Scanner workflow: delete if broken (as on the site) | ☑ map #262 |
| 3.8 | Remove unused `wouter`, unmounted analytics packages; `@types/node@22` | ☑ map #263 |
| 3.9 | Free vector tiles (OpenFreeMap) for both maps | ☑ map #265 (player map, off by default; turning it on is 0.14). Template half ⛔ 0.15 |

## Wave 4: the contest app, Phase 1 (template first, then VA-States)

From the master plan's Phase 1, ordered so each builds on the last. Every item: lib with unit
tests, additive migration if any, UI at 360px, then a port PR to VA-States.

| # | Item | Notes | Status |
|---|---|---|---|
| 4.1 | Port score status, round plans, split, prizes, DJ battle view, disputes, bot check, champion rule into the template | Parity (VA-States → template). Prerequisite for T1 and the rest | ◐ template #47 score status, #48 bot check, #49 split, #50 prizes, #51 DJ battle view, #52 round plans, #53 dispute flags; champion rule is an owner decision (not built) |
| 4.2 | Port roles and `/staff`, migration replay in CI, setup scripts, three tests into VA-States | Parity (template → VA-States). Production care | ◐ VA-States #82 (merged: migration replay in CI, setup script, three tests). Roles and `/staff` not ported: owner call |
| 4.3 | Migration number map (0037–0049) and the survey table name | Parity "Both". Docs plus one rename | ◐ template #54, VA-States #80 |
| 4.4 | Season archive purge and reset, with the retention decisions above | Production care | ◐ VA-States #83 (merged). Migration 0060 applied to production 2026-10-10; nothing purged |
| 4.5 | T19 port to VA-States | After template #45 merges | ◐ VA-States #84 (merged) |
| 4.6 | T1 scores-in board | Builds on score status | ◐ template #55 (stacked on #47) |
| 4.7 | T2 release gates (run order gate, head-judge "checked") | | ✓ VA-States #90 (off until `dayOf.releaseGates`); migration 0052 applied 2026-10-10 |
| 4.8 | P4 published draws (recorded seed, re-checkable) | | ✓ VA-States #91 (off until `dayOf.publishedDraws`); migration 0053 applied 2026-10-10 |
| 4.9 | P1 code of conduct version recorded per person, re-accept on change | | ✓ VA-States #92; migration 0054 applied 2026-10-10 (record only; re-accept prompt is a follow-up) |
| 4.10 | R11 photo and video consent at registration, honored on results videos | Before any video work ships in the app | ◐ template #59, migration 0055; decided: mandatory for competitors, nothing to build |
| 4.11 | T11 how it was scored + T12 score shading | Frontend only | ◐ template #60; per-judge public score sheet ("Judges' Scores") decided, to build |
| 4.12 | T4 MC cards (say-it-like-this name, intro line) | | ✓ VA-States #93 (admin only); migration 0056 applied 2026-10-10 |
| 4.13 | O5 rules with a changelog · O4 open books (public budget page) | | ◐ rules changelog: template #62 only; ✓ open books VA-States #94, migration 0057 applied 2026-10-10 |
| 4.14 | T18 contest guide page + O1 first contest path | | ◐ template #64 |
| 4.15 | E8 email log stub · E9 first admin once | Setup safety | ◐ template #65 |
| 4.16 | F1 bracket match scores | Kendama payoff; format steps in master plan Part 6 | ✓ VA-States #95 (off until a division sets `matchScoring`); migration 0058 applied 2026-10-10 |
| 4.17 | S2 trick list page, S3 prize table, S7 kendama preset (trick-deck battles + speed ladder) | | ◐ template #67 (S7, S2; stacked on #66), #68 (S3; stacked on #50) |
| 4.18 | R2 $0 add-on divisions (girls divisions as $0 add-ons) | | ✓ VA-States #96 (no add-on configured yet); migration 0059 applied 2026-10-10 |
| 4.19 | VA-States leftovers: admin route rate limit (Next 8), money-path route tests (Next 9) | | ◐ VA-States #81 (merged) |
| 4.20 | VA-States results data gaps on `/results` (Next 12) | Needs a read of the import rows | ◐ VA-States #85 (merged): the read-only query is in; the fix waits on its output |

## Wave 5: platform pieces

| # | Item | Notes |
|---|---|---|
| 5.1 | Forms on our own system (config plus one submission table), sponsor form as the first instance | ◐ registration template #70 (engine, `/forms/<id>`, `/forms-review`, migration 0061). The sponsor form is not moved onto it yet: it has tier slots and a convert step |
| 5.2 | P2 confidential conduct reports on the forms system, linked from every footer (site, templates, app) | ⛔ owner: who is on the conduct team, and who sees reports (see "Waiting on owner" (a)). Needs 0.7 for routing |
| 5.3 | Scoring-format interface and registry (hub "next steps" 1) | Deferred on purpose: `FORMATS` plus TypeScript exhaustiveness already list every place a new format must touch. Extract the interface together with the first Wave 6 format (F3) so its shape comes from a real second format |
| 5.4 | Stage 1: `event_id` with a default, `events` in config, per-event routes and results (hub steps 2–4), E2 one event shape | ◐ decided: every event is multi-event with its own organizers; design first. Was: is a deployment one organizer running several events, or separate organizers sharing a hub? (hub open question 1). Large schema change; not started |
| 5.5 | Finance and budget upgrade (feeds O4) | Not started: scope is not defined beyond "open books" (done in 4.13). Needs a list of what finance wants to see |
| 5.6 | E4 daily housekeeping, E5 report a problem, E6 status page, E1 filtered feeds | E5 can be a plain form on the 5.1 engine (add one to `contest.forms`; see `docs/FORMS.md`). The others are not started |
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

## Wave 8: parity (owner rule, 2026-10-10)

The template and the live repo stay in parity: core features exist in both, and the live repo differs only
where it holds real data or its own config and content. The registration app's gaps come from a file-by-file
audit (`yoyo-registration-template/docs/PARITY.md`, PR #73). One PR per row, lowest risk first. Production
care applies to every row that touches VA-States: off by default where it can be, tests, no unreviewed
migration.

| # | Direction | Item | Notes |
|---|---|---|---|
| 8.1 | VA-States → template | Home-state eligibility and the champion rule, as a config option | Blank `stateChampion.state` turns it off |
| 8.2 | VA-States → template | Season purge and reset code, `scripts/purge.ts`, results-gaps query | Design is already in the template's `SEASON_ARCHIVE.md` |
| 8.3 | VA-States → template | Money-path route test harness and its stubs | |
| 8.4 | VA-States → template | Nightly encrypted backup workflow, generic day-of runbook, generic audit and spec docs | |
| 8.5 | template → VA-States | Schedule clash check | No migration |
| 8.6 | template → VA-States | Contest guide, rules with changelog, trick-list pages | Config-driven; VA-States keeps its own content |
| 8.7 | template → VA-States | Setup safety: email log stub, first admin once, auth email renderer, local deadline display | |
| 8.8 | template → VA-States | Forms engine, `/forms-review`, migration 0061 | Off unless a form is configured; needs the Supabase SQL editor for the migration |
| 8.9 | template → VA-States | Roles, grants, `/staff` pane, then the role pages (media, merch, stream, volunteers, finance, event, staff) | Largest port; touches sign-in, so last, behind a flag, with route tests. Owner: yes |
| 8.10 | static sites and maps | Same audit for the club site and club template, contest site and contest template, map app and map template, scouts template and the two live sites | Not started |

## Waiting on owner (2026-10-10)

Everything below needs a person. Template PRs #47–#69, VA-States #80–#85, club-template #15 and the live-site docs PRs are merged; this list is what is left.

### (a) Facts and answers

| Item | What is needed | Unblocks |
|---|---|---|
| 5.2 | Conduct reports (P2): who is on the conduct team (at least two named people), who gets told, how reports are acknowledged and how long you keep them. The forms engine and review screen are ready for it. | Building the confidential report form |
| 1.19 / 1.20 | Founded-year source; VSYC-27 date and venue | Those two club-site edits |
| 0.x | Items 0.2–0.4, 0.6–0.8, 0.11–0.13 | See Wave 0 |
| other | yoyomagic.fun 404, GUIDES in the VSYC nav, Challonge embed replacement, open axe colour findings, troop repo items | Each as noted in its PR |

### (b) Dashboard and account actions

- Create a `v1.0.0` tag on each of the four static templates.
- Cloudflare Turnstile: create the site and keys.
- Stripe: turn on `charge.dispute.created` and `charge.dispute.closed` for the webhook.
- Repo access for `dmvt-event-hub` and `DMVT-Design` (0.12).
- Run `scripts/results-gaps.sql` read-only in the Supabase SQL editor and send the output (4.20).
- Supabase API: DDL through the API times out on project `vsyc26-registration` (migration 0060 was applied by hand in the SQL editor). Worth a support ticket.
- Before any purge: take a backup, test a restore, run `npm run purge` as a dry run and read the counts, then `--apply`. Not before the 2026 archive page is live.

### (c) Migrations

- VA-States 0060: applied 2026-10-10 (tables first, functions by hand). Add the history row if you track it.
- VA-States 0052–0059: applied 2026-10-10 in the Supabase SQL editor (the API tool hangs on any statement containing `DROP`, so constraint changes go through the editor). 0055 (photo release) is skipped on purpose. The code for all of them is merged and each feature is off until its setting is turned on.
- Template 0050–0059: nothing to apply until a deployment exists. Deploy order for a new deployment: apply 0054, 0056, 0057, 0058 before turning on the routes that write them.

### (d) Reviews and merges

Nothing open from this run except the owner items above. The migration-dependent VA-States ports (4.7, 4.8, 4.9, 4.12, 4.13, 4.16, 4.18) are merged; 4.10 waits on the photo release decision. Still to build: 2.4, Waves 5–7. After the next registration, check that `code_of_conduct_version` is stored, and open `/budget` to confirm the totals.

## What we're chipping first

Wave 1 top to bottom, then wave 3 (the map app's list is self-contained), with wave 4's parity
ports (4.1–4.3) starting once the open registration-template PRs merge, so each port starts from
a clean base.
