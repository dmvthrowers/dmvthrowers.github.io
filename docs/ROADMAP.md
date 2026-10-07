# dmvthrowers.club — Roadmap

Open work for the static site, in priority order. Built from the October 2026 audit; every
status was re-checked against the repo on 2026-10-02. VSYC-27 planning items live in GitHub
issues #76–#96 (contest-app items carry a `[VA-States]` prefix).

The build order across every repo, with status per item, is in [`BUILD_PLAN.md`](BUILD_PLAN.md).

## Done since the audit

| Item | Where |
|---|---|
| Dependabot PR #67 (Actions SHA bumps) merged | #67 |
| Real club/contest photos replace AI images | #110 |
| `learn-yoyo.html` and `yoyo-gear.html` split into hub + 4 parts, with a deep-link forwarder | merged Oct 1 |
| Glossary "Read more" links all have descriptive `aria-label`s (28 already did; last 2 added) | this PR |
| Broken OSV-Scanner workflow deleted (failed at startup on every run; the repo has no lockfiles to scan) | this PR |
| `.pre-commit-config.yaml` was invalid YAML (`: ` inside an unquoted value), so no hook could ever run — fixed. Hooks bumped to `pre-commit-hooks` v6.0.0, and CNAME is now excluded from the whitespace/EOF fixers so a hook run can't touch it | this PR |
| JotForm sponsor embed replaced by a link to `register.dmvthrowers.club/sponsor` (no third-party script left on `vsyc26-sponsors.html`) | #77 |
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

4. **Link checker in CI** (`lychee` against the staged site) — the hub ↔ part guide links,
   redirect stubs and JSON-LD URLs are all hand-maintained and drift silently.
5. **HTML validation in CI** (`vnu` / `html5validator`) for the copy-paste boilerplate.
6. ~~**Guide part numbering.**~~ Done: section labels on each part now read "Section 1, 2…"
   per page, and the two hub labels read "Quick reference".
7. **Guides aren't in the main nav.** The largest content (learn-yoyo, yoyo-gear, history,
   science, collecting) is reachable only through inline links. Adding a nav item means editing
   every page's nav identically — plan it as one change across all pages.
8. ~~**`/.well-known/security.txt`** with a contact address.~~ Done; renew its `Expires` line
   before 2027-10-01.
9. **Cold-load flash on `vsyc26.html`**: hero title briefly renders in fallback fonts and the nav
    logo shows a broken-image glyph. Check font-display and the logo's `width`/`height`.
10. **JotForm leftovers.** ~~`privacy.html` still lists JotForm as a registration processor.~~
   Removed (owner confirmed no JotForm form is live). 16 pages (`about.html`,
   `index.html`, `teachers.html`, the guides) carry stale "jotform for VSYC-26" CSP comments.
   `AGENTS.md` still describes a JotForm embed on `vsyc26-sponsors.html`. One small PR.
11. ~~**Status page link in the footers**, not only on the contact page.~~ Done: every footer
    links the UptimeRobot status page.

## Later

- Shared nav/footer styles drift between `main.css` and `vsyc26.css`; a small shared stylesheet
  would cut per-page edits without adding a build step.
- Security headers: GitHub Pages can't send HSTS/CSP headers; per-page CSP `<meta>` tags are the
  enforcement. Putting Cloudflare (free) in front would add real headers.
- Sitemap check in CI so a new page can't ship without a `sitemap.xml` entry.

- **Raw hex colors** in page `<style>` blocks. Brand colors and white are now variables
  everywhere (`--white` added to `main.css`). What's left is off-palette, so mapping it changes how
  pages look and needs a design call: the events page's status colors (greens, blues, greys), the
  team page's badge colors, the teal on `index.html`, and the gold and grey-blue text on
  `vsyc26-terms.html` and `about.html` (`#f0c040`, `#8090b8`, `#c8d0e0`).

## Owner actions (not code)

- **Send one test sponsor inquiry** at `register.dmvthrowers.club/sponsor` (the database has
  none yet), then check the row, the slot count and the notice email.
