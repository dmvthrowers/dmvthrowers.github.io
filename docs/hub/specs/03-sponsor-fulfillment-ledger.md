# Spec 03: Sponsor Fulfillment Ledger

**Status:** Draft, needs Brandon's approval · **Repos:** yoyo-registration-template first, then VA-States (parity: "ports to VA-States") · **Lane / phase:** B / 4 · **Fall build:** 9 · **Size:** 1–2 sessions · **Needed by:** VSYC-27 sponsor outreach, Nov–Dec 2026

## Problem

Sponsors were promised things by tier (logo on banners and screens, booth, shoutouts, tags) and some promises slipped: after VSYC-26 the organizer told a sponsor he had fallen behind on shoutouts and tagging. The app already tracks a per-sponsor checklist, but every item is typed by hand, nothing has a due date or owner, and nothing records proof that it happened. For VSYC-27 asks, "here's exactly what you'll get and how we'll prove it" is a selling point.

## What exists (don't rebuild)

- `contest_sponsors.deliverables jsonb`: array of `{ label, done }`, max 20, cleaned by `cleanDeliverables()` in `lib/sponsors.ts`.
- `/sponsors` page: toggle done, "Add deliverable" (a `window.prompt`), and a "Deliverables done X of Y" summary from `summarizeSponsors()` (counts committed and paid sponsors only).
- `contest.config.ts` → `sponsors.tiers[]` has `{ id, label, amount, slots?, perks? }`. `perks` is optional and unused by the checklist.
- Capability `sponsors.manage` gates the page.

## Design

**1. Richer deliverable** (backward compatible; old rows still parse):

```ts
interface Deliverable {
  label: string;           // existing
  done: boolean;           // existing
  kind?: 'logo' | 'booth' | 'shoutout' | 'social_post' | 'stream' | 'prize' | 'other';
  due?: string;            // ISO date; default derived from kind (see 3)
  owner?: string;          // staff display name, free text
  proof_url?: string;      // link to the post, photo or clip (https only)
  done_at?: string;        // ISO timestamp, set when done flips to true
}
```

`cleanDeliverables()` keeps unknown fields out, caps text lengths, validates `due` and `proof_url`, and still caps the list at 20. No migration: the column is already `jsonb`.

**2. Tier templates in config.** Extend tiers with optional structured deliverables, keeping `perks` as display text:

```ts
tiers: [{ id: 'gold', label: 'Gold', amount: '$500+', slots: 2,
  deliverables: [{ label: 'Logo on banner', kind: 'logo' }, { label: '2 Instagram shoutouts', kind: 'social_post' }] }]
```

When a sponsor moves to **committed** with a tier that has a template, and its checklist is empty, seed the checklist from the template. Never overwrite a non-empty list. A "Reset from tier" button re-seeds on request (with a confirm).

**3. Due dates by kind**, relative to `contest.date`: logo −21 days (print deadline), social posts spread across the 4 weeks before, stream and booth on the day, prize on the day, thank-you post +3 days. Staff can edit any date.

**4. Ledger view on `/sponsors`.** A tab "Fulfillment" lists every open deliverable across committed and paid sponsors, sorted by due date, with overdue items flagged. Columns: sponsor, item, due, owner, proof, done. Replace `window.prompt` with an inline form.

**5. Shoutout queue.** For each open `social_post` or `shoutout` item, show a drafted caption: sponsor name, tier, the sponsor's handle (new optional field `contact_handle` on the sponsor, stored in `notes` until a column is warranted), and the contest hashtag. A "Copy" button only. The app never posts.

**6. Summary upgrade.** `summarizeSponsors()` adds `deliverablesOverdue`, and the dashboard shows it.

## Out of scope

Posting to social networks; sponsor logins seeing their own ledger (later; `auth_user_id` exists); file uploads for proof (links only, free-tier storage).

## Acceptance criteria

- [ ] Existing rows with `{label, done}` load and save unchanged; tests cover old and new shapes in `lib/sponsors.test.mjs`.
- [ ] Moving a sponsor with an empty checklist to committed seeds it from the tier template; a non-empty checklist is untouched.
- [ ] Due dates default by kind from `contest.date` and are editable; overdue items show on the Fulfillment tab.
- [ ] `proof_url` accepts only `https://` links; `done_at` is set when an item is ticked and cleared when unticked.
- [ ] Shoutout queue shows a caption per open social item with a Copy button and no network call.
- [ ] Every change is audit-logged with `logAudit`; routes check `sponsors.manage` server-side.
- [ ] `npm run typecheck`, `lint`, `test`, `build` pass in the template; the VA-States port PR passes the same and moves VSYC wording into config.

## Open questions for Brandon

- The VSYC-27 tier list and each tier's promised deliverables (also open in the template's `docs/SPONSOR_FORM.md` questions 1–4).
- Due-date offsets: is 21 days right for the banner print deadline?

## Claude Code handoff

```
Repo: yoyo-registration-template. Read AGENTS.md, docs/PARITY.md,
docs/SPONSOR_FORM.md and docs/hub/specs/03-sponsor-fulfillment-ledger.md (in
dmvthrowers.github.io). Extend Deliverable and cleanDeliverables in lib/sponsors.ts
(backward compatible, tests first), add optional tier deliverables in
contest.config.ts, seed on committed when empty, default due dates by kind, add the
Fulfillment tab and shoutout queue to app/sponsors, and audit-log every change. No
migration: deliverables is already jsonb. Run typecheck, lint, test, build. Branch
claude/sponsor-fulfillment-ledger; PR states the parity line "ports to VA-States".
Then open the VA-States port as a second PR linked from the first.
```
