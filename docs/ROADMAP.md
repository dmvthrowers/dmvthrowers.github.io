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
6. **Guide part numbering.** Part intros say "Part N of 4", but body section headings keep the
   old global numbers (e.g. maintenance is "Part 2 of 4" with sections "PART 4–9"). Renumber the
   body headings per part, or drop the numbers.
7. **Guides aren't in the main nav.** The largest content (learn-yoyo, yoyo-gear, history,
   science, collecting) is reachable only through inline links. Adding a nav item means editing
   every page's nav identically — plan it as one change across all pages.
8. **`/.well-known/security.txt`** with a contact address.
9. **Cold-load flash on `vsyc26.html`**: hero title briefly renders in fallback fonts and the nav
    logo shows a broken-image glyph. Check font-display and the logo's `width`/`height`.
10. **JotForm leftovers.** `privacy.html` still lists JotForm as a registration processor (update
   once no live JotForm forms remain; owner confirms wording). 16 pages (`about.html`,
   `index.html`, `teachers.html`, the guides) carry stale "jotform for VSYC-26" CSP comments.
   `AGENTS.md` still describes a JotForm embed on `vsyc26-sponsors.html`. One small PR.
11. **Status page link in the footers**, not only on the contact page. Touches every footer, so
    plan it as one change across all pages.

## Later

- Shared nav/footer styles drift between `main.css` and `vsyc26.css`; a small shared stylesheet
  would cut per-page edits without adding a build step.
- Security headers: GitHub Pages can't send HSTS/CSP headers; per-page CSP `<meta>` tags are the
  enforcement. Putting Cloudflare (free) in front would add real headers.
- Sitemap check in CI so a new page can't ship without a `sitemap.xml` entry.

- **Raw hex colors** remain in page `<style>` blocks. Convert them to `--red`, `--navy`, `--cream`
  and `--border`.

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