- **Set `SPONSOR_NOTICE_EMAIL`** in Vercel for the registration app.
- **UptimeRobot monitor** for `register.dmvthrowers.club/api/health` (only the homepage is
  checked today).
- **`github-advanced-security` is red on every PR in the org.** On 2026-10-07 the job log showed
  the Copilot code-scanning agent failing with HTTP 402, "exceeded your monthly quota", before
  it scanned anything. Fix the Copilot quota or billing, or turn the check off; it isn't a code
  problem.
- **Review and merge the draft PRs:** VA-States #78 (archive), yoyo-registration-template #41
  (archive) and #43 (contest app plans), site #135 (status page link) and #136 (this roadmap).
- **Check production's migration history:** `0032_revoke_anon_table_access` reads
  `20261001190000` now but read `20261001205725` earlier on 2026-10-06.
- **Re-check the VA-States roadmap's "Now" list:** close the VSYC-26 registration flag, remove
  dead Vercel env vars, Stripe webhook events (refunds, disputes), turn on backups and test a
  restore, rotate contest-day staff accounts.
- **Supply the lo-fi tracks** for `vsyc26-music/lofi/`.

## Decisions needed (owner)

- **VSYC-27 sponsor questions** (17 in the template's `docs/SPONSOR_FORM.md`): tiers, prices and
  slot caps; whether an inquiry holds a slot; table add-on cap and hobby-club price; logo link or
  upload; shipping from abroad; nonprofit status and receipts; refund and payment wording; how
  long to keep dismissed inquiries.
- **Archive and purge** (VA-States `docs/specs/season-archive.md`): payment records, waiver and
  guardian consent retention, anonymize or delete registrants, whether returning players keep
  accounts, whether to keep a past-champions table.
- **Prize scale rules.**
- **TypeScript 7 on yoyo-player-map:** hold for 7.1, or take #250 (green).
- **Contest app open questions:** the ten in the registration template's
  `docs/CONTEST_APP_MASTER_PLAN.md` (Part 6).

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

## Parity fixes (audit, 2026-10-07)

Every live site stays in step with its template (see `docs/PARITY.md` in the registration
template). This audit compared each pair. Fixes are listed by direction: what the template should
gain from the live site, and the reverse.

### VSYC pages ↔ `yoyo-contest-template`

Same core pages on both sides (home, schedule, register, rules, venue, sponsors, results, FAQ,
terms, 404). Into the template:

- **Results with routine videos and a recap page.** Live has `vsyc26-results.html` and
  `vsyc26-recap.html` with privacy-friendly YouTube embeds; the template's results page has none.
- **A bracket page.** Live `vsyc26-dueling-stars.html` embeds a Challonge bracket; the template has
  bracket settings but no page. Build it from the template's own config (or the registration app)
  rather than an outside embed, per the contest app plan.
- **Merch and side-event pages.** Live has `vsyc26-merch.html` and `vsyc26-twirly-tour.html`;
  the template has neither. Add both as optional pages.
- **Redirects for retired pages.** Live keeps `vsyc26-battles.html` and `vsyc26-divisions.html` as
  redirect stubs; add a `redirects` setting so a template site can retire a page without breaking
  links.

### Club pages ↔ `yoyoclub-template`

Same core pages (home, about, meetups/events, team, gallery, resources, FAQ, contact, conduct,
privacy, 404). Into the template:

- **Long-form guides.** Live has the "How to Yo-Yo" and "Gear" hubs with four parts each, a
  deep-link forwarder, a shared references list, and standalone guides (history, science,
  collecting, Filipino yo-yo history). The template has one Learn page. Add optional guide pages
  (hub plus parts) from `content/`.
- **A contact form.** Live uses Formspree with a honeypot and a locked CSP `form-action`; the
  template only shows an email link. Add an optional form endpoint, off by default.
- **A teachers page.** Live has `teachers.html`; add it as an optional "For schools" page.
- **A status page link** in the footer (site #135), as an optional setting.

Into the live site:

- **An automated site check.** The template's `scripts/check_site.py` fails the build when headers
  or footers differ, links break or alt text is missing. Live hand-copies the same nav and footer
  onto about 40 pages with no check; run an equivalent in CI (goes with "Link checker" and "HTML
  validation" under Next). The template's version also rejects inline styles and scripts, which
  live pages use on purpose (per-page `<style>`, the FAQ toggle), so port the header, footer, link,
  alt-text and JSON-LD checks and leave that rule out.

Both: live uses `assets/js/mobile-enhancements.js`, the templates use `assets/site.js`. Pick one
as the source for shared fixes (menu, external-link safety) and port the other's improvements.

### Registration app (`VA-States` ↔ `yoyo-registration-template`)

The full list is in the template's `docs/PARITY.md`. The headline:

- **Into the template:** home-state champion rule, round plans, division split, prizes, score
  status, DJ battle view, payment dispute flags, the bot check, nightly backups, the day-of runbook.
- **Into VA-States:** roles and the `/staff` pane with its role pages, migration replay in CI, the
  setup scripts, newer `resend` and `@vercel/analytics`, three test files.
- **Both:** 151 of 236 shared files differ, mostly VSYC wording written into VA-States code where
  the template reads config. Move it into config until shared files match. Migration numbers
  0037–0049 mean different things in each repo; map them before porting schema changes.

### Troop and pack sites (`Scouts-Template-Site`)

The full list is in that repo's `PARITY.md`. The headline:

- **Girl Scout Troop 80301** is behind the template. Copy the template's `build.py` (custom words,
  automatic Vercel address) and `presets/`, then rebuild.
- **Cub Scout Pack 1125** loads Google Fonts (the template promises no outside fonts), shows
  official rank badges (confirm permission or use plain names), and runs a different check script.

### Player map (`yoyo-player-map` ↔ `yoyo-map-template`)

Two levels again: the template is the simple static map, the live map is a full app. Features the
simple map could gain without a server: marker clustering, a search box, browse-by-place pages,
and a privacy page. Multiple languages, accounts and moderation stay full-app only.
**Decision:** should the full map app also become a template (level 2), like the registration app?

## Gaps found in the roadmap review (2026-10-07)

Things no roadmap covered yet, checked against every repo's roadmap and the principles in the
registration template's `docs/CONTEST_APP_MASTER_PLAN.md`.

1. **Accounts and the bus factor.** `github.com/dmvthrowers` is one user account; every repo, and
   most service logins, run through it. A `DMV-Throwers` organization already exists (with its own
   copy of VA-States). Move the repos into the organization or add a second owner, add a second
   admin on Vercel, Supabase, Stripe, Porkbun and Resend, keep logins in a shared password manager,
   and write a one-page handoff note. Also decide which VA-States repo is canonical.
2. **Template releases.** The templates have no versions, so "pull template updates cleanly" has
   nothing to pull. Tag releases, keep a `CHANGELOG.md`, and add a short "update your copy" guide to
   each template. Parity ports land in the next release.
3. **Accessibility pass.** Only spot fixes are planned (map markers, one form label). Do a WCAG 2.2
   AA review of the club site, contest pages, templates and registration app, and add an automated
   axe check to each CI.
4. **Languages.** The map speaks 11 languages; the club site, contest pages, registration app and
   static templates are English only. Start with Spanish on the club and contest pages, and give the
   templates a `language` setting with translatable strings.
5. **End-to-end smoke tests.** No repo has one. Add a Playwright run of the registration happy path
   (Stripe test mode) to the registration template and VA-States, and a build-and-click run of each
   template's showcase.
6. **Photo and video consent.** Minors' names are protected, but photos and routine videos aren't
   tied to any consent. Record photo and video consent at registration (a guardian's for minors) and
   honor it on the gallery, results videos and recap. The club gallery needs the same rule.
7. **Event hub launch.** `dmvt-event-hub` is built but not launched and has no roadmap: swap the
   email stub for a real provider, untrack `.env`, fix its `skills/` files (written for the map),
   point `events.dmvthrowers.club` at it, add it to the tables above, and decide whether it also
   becomes a template.
8. **Brand parity.** DMVT-Design is the brand contract, but nothing checks the live site and apps
   against it. Add a small check of colors, fonts and corner radius against DMVT-Design's tokens.
9. **Club calendar feed.** Meetups have no `.ics` or `webcal://` subscription on the live site or
   the club template (the contest app's feeds are planned separately). Generate one from the
   meetup rule.

## Fair and safe: the code of conduct everywhere (2026-10-07)

Goal: everyone is treated equitably and fairly, and every space we run (meetups, contests, the
map, the calendar, online) is a safe place to be. The contest app's part is P1–P9 in the
registration template's `docs/CONTEST_APP_MASTER_PLAN.md` (judge conflicts, published draws,
appeals, accommodations, fee waivers, youth safety). The rest:

- **A private way to report.** `code-of-conduct.html` asks people to email `contact@`, which goes to
  one inbox. Add a confidential report form (through the forms system, P2) that reaches a named
  conduct team of at least two people, skips anyone named in the report, and allows anonymous
  reports. Link it from every footer.
- **Name the conduct team and the steps.** Say who handles reports, how fast they respond, and what
  can happen (a conversation, a warning, a break from events, a ban), so the process is known
  before anyone needs it. Keep the version tag and effective date, and add a short changelog when
  the code changes.
- **At meetups:** a visible point of contact at every meetup (named on the events page and on site),
  and the code of conduct posted at the table.
- **Club and contest templates:** make the conduct team, report link, steps, version and effective
  date settings, so every club that copies the template starts with a complete code, not just an
  email address.
- **Troop and pack template:** a youth protection section (two-adult rule, links to the official
  training for each organization) as a setting.
- **Event hub and map:** submitters agree to the code of conduct; events and entries that break it
  are hidden; conduct reports go to the conduct team, not the general moderation queue.
- **Review it yearly** with the people it protects, and publish what changed (fits "open at every
  level").

## Features worth adding, from research (2026-10-07)

What comparable tools do that ours don't, per repo. Sources: [The Yoyo Archive](https://yoyoarchive.org/yya-events)
and its open dataset, [WCA Live and the WCA results export](https://www.worldcubeassociation.org/export/results),
[BCOE&M](https://github.com/geoffhumphrey/brewcompetitiononlineentry) (open-source competition entry
and judging), CompAdminPro, [Gancio and Mobilizon](https://docs.mobilizon.org/6.%20Fediverse/3.gancio/)
(community calendars), [OpenFreeMap](https://openfreemap.org/) and Open User Map, and troop-site
guidance from [TroopWebHost](https://www.troopwebhost.org/help.aspx?ID=397).

### Event hub (`dmvt-event-hub`)

- **Past events become an archive.** Keep every event page after it ends, with "Upcoming" and
  "Past" tabs and month navigation; link each past contest to its results, recap and photos.
  (Yoyo Archive)
- **Search.** One search box across events, venues and organizers. (Yoyo Archive)
- **Open data.** Publish the events as a dataset (JSON and CSV) under an open license in a public
  repo, alongside the `.ics` and RSS feeds. (Yoyo Archive, CC BY-SA)
- **Share instead of duplicate.** Offer our events and results to the Yoyo Archive's open dataset,
  and read theirs, rather than building a second archive of the same contests.
- **Federation and embeds.** An embeddable event list for club sites, and ActivityPub export so
  Gancio or Mobilizon calendars can follow ours. (Gancio, Mobilizon)

### Registration app (VA-States and the template)

Contest-specific; detailed as D1–D6 in the template's `docs/CONTEST_APP_MASTER_PLAN.md`.

- **Player career page** across seasons: every placement, linked from results. (Yoyo Archive
  player profiles, WCA person view)
- **Open results data:** each season's public results as JSON and CSV under an open license.
  (WCA export)
- **Psych sheet:** registered players with their past placements, for seeding, run order and the
  MC. (WCA Live)
- **Judge notes:** short written feedback attached to a player's score sheet. (BCOE&M scoresheets,
  CompAdminPro)
- **A documented contest data format** (divisions, rounds, entries, results) for moving a contest
  between deployments and tools. (WCA's WCIF)
- **Schedule conflict check:** warn when a player's divisions overlap. (CompAdminPro)

### Club site and `yoyoclub-template`

- **Site search** across the guides, as a static index with no tracking (for example Pagefind).
  (Yoyo Archive)
- **Loaner program page:** what loaners are, how to borrow one, and the rules. (Astronomy club
  sites)
- **News archive with RSS:** each month's recap as a post, so people can follow without social
  media.
- **Supporters page:** who helps keep the club free, alongside the open books (contest app O4).
  (Yoyo Archive supporters)
- **Events from the hub:** show the event hub's feed on the events page instead of hand-editing
  cards each month.

### Troop and pack sites (`Scouts-Template-Site`)

- **Photo permission and first names only** as template settings, with `check_site.py` flagging
  full names and photos without permission. (Troop-site guidelines)
- **Event sign-ups and electronic permission slips** need a server, so they belong in "forms on our
  own system" in the registration template, linked from the static site. (TroopWebHost)
- **Forms library:** the unit's permission, medical and registration forms in one place with dates.

### Player map and `yoyo-map-template`

- **Free vector tiles with no key or limits** (OpenFreeMap), for both maps.
- **Visibility per entry:** city, region, or hidden from the map but listed. (Member directories)
- **Clustering and search** in the simple template (already under Parity fixes).
- **Open counts, not people:** publish players per region as open data, never individual pins.

### Contest site (`yoyo-contest-template`)

- **Live results from the app:** when a registration app exists, the results page reads its public
  feed instead of being edited by hand.
- **A link to the season's open results data** (see the registration app above).

## Other club repos (tracked here)

### yoyo-player-map: dependency majors

Each is its own migration and PR. Eight major bumps are open: #250 (TypeScript 7) is green;
#254 (hookform resolvers 5), #249 (lucide-react 1) and #247 (workflow 5) fail typecheck or lint
(#247 also fails dependency review); #252, #253, #251 and #245 are unchecked. The `npm audit`
step fails on `main` too.


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
- **Season rollover (blocked on the archive and purge decisions):** purge and reset tooling for
  2026 → 2027, dry-run by default, requiring a recent backup and a merged archive. Reset covers the
  season bump, a music bucket name derived from the season (a constant today) and the 2027 round
  plan. First real archive run about a month after the event, reviewed in a site PR.
- **Sponsor extras (blocked on the sponsor questions):** logo upload, tier-prefilled
  deliverables, table add-on with a cap, CSV import of old JotForm submissions and the outreach
  directory as admin-only prospects, auto-deleting old dismissed inquiries, invoice tracking.
  Sponsors stay admin-only in VA-States until the roles system is ported (separate project).
- **Hub and template:** finance and budget upgrade; organization and event IDs (hub stage 1);
  port battles, round plans, disputes, split, champion (the template still has the older rule),
  prizes and score status from VA-States; drop `contest_staff_accounts.role` once migrations 0044
  and 0045 are everywhere; a shared pattern for other public forms (vendor and merch tables,
  volunteers) built on the sponsor form.
- **Deferred majors** on both: ESLint 10, `resend` 6, `@vercel/analytics` 2, `zod` 4. Replace
  `@vercel/kv` with `@upstash/redis` the next time rate limiting is touched.
- Contest app features (formats, contest-day tools, spectator pages): see the registration
  template's `docs/CONTEST_APP_PLAN.md`, with its sources `CONTEST_APP_MASTER_PLAN.md` and
  `FORMAT_RESEARCH.md`, linked from `docs/HUB_ROADMAP.md`.
