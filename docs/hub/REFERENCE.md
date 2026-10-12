# Organizer Hub — Build Reference

Oct 12, 2026 · The facts a builder needs before touching any hub feature: where things live, what already exists to reuse, how each repo is checked, and the house rules. Pairs with [`SPEC.md`](SPEC.md) (what and why) and [`BUILD_PLAN.md`](BUILD_PLAN.md) (order and gates). Checked against each repo's `main` on Oct 12, 2026; when this page and the code disagree, the code wins.

## Repos and where hub work lands

| Repo | Stack | Live at | Hub work that lands here |
| --- | --- | --- | --- |
| `dmvthrowers.github.io` | Static HTML/CSS, no build step, GitHub Pages | dmvthrowers.club | Lane A: front door, kits, seed retros, governance pack; meetup booking gate; this plan |
| `yoyo-registration-template` | Next.js 16, Supabase, Stripe, Resend, Upstash | Template (Deploy with Vercel) | Lane B first: fulfillment ledger, recap generator, volunteer shifts, score overlay |
| `VA-States` | Same as the template | register.dmvthrowers.club | Lane B second: each template change ported here |
| `dmvt-event-hub` | React 18 + Vite + shadcn/ui on Lovable Cloud (Supabase); moving to Cloudflare Pages + Workers + D1 | Not launched (target events.dmvthrowers.club) | Lane C: Phase 1 rebuild, then the Exchange |
| `yoyo-player-map` | Next.js 16, Supabase, Leaflet | map.dmvthrowers.club | Cross-links only for now |
| `DMVT-Design` | CSS tokens, brand books | — | Brand source for every new surface |
| `yoyoclub-template`, `yoyo-contest-template`, `yoyo-map-template`, `Scouts-Template-Site` | Static, one `site.jsonc`, Python builder | Showcases under dmvthrowers.club | Front door links; kits point people here |

## How work flows

- **Spec first.** No implementation PR without an approved spec section ([`specs/`](specs/)).
- **Branches and PRs.** Claude Code opens PRs from `claude/*` branches; Brandon merges. One item, one PR, one repo.
- **Template first, then live.** New app features land in `yoyo-registration-template`, then port to VA-States. Every PR states its parity line ("ports to …", "logged as a gap", or "live-only"), per the template's `docs/PARITY.md`.
- **Commit prefixes** on the site: `feat(events):`, `fix(vsyc26):`, `chore(assets):`, `docs:`.
- **Agent orientation.** Every repo has `AGENTS.md` and `CLAUDE.md`. Read them before code.

## Checks per repo

Run these before every push; CI runs them too.

| Repo | Local checks | CI on PRs |
| --- | --- | --- |
| dmvthrowers.github.io | `python3 scripts/check_site.py` (links, alt text, nav and footer drift) | Site check, W3C HTML validator, axe (report-only), CodeQL, dependency review |
| yoyo-registration-template, VA-States | `npm run typecheck`, `npm run lint`, `npm test`, `npm run build` | Same four, in that order |
| yoyo-player-map | `pnpm typecheck`, `pnpm lint`, `pnpm test`, `pnpm i18n:parity --strict`, `pnpm build` (in `yoyomap/`, `--ignore-workspace`) | Same, plus migrations, backups, OSV |
| dmvt-event-hub (today) | `bun run lint`, `bun run test`, `bun run build` | Dependabot only |

The `github-advanced-security` check has been red on every PR since a Copilot quota error (HTTP 402); it is not a code problem.

## Reuse before you build (registration template `lib/`)

| Need | Use | Notes |
| --- | --- | --- |
| API error envelope with request id | `apiError`, `withErrorHandling`, `newRequestId` (`lib/api-error.ts`) | Every route returns this shape |
| Rate limit | `checkRateLimit`, `getClientIp` (`lib/rate-limit.ts`) | Upstash; fails open if KV is down |
| Bot check | `verifyTurnstile` (`lib/turnstile.ts`) | Same keys as the map |
| Audit log | `logAudit` (`lib/audit.ts`) | Log every admin change |
| Email | `queueEmail`, `enqueueEmails`, `drainOutbox` (`lib/outbox.ts`); templates in `lib/email.ts` | Outbox table, never send inline. Resend free tier: 100/day shared across apps |
| Signed background jobs | `isSignedByQstash` (`lib/qstash.ts`) | Worker routes verify the signature |
| Auth and roles | `lib/auth/admin-request.ts`, `lib/auth/staff.ts`, capabilities in `lib/roles.ts` | Capabilities are `area.action` strings; check on every route, not only in menus |
| Supabase clients | `lib/supabase/admin.ts` (service role), `lib/supabase/client.ts` | Service role only on the server |
| Sponsors | `lib/sponsors.ts` (`SPONSOR_STATUSES`, `Deliverable`, `summarizeSponsors`, `cleanDeliverables`), `lib/sponsors-server.ts`, `lib/sponsor-inquiry.ts`, `lib/sponsor-availability.ts`, `lib/sponsor-settings.ts` | Statuses: prospect, contacted, committed, paid, declined |
| Surveys | `lib/surveys.ts` (`SURVEYS`, `SURVEY_TYPES`, `validateSurveyAnswers`) | Types: competitor, winner, spectator, volunteer, vendor, sponsor |
| Results | `lib/standings.ts` (`computeStandings`, `winnersFrom`, `publicEntry`) | Public-name rules for minors live here |
| Season archive | `lib/season-archive.ts` (`buildArchiveData`), `npm run archive`, `npm run archive:verify` | Writes `archive/<season>/results.json` + static pages |
| Budget and open books | `lib/budget.ts`, `lib/open-books.ts` | |
| Volunteers | `lib/volunteer-roles.ts`, `lib/volunteer-availability.ts` | Shift scheduling (T8) not built |
| Calendar file | `lib/ics.ts` | |
| Feature modules | `lib/modules.ts`, `lib/modules-server.ts` | Turn features on per deployment |

