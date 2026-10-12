# Spec 05: Event Hub on Cloudflare (Hub Phase 1)

**Status:** Draft, needs Brandon's approval · **Repo:** dmvt-event-hub · **Lane / phase:** C / 1 · **Fall build:** 1 · **BUILD_PLAN:** 7.1 / 10.10 · **Size:** 2–3 weekends · **Blocked on:** a Cloudflare API token with Workers Scripts Edit

## Problem

The event calendar was built on Lovable Cloud (Supabase). Lovable's free tier kept going dormant, so the hub is paused and was never launched. Decided Oct 11, 2026: move it to Cloudflare Pages + Workers + D1 with its own Resend key, built so it doubles as the hub's reference architecture and the base for the Exchange (Phase 2).

## What exists today

- **Front end:** React 18 + Vite + Tailwind + shadcn/ui, React Router. Pages: Home, Events, EventDetail, SubmitEvent, SubmitThanks, Verify, Manage, Renew, ReportEvent, Subscribe, FeedsManage, Status, admin. Calls Supabase directly and through edge functions.
- **Database:** 12 tables with RLS — `events`, `event_occurrences`, `submitters`, `verification_tokens`, `manage_tokens`, `renew_tokens`, `reports`, `user_roles`, `profiles`, `audit_log`, `feed_subscriptions`, `feed_manage_tokens`. SQL functions `has_role`, `validate_event`, `bootstrap_first_admin`, `handle_new_user`, `set_updated_at`. 13 migrations.
- **Edge functions (13):** `submit-event`, `verify-event`, `manage-event`, `renew-event`, `report-event`, `geocode`, `feeds`, `feed-subscribe`, `manage-feed-subscription`, `sitemap`, `service-status`, `admin-action`, `daily-maintenance`. Shared: `audit`, `cors`, `email` (Resend via `sendMail`), `rate-limit`, `site-url`, `tokens`, `validate`. `email-stub.ts` is leftover; the README still describes the stub.
- **Jobs:** `daily-maintenance` via pg_cron at 09:00 UTC (re-materialize recurring occurrences, 14-day renewal reminders, hide expired events).
- **Auth:** Supabase Auth for admins; submitters use emailed tokens, no accounts.

## Target architecture

| Today (Supabase) | Cloudflare | Notes |
| --- | --- | --- |
| Postgres tables + RLS | D1 (SQLite) | RLS doesn't exist in D1: every access check moves into Worker code. One module, `auth.ts`, owns them |
| `has_role`, `validate_event` SQL functions | TypeScript in the Worker | Port `validate_event` rules exactly; test them |
| Edge functions | One Worker with routes (`/api/...`) on Pages Functions | Same paths where possible so the front end changes little |
| pg_cron | Cron Trigger on the Worker | `0 9 * * *` |
| Supabase Auth (admins) | Magic-link email to an allow-listed admin, signed session cookie (HttpOnly, Secure, SameSite=Lax) | Few admins; no password store. Cloudflare Access is the zero-code alternative |
| `rate-limit.ts` | Workers rate limiting binding, or a D1 counter table | Keep per-IP limits on submit, report and subscribe |
| Turnstile (not used yet) | Turnstile on submit and report | Same keys as the map |
| Resend via `sendMail` | Same module, Workers `fetch` | Separate Resend key for isolation |
| Nominatim geocode with caching | Same, cached in D1 | Respect Nominatim's usage policy (one request per second, a real User-Agent) |
| `feeds`, `sitemap` | Worker routes with Cache API | iCal and JSON feeds are the hub's public contract (BUILD_PLAN 7.3) |

**Data types:** `uuid` → `TEXT` (generate with `crypto.randomUUID()`); `timestamptz` → ISO 8601 `TEXT` in UTC; `jsonb` → `TEXT` with JSON functions; enums and checks → `CHECK` constraints in D1 schema. Migrations live in `migrations/` and run with `wrangler d1 migrations apply`.

**Repo layout:** keep the Vite app; add `functions/` (Pages Functions) or `worker/`, `wrangler.jsonc`, `migrations/`. Remove `supabase/` only after cutover. Untrack `.env`, fix `skills/` (BUILD_PLAN 7.1), and add `security.txt` (9.31).

## Cutover

1. Build and test against a local D1 (`wrangler dev`). 2. Deploy to a `*.pages.dev` preview with Turnstile test keys. 3. Export any real events from Supabase (CSV), import to D1. 4. Point `events.dmvthrowers.club` DNS at Pages. 5. Keep the Supabase project paused, not deleted, for 30 days.

## Acceptance criteria

- [ ] Submit → verification email arrives (real Resend key) → verify publishes the event → manage link edits it → renew link extends it.
- [ ] Recurring events materialize occurrences; the cron run sends a 14-day renewal reminder and hides expired events (tested with a fake clock).
- [ ] Report flow, feed subscribe and manage, iCal and JSON feeds, sitemap and status page all work on the preview URL.
- [ ] Every rule `validate_event` enforced in SQL is enforced in the Worker, with tests.
- [ ] Non-admins can't reach any admin route; checked by route tests, not just hidden menus.
- [ ] Rate limits and Turnstile active on submit, report and subscribe.
- [ ] Deploy steps documented as the reference architecture (`docs/DEPLOY.md`): one `wrangler` command per resource, every secret named, free-tier limits listed.
- [ ] `bun run lint`, `test`, `build` pass; CI added for the same.

## Open questions for Brandon

- Admin sign-in: magic link in the Worker, or Cloudflare Access (no code, Google login)?
- Any real submitted events in Supabase worth migrating, or start clean?
- Keep the Lovable editor in the loop, or is the repo now hand-maintained only?

## Claude Code handoff

```
Repo: dmvt-event-hub. Read AGENTS.md, README.md and
docs/hub/specs/05-event-hub-cloudflare.md (in dmvthrowers.github.io). Do not start
until Brandon confirms the Cloudflare token works. Phase the work as separate PRs:
(1) D1 schema + migrations translated from supabase/migrations, with validate_event
rules ported and tested; (2) Worker routes for submit/verify/manage/renew/report with
sendMail, rate limits and Turnstile; (3) feeds, sitemap, status, geocode with caching;
(4) cron trigger for daily maintenance; (5) admin auth and admin-action; (6) front-end
switch from Supabase client to /api routes; (7) DEPLOY.md and CI. Each PR: lint,
test, build green, branch claude/hub-cf-<step>.
```
