# Security plan: encryption and zero trust

How we secure every club repo and app to an enterprise standard on a free, open-source budget.
This file is the *what* and *why*. The *when* is Wave 9 in [`BUILD_PLAN.md`](BUILD_PLAN.md).
Written 2026-10-11 from a review of all 13 repos.

None of our apps is high-criticality. Some hold sensitive data anyway: minors' names, guardian
and emergency contacts, home addresses, payment records and players' emails. Build for that
data, not for the size of the club.

## Principles

1. **Never trust the network. Check every request.** Every request proves who sent it (a
   signed-in person, a signed webhook or a scoped key) and what it may do. Being "inside" earns
   no trust.
2. **Named people, not shared passwords.** Every human gets their own account. Nobody shares a
   login, and no admin password sits in a header.
3. **Phishing-resistant MFA on everything that matters.** Use passkeys or security keys first,
   then TOTP apps. Use SMS only if nothing else works.
4. **Least privilege, short-lived.** Give each key and role only what its job needs, and take it
   away when the job ends. That covers contest-day staff, restricted Stripe keys and CI tokens.
5. **Encrypt in transit everywhere.** Use TLS on every hop, HSTS on every domain, and TLS-only
   database connections. Sign the email we send.
6. **Encrypt at rest, twice for the worst data.** Platform disk encryption covers everything.
   The most sensitive fields also get app-level encryption, so a leaked database login, a SQL
   editor screen or a backup doesn't expose them.
7. **Collect less.** Data we never store can't leak. This beats every other control.
8. **Assume breach.** Keep audit logs, encrypted backups, tested restores, a rotation calendar
   and a one-page incident runbook.
9. **Trust the supply chain only after checking it.** Pin every action to a commit SHA, give
   workflows the fewest permissions, review dependencies and scan for secrets.