## Data shapes worth knowing

**`contest_sponsors`** (migration 0046): `name`, `tier`, `status`, `amount_cents`, `in_kind`, `contact_name`, `contact_email`, `notes`, `deliverables jsonb` (array of `{label, done}`, max 20, added by hand), `auth_user_id`. Service-role RLS only. Inquiries: `contest_sponsor_inquiries` (0048); form settings: `contest_sponsor_form` (0049).

**`contest_survey_responses`**: `survey_type`, `answers jsonb`, `contact_name`, `contact_email`, `quote_text`, plus hardening (0029) and contacts (0030).

**`results.json`** (season archive): `{ season, contest, shortName, dateAndPlace, generatedAt, divisions: [{ code, name, format, rounds: [{ name, rows }], final: [ArchiveRow] }] }`, where `ArchiveRow = { place, name, city, state, result, detail?, champion? }`. Names already follow the minor rules. **No stable player id**: cross-contest matching (the circuit) needs one.

**Event hub (Supabase, today):** 12 tables (`events`, `event_occurrences`, `submitters`, `verification_tokens`, `manage_tokens`, `renew_tokens`, `reports`, `user_roles`, `profiles`, `audit_log`, `feed_subscriptions`, `feed_manage_tokens`), SQL functions `has_role`, `validate_event`, `bootstrap_first_admin`, `handle_new_user`, `set_updated_at`, 13 migrations, and edge functions `submit-event`, `verify-event`, `manage-event`, `renew-event`, `report-event`, `geocode`, `feeds`, `feed-subscribe`, `manage-feed-subscription`, `sitemap`, `service-status`, `admin-action`, `daily-maintenance` (+ `_shared`). Five functions already send mail through Resend (`_shared/email.ts`, `sendMail`, needs `RESEND_API_KEY`); `email-stub.ts` is leftover and the repo README still describes the stub.

## Site facts for Lane A

- Pages are hand-built HTML; copy `about.html` for a new page and follow `CLAUDE.md` ("How to add a new main-site page").
- New guides get a card on `guides.html` (the GUIDES nav item). Adding a nav item means editing every page identically.
- Existing kit files in `assets/documents/`: `event-checklist.docx` (shown as "Event Planning Kit"), `workshop-run-sheet.docx`, `beginner-trick-checklist.pdf`, `trick-reference-guide.pptx`, `maintenance-guide.pptx`, `club-display-loop.pptx`, `DMV Throwers Charter v5.docx`, `DMV Throwers Officer Roles.docx`, `DMV Throwers Press Kit.pdf`.
- `scripts/update_meetup.py` runs weekly (`.github/workflows/update-meetup.yml`): NEXT MEET bar, past cards removed, JSON-LD, sitemap `lastmod`, and `meetups.ics` with the next 12 meetups. It has no booking check (spec 00).
- Images under 500 KB, WebP with fallback, `width`/`height` set, alt text required. Relative, root-based links (`<base href="/">`). Never edit `CNAME`.

## Brand (DMVT-Design `colors_and_type.css`)

| Token | Value | Use |
| --- | --- | --- |
| `--color-red` | `#B80000` | Canonical red |
| `--color-navy` | `#102040` | Primary dark |
| `--color-cream` | `#fffdfa` | Main background |
| `--color-gold` | `#C9A84C` | VSYC accent only |
| `--color-text-body` | `#1a2744` | Body text |
| `--color-border` | `#b0a890` | Hairlines |

Playfair Display (display), DM Sans (body), Montserrat (VSYC only), all self-hosted. `border-radius: 0` and no card shadows. Nav ALL CAPS, headings Title Case, body sentence case, second person. No emoji except ☕ on donate. On the site use `main.css` variables (`--red`, `--navy`, `--cream`, `--border`), not raw hex.

## Shared services and limits

| Service | Used by | Limit to watch |
| --- | --- | --- |
| GitHub Pages | Site | No real headers; CSP is per-page `<meta>` |
| Vercel (free) | Map, VA-States | 10 GB deployment storage; free plan is non-commercial |
| Supabase (free) | Map, VA-States, event hub (until Phase 1) | Idle projects pause; DB and storage caps. Management API access needs a fresh personal access token |
| Cloudflare | Event hub (Phase 1), Turnstile | Needs a token with Workers Scripts Edit |
| Resend | VA-States, map; event hub gets its own key | 100 emails/day per account, shared |
| Upstash Redis / QStash | VA-States, map | Free-tier request caps |
| Stripe | VA-States | Webhooks reconcile payments; refunds and disputes handled |
| Sentry, Healthchecks.io, UptimeRobot | Apps, site | Off when unset |

## Privacy rules that bind every build

- Minors: public names are nickname or first name + last initial unless opted in (`lib/standings.ts`, `lib/display-name.ts`).
- Map: people at city level only, jittered about 10 miles.
- Nothing stores a child's account; check-ins collect no personal data (spec §1, proposed).
- Contact emails never leave admin views; public endpoints never return them.
