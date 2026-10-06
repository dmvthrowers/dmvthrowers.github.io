# DMV Throwers — how the repos fit together

The map of the territory for a volunteer developer. Each repo has its own `AGENTS.md` /
`CLAUDE.md` with day-to-day rules — read those before touching code. Last checked 2026-10-02,
after the October 2026 technical audit.

## The repos

| Repo | What it is | Live at | Start with |
|---|---|---|---|
| `dmvthrowers/dmvthrowers.github.io` (this one) | Static club website: meetups, guides, VSYC contest pages. No build step | dmvthrowers.club (GitHub Pages) | `CLAUDE.md`, `docs/ROADMAP.md` |
| `dmvthrowers/yoyo-player-map` | Public player/club/shop map. No login; email-verified; person pins jittered ~10 mi | map.dmvthrowers.club (Vercel) | `docs/REPO_GUIDE.md`, `docs/ROADMAP.md` |
| `dmvthrowers/VA-States` | Contest registration, Stripe payments, day-of ops (run order, scoring, music). **The money app** | register.dmvthrowers.club (Vercel) | `docs/REPO_GUIDE.md`, `docs/ROADMAP.md` |
| `dmvthrowers/dmvt-event-hub` | Community event calendar (React + Vite + Supabase, Lovable-built). **Not launched** | — (target events.dmvthrowers.club) | its `AGENTS.md` |
| `dmvthrowers/DMVT-Design` | Brand and design-system reference + a Claude skill. Not an app | — | its `README.md` |
| `dmvthrowers/yoyoclub-template` | Public template other clubs copy: this site's club pages as a `site.jsonc` + Python builder. Meetup dates generated from a rule | dmvthrowers.club/yoyoclub-template (showcase) | its `AGENTS.md` |
| `dmvthrowers/yoyo-contest-template` | Public template for contests, built from the VSYC-26 pages. Stages (registration, contest day, wrap) switch by date | dmvthrowers.club/yoyo-contest-template (showcase) | its `AGENTS.md` |
| `dmvthrowers/Scouts-Template-Site` | Sister template for Scout units and kids clubs; same engine | dmvthrowers.club/Scouts-Template-Site (showcase) | its `AGENTS.md` |

How they relate: the site is the front door and links out to registration (VA-States) and the
map. VA-States and the map are separate Next.js + Supabase apps that share patterns (structured
API errors with request ids, Upstash rate limiting, Resend email with a queue, audit logs,
Sentry) but **not** databases. DMVT-Design is the brand contract: brand changes land there first,
then get applied to the apps — don't copy brand rules into app repos, link to it.

`github.com/dmvthrowers` is a user account, not an organization: there are no teams or roles,
and all access runs through that one account.

## Shared services

| Service | Used by | Notes |
|---|---|---|
| GitHub Pages | site | Custom domain via `CNAME` (never edit it) |
| Vercel (team `dmvthrowers-projects`, free tier) | map, VA-States | Main-only deploys, previews off. Watch the 10 GB deployment-storage cap — it was at or near 100% on Oct 1 |
| Supabase | map, VA-States (separate projects); event-hub (Lovable Cloud, pre-launch) | Postgres + RLS + Auth + Storage |
| Stripe | VA-States | Checkout + webhooks |
| Resend | VA-States, map | Free tier is 100 emails/day **per account, shared** — both apps budget for it |
| Upstash (Redis, QStash) | VA-States, map | Rate limiting; QStash backstop for email drains |
| Cloudflare Turnstile | map | Bot check on submit/report |
| Sentry, Healthchecks.io | VA-States, map | Errors and job check-ins; both off when unset |
| UptimeRobot (free) | site, map, VA-States | Public status page at https://stats.uptimerobot.com/7XjeeDhuSq, linked from the contact page. Monitors: the site root, two troop pages, `map.dmvthrowers.club`, `register.dmvthrowers.club/`. Add a monitor for `register.dmvthrowers.club/api/health` so a database or app failure shows up |
| Formspree, JotForm | site | Contact form; sponsor-interest form (JotForm slated for replacement, issue #77) |
| Porkbun | all | Registrar, DNS, email forwarding |

## Cross-repo plan (from the audit)

**Owner actions — dashboards, not code**

1. Rotate the map's Supabase `service_role` key if it wasn't rotated after it sat in the map
   repo's public git history (May 4–13, 2026). Then check Supabase logs since May 4.
2. Turn on secret scanning + push protection on every repo (Settings → Code security; free for
   public repos). It would have blocked that leak.
3. Branch protection on `main` everywhere: PR required, CI must pass.
4. Confirm MFA on GitHub, Vercel, Supabase, Stripe, Porkbun, Resend, Upstash and the Google
   accounts.
5. Close VSYC-26 registration in the VA-States app (the `online_registration_open` event flag) —
   it still accepts submissions after the event.
6. Vercel storage: delete stale deployments and set retention (7 days pre-production/errored,
   30 days production).
7. Email: DMARC is `p=none` with no reporting. Once senders are inventoried, move to
   `p=quarantine` with a `rua=` address.

**Code — tracked in each repo's `docs/ROADMAP.md`.** The big ones: Stripe dispute handling and
per-division music tracks (VA-States), error envelopes and hreflang (map), the JotForm
replacement and a link checker (site), and the event hub's pre-launch gates (real email delivery
verified end to end, one lockfile, one deploy target, a working Dependabot config).

## Where the audit itself lives

The full October 2026 audit — security assessment, threat model, incident-response and
disaster-recovery runbooks, asset inventory, discoverability report, repo specs — is in the
club's Google Drive:
**[Technical docs - Oct 2026](https://drive.google.com/drive/folders/1Jt7amThKNkeVJenksPtA87cBtR-nwZiq)**
(access-restricted; ask the coordinator for access). It stays out of these public repos because
parts of it describe accounts and credentials. The repo docs above carry the actionable,
non-sensitive parts.

| Drive subfolder | What's in it |
|---|---|
| `repo-docs/` | Per-repo structure guides (the source for each repo's `docs/REPO_GUIDE.md`) |
| `repo-specs/` | Task specs for each repo, including the `/ideas` board spec |
| `deep-dive/`, `audit-2/` | Sep 30 security/dependency review and the Oct 1 fix verification |
| `security/nist-800-171/` | NIST 800-171 gap assessment, risk register, runbooks, policies |
| `discoverability-audit/` | Search ranking, technical SEO and reputation report |