10. **Free and open source first.** When something costs money, say so, then skip it or build
    around it (see [Costs](#costs-what-we-skip-or-build-around)).

## What's already good

Credit where it's due. The review found a lot already in place:

- **Registration app (VA-States and template):** CSP, HSTS with preload, `frame-ancestors 'none'`
  and COOP headers. Row-level security on every table, with anon table access revoked
  (migration 0032). Portal tokens are stored as SHA-256 hashes, and secrets are compared in
  constant time. Stripe webhook signatures are checked. Admin routes have per-IP rate limits.
  Roles and capabilities are checked on the server. Sentry sends stack traces only, with no user
  data. Nightly backups are encrypted with `age`. Turnstile is ready.
- **Player map:** full security headers. The admin password fails closed when it's weak and is
  compared in constant time. Person pins are city-level and jittered. Backups are encrypted with
  `age`.
- **Event hub:** headers in `vercel.json`. RLS cleanup, token hashing in the audit log and a
  GraphQL lockdown (May 2026 migrations). The admin function checks the JWT and the admin role on
  the server.
- **Club site and static templates:** a CSP on every page, no third-party scripts, `security.txt`,
  pinned actions on the site, Dependabot and a `SECURITY.md` almost everywhere.
- **Secrets hygiene:** the review scanned the event hub's tracked `.env` and its history, and the
  tracked `.vs/` editor caches in three repos. Only public values turned up (anon and publishable
  keys, a database hostname). No service-role key, JWT secret or password was ever committed.

## What we hold, and where

| Tier | Data | Lives in | Who should read it |
|---|---|---|---|
| **High** | Minors' details, guardian and emergency contacts, home addresses, waivers, payment records | VA-States (Supabase), its backups, any CSV export | Admins; finance for payments; nobody else by default |
| **Medium** | Player and organizer emails, staff accounts, sponsor contacts, conduct reports (planned) | VA-States, map, event hub, Formspree | Admins; the conduct team for reports |
| **Low** | Public pins (city-level), public events, results, the brand | Map, event hub, static sites | Everyone |
| **Future high** | Parent and youth records for a troop or pack | `scouts-private` (empty today) | Designed before it's built (see below) |

Item 9.33 turns this table into a full data inventory, with each field, its retention and its
readers.

## Encryption in transit

| Hop | Today | Plan |
|---|---|---|
| Browser → `dmvthrowers.club` (GitHub Pages) | HTTPS with a Let's Encrypt certificate. GitHub Pages can't send HSTS or real headers | Check that "Enforce HTTPS" is on. Decide on free Cloudflare in front for HSTS and real headers (9.12), then add the apex to the HSTS preload list |
| Browser → `register.` / `map.` / `events.` (Vercel) | TLS, with `Strict-Transport-Security: …; includeSubDomains; preload` | Preload only takes effect once the apex sends it too (9.12) |
| App → Supabase API | HTTPS through `supabase-js` | No change |
| Backups and scripts → Postgres | Direct database connection | Turn on **Enforce SSL** in each Supabase project and connect with `sslmode=require` (9.07) |
| Our email out (Resend) | TLS when the receiving server offers it | SPF, DKIM and DMARC aligned. Move DMARC from `none` → `quarantine` → `reject` after 30 days of clean reports (9.06) |
| Email in (`contact@`) | Whatever the mail host does | MTA-STS and TLS-RPT. The policy file can sit on GitHub Pages for free (9.06) |
| DNS (Porkbun) | Unsigned | DNSSEC plus CAA records that list only the certificate authorities we use (9.05) |
| Webhooks and crons | Stripe signature check, `CRON_SECRET` compared in constant time | Keep. Every new webhook verifies a signature before it reads the body |

## Encryption at rest

| Store | Today | Plan |
|---|---|---|
| Supabase databases (VA-States, map, hub) | AES-256 disk encryption by Supabase | Add field-level encryption for High-tier columns (9.27, below). Keep database-side secrets in Supabase Vault (already used for the cron secret) |
| Nightly backups | `age`-encrypted dumps for VA-States, the template and the map, kept 30 days as workflow artifacts | Add a backup for the event hub (9.30). The encryption is what makes artifacts safe: on a public repo anyone with read access can download them. Guard the private key (9.10) |
| Vercel environment variables | Encrypted by Vercel | Mark every secret **Sensitive**, so nobody can read it back, including us (9.09) |
| GitHub Actions secrets | Encrypted | Move `SUPABASE_DB_URL` into a `backup` environment that only `main` can use (9.20) |
| Laptops and phones | Unknown | Full-disk encryption (FileVault, BitLocker or LUKS) and a screen lock on any device that holds repo access, a dump or an export (9.11) |
| CSV exports and Google Drive | Ad hoc | Export only the columns you need, delete exports after the event, and use restricted sharing. Never put High-tier data in a shared Drive folder |

### Field-level encryption (High-tier columns)

Supabase already encrypts the disk. That doesn't help when someone gets the service key, opens
the SQL editor, or gets a backup together with its key. For the worst data, add a second layer:

- **What:** guardian phone and email, emergency contact name, phone and relationship, and home
  address. Login emails stay plain, because Supabase Auth needs them.
- **How:** AES-256-GCM with Web Crypto in server routes only. The key (`PII_ENCRYPTION_KEY`,
  32 random bytes) is a Sensitive Vercel variable. Each row stores `ciphertext`, `iv` and
  `key_id`, so keys can rotate. If we need to look a value up, an HMAC "blind index" column
  makes it searchable without decrypting.
- **Who reads it:** only routes that hold a new `registrations.contact` capability. Each decrypt
  writes an audit-log row.
- **Migration:** expand and contract, as the repo already does it. Add the new columns, backfill
  with a script, switch reads over, take a verified backup, then drop the plain columns. Spec and
  build it in the template first, then port it to VA-States.
- **Trade-off:** the SQL editor shows ciphertext for these columns, which is the point.
  Day-of lookups go through the app.
- **Shrink it first:** the 4.4 and 4.1 decisions (anonymize after the archive; collect the home
  address only when a contest uses a state champion rule) cut how much of this data exists at all.

## Zero trust: identity and access

### People and accounts (owner actions, all free)

- **Phishing-resistant MFA everywhere.** Use passkeys or security keys, and store recovery codes
  offline. This covers GitHub, Google (`contact@`, `dmvthrowers@gmail.com`), Vercel, Supabase,
  Stripe, Porkbun, Resend, Formspree, Sentry, UptimeRobot, Upstash and Cloudflare (9.01).
- **A password manager with a shared vault.** Bitwarden is open source, and its free
  organization covers two people. Vaultwarden is the self-hosted option. This is also the fix
  for the bus factor (Gap 1): the second owner gets the vault, not a sticky note (9.02).
- **The GitHub organization requires 2FA** once the repos move there (Gap 1).
- **Fine-grained tokens with expiry dates.** No classic personal access tokens. List every token
  in the vault with its owner and expiry.
- **Access review after each contest and once a year.** Who has which account? Remove anyone who
  no longer needs it, and rotate on the calendar below (9.13).

### People inside the apps

| App | Today | Plan |
|---|---|---|
| VA-States and template | Supabase email and password for staff. Roles and capabilities checked on the server | **TOTP MFA (free in Supabase Auth).** Required for admin and finance, checked on the server (`aal2`) in `getStaffIdentityFromToken`. Optional for judges and DJs on shared contest-day tablets, whose accounts are short-lived anyway. A second admin resets a lost factor (9.25) |
| Player map | **One shared `ADMIN_PASSWORD`**, sent as `x-admin-token` from the browser on every admin call. No identity, no per-person audit trail, no MFA | Named Supabase Auth admin accounts with TOTP, an `admins` role table, and the audit log recording *who* did it. Then delete `ADMIN_PASSWORD` (9.29). This is the biggest zero-trust gap in the review |
| Event hub | Email and password or OAuth, with the admin role checked in `admin-action` | Admin TOTP before launch (9.30) |
| `scouts-private` | Not built | Invite-only accounts, passkeys or TOTP for leaders, RLS per family and per den (9.34) |

Shorten the Supabase JWT expiry for staff sessions (free setting). Supabase's time-boxed and
idle session limits are a paid feature, and short JWTs plus MFA cover most of the same ground.

### Services talking to services

- **Supabase:** move from the legacy `service_role` JWT to the newer `sb_secret_…` keys. They can
  be rotated one at a time without touching the JWT secret. Revoke the legacy key afterwards
  (9.07). The service key stays in server routes only, as it does today.
- **Stripe:** a **restricted key** with only the resources the app touches (Checkout, refunds,
  disputes read) instead of the full secret key (9.08).
- **Resend:** a sending-only key, scoped to the one domain (9.08).
- **Event hub edge functions:** all nine run with `verify_jwt = false` and send
  `Access-Control-Allow-Origin: *`. That's fine for the public feeds, but each mutating function
  then has to check the caller itself. Turn `verify_jwt` on for anything that needs a user, and
  limit CORS on mutating functions to `events.dmvthrowers.club` (plus localhost in dev) (9.30).
- **Rate limits:** two staff guards in the registration app (`requireRunOrderEditorRequest` and
  `requireScoreReviewRequest`) skip the per-IP limit the others apply (9.28).

## Supply chain and CI

| Repo | Unpinned actions | Workflows with no `permissions:` | Other |
|---|---|---|---|
| dmvthrowers.github.io | 1 (`actions/setup-example@v1`, a template placeholder) | 5 | `powershell.yml`, `codeql1.yml`, `super-linter.yml` and `summary.yml` are starter boilerplate an HTML site doesn't need |
| DMVT-Design | 13 | 5 | No Dependabot, no `SECURITY.md`, 345 tracked `.vs/` files, a stray `.zip` of uploads |
| dmvt-event-hub | 10 | 4 | `.env` tracked, 66 tracked `.vs/` files |
| yoyo-player-map | 9 | 3 | 66 tracked `.vs/` files |
| VA-States | 4 | 0 | No `SECURITY.md` (the template has one) |
| yoyo-registration-template | 4 | 0 | — |
| Static templates, troop, pack | 0 | 0 | Good |
| scouts-private | — | — | No CI at all. It's a private repo, so GitHub's free secret scanning doesn't cover it |

The plan for every repo (9.20–9.22):

- Pin every `uses:` to a full commit SHA with a version comment. Dependabot's `github-actions`
  ecosystem keeps them current.
- Set `permissions: contents: read` at the top of every workflow. Grant writes per job, only where
  needed.
- Delete starter workflows that do nothing for the repo.
- Run [zizmor](https://github.com/zizmorcore/zizmor) (workflow linter, MIT) and
  [gitleaks](https://github.com/gitleaks/gitleaks) (secret scanner, MIT) on every PR. Run
  [OpenSSF Scorecard](https://github.com/ossf/scorecard) weekly on public repos.
- Keep `dependency-review` on PRs for the three apps, and keep lockfiles committed.
- Branch rulesets on `main`: PRs and passing checks required, no force-push, no deletion (9.04).

## Detect and respond

- **`security.txt` on every domain.** The club site has one. Add it to `register.`, `map.` and
  `events.` as `public/.well-known/security.txt`, and turn on GitHub private vulnerability
  reporting (9.31, 9.03).
- **Weekly outside-in checks, report-only to start.** A small script checks headers and TLS on
  every domain (HSTS present, CSP present, no `unsafe-eval`, certificate days left). An
  [OWASP ZAP](https://www.zaproxy.org/) baseline scan runs against production. Both are free and
  open source (9.32).
- **Supabase Security Advisor** run monthly on each project (free).
- **Incident runbook** (`docs/INCIDENT_RESPONSE.md`, 9.33): who to call, how to rotate each key in
  ten minutes, how to pause registration, Stripe's dispute steps, and when and how to tell
  families. The first move is always to rotate first and investigate after.
- **Rotation calendar (9.13):**

  | When | What |
  |---|---|
  | After every contest | Deactivate contest-day staff accounts (already in VA-States' "Now" list). Rotate `CRON_SECRET` and any shared day-of codes |
  | Yearly (October) | Supabase secret keys, the Stripe restricted key, Resend, Upstash and QStash tokens, the `security.txt` `Expires` line |
  | When someone leaves or a device is lost | Everything that person or device could reach |
  | Only if compromised | The `age` backup key (rotating it orphans old backups) and `PII_ENCRYPTION_KEY` (rotation goes through `key_id`) |

## Per repo

### dmvthrowers.github.io (live club site)

- Harden every page's CSP `<meta>`. Today it's `default-src 'self'; script-src 'self'
  'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:;`.
  Add `object-src 'none'; base-uri 'self'; form-action 'self'` (Formspree only on
  `contact.html`) and `upgrade-insecure-requests`. Extend `check_site.py` so a page can't ship
  without them (9.23). `frame-ancestors` and HSTS can't be set from a `<meta>` tag; that's the
  Cloudflare decision (9.12).
- CI clean-up (9.20). Check the Pages setting "Enforce HTTPS" (9.09).
- Inline scripts (the FAQ toggle, the hamburger) keep `'unsafe-inline'` for now. Moving them into
  `assets/js/` would let the site drop it. That's a later, larger edit across about 40 pages.

### VA-States and yoyo-registration-template (the money app)

Template first, then port, as always. Production care on VA-States.

- Staff MFA (9.25).
- **Strict CSP (9.26).** Today scripts allow `'unsafe-inline'` and `'unsafe-eval'`, and the CSP
  allows Google Fonts. Move to per-request nonces from `proxy.ts` (Next supports this) and keep
  `'unsafe-eval'` for `next dev` only. Self-host the fonts, which also follows the
  no-outside-fonts brand rule.
- Field-level encryption for High-tier columns (9.27).
- Append-only audit log, recording sign-ins and every decrypt. Rate limits on the two
  unthrottled guards (9.28).
- Stripe restricted key and Supabase secret keys (9.07, 9.08). The backup secret moves into an
  environment (9.20). `SECURITY.md` for VA-States (9.22).

### yoyo-player-map

- Replace the shared admin password with named accounts and MFA (9.29).
- Drop `'unsafe-eval'` from the production CSP (with 9.26's pattern).
- Already on its "Now" list: confirm the service-role key rotation, secret scanning, Vercel
  storage clean-up (0.3). 9.07's switch to `sb_secret_` keys finishes that job.
- CI clean-up and removing the `.vs/` files (9.20, 9.22).

### dmvt-event-hub (before launch)

Launch is the cheapest time to get this right. Item 9.30 is a launch gate for 7.1:
untrack `.env`, CORS allow-list, `verify_jwt` where a function needs a user, admin MFA, an
`age`-encrypted nightly backup like the other apps, `.vs/` removed, pinned actions and
least-privilege workflows.

### DMVT-Design

Low data, but it's the repo every brand change flows from. Pin and trim its workflows (the
CodeQL duplicates, PowerShell, super-linter and summary). Add Dependabot for `github-actions`
and a `SECURITY.md`. Remove `.vs/` and the uploads `.zip`, whose logos already live in
`assets/` (9.20, 9.22).

### Static templates (club, contest, map, scouts) and their copies (troop, pack)

These are the multiplier: every club that copies a template inherits its defaults.

- `check_site.py` fails the build when a page's CSP is missing `object-src 'none'` or
  `base-uri`, or allows `unsafe-eval` (9.24).
- `build.py` writes `/.well-known/security.txt` from a `security` block in `site.jsonc`.
- **"Secure your copy"** in each `DEPLOY.md`: turn on 2FA, secret scanning, Enforce HTTPS, DNSSEC
  and branch rules. A static site collects no personal data, and forms link to the forms system.
- Pack 1125: self-host its fonts (already decided), which removes Google from its CSP.

### scouts-private (admin and parent portal, not started)

If it gets built, this will hold the most sensitive data on the roadmap: children, parents and
maybe medical forms. Write the spec before any code (9.34):

- Don't store medical forms at all if the official tools (Scoutbook, or the council's own) can
  hold them. Link to them instead.
- If it does store them: invite-only accounts, passkeys or TOTP for every leader, RLS per family
  and per den, field-level encryption (same pattern as 9.27), an audit log for every read, and
  the retention rules agreed before launch.
- Keep the repo private, and add gitleaks and osv-scanner to CI. GitHub's secret scanning and
  code scanning cost money on private repos.

## Costs: what we skip or build around

| Paid thing | Cost | What we do instead |
|---|---|---|
| Supabase point-in-time recovery | Pro plan plus an add-on | Nightly `age`-encrypted dumps and a tested restore every quarter |
| Supabase time-boxed and idle sessions, SSO | Pro plan | Short JWT expiry plus MFA |
| Vercel team members (a second admin) | Pro, about $20 a month | Deploys come from GitHub merges, so a second GitHub owner can ship. The Vercel login and recovery codes sit in the shared vault. Revisit if the club takes on a treasurer |
| Vercel advanced firewall and password protection | Pro or Enterprise | The free firewall rules, our own rate limits and Turnstile |
| GitHub Advanced Security on private repos | Per committer | Keep repos public where possible; gitleaks and osv-scanner on the private ones |
| Hardware security keys | Roughly $25–60 each, buy two | Passkeys on phones and laptops are free. Two keys for the owner account are the best-value purchase on this page |
| Penetration test | Thousands of dollars | OWASP ZAP baseline, Supabase Security Advisor, and this review repeated yearly |
| SMS MFA | Per message | TOTP apps and passkeys, which are free and stronger |

Everything else in this plan is free.

## Decisions needed (owner)

1. **Cloudflare (free) in front of `dmvthrowers.club`?** It moves DNS from Porkbun to Cloudflare
   (the domain stays registered at Porkbun). In return the site gets real HSTS, real CSP headers
   and the HSTS preload list. GitHub Pages stays the host, and `CNAME` doesn't change.
   Recommendation: yes, after 9.05.
2. **Who must use MFA in the registration app?** Recommendation: admin and finance required;
   judges, DJs and other contest-day roles optional.
3. **Field-level encryption scope.** Recommendation: the six fields listed above, template first.
4. **Two hardware keys** for the owner account (the one purchase recommended).
5. **The map's admin password** goes away once named admin accounts work (9.29). Who else should
   be a map admin?
