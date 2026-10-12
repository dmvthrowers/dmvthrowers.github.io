# Spec 04: Sponsor Recap Generator

**Status:** Draft, needs Brandon's approval · **Repos:** yoyo-registration-template first, then VA-States · **Lane / phase:** B / 4 · **Fall build:** 5 · **Size:** 1–2 sessions · **Needed by:** VSYC-27 sponsor outreach, Nov–Dec 2026 · **Depends on:** spec 03 (deliverables with proof)

## Problem

After VSYC-26, tailored recaps went to 17 sponsors, the venue, judges, crew, competitors and spectators, all built by hand around Sept 30. They worked (sponsors replied with thanks), but the numbers had to be gathered from surveys, results and notes each time. Next year's asks should open with last year's numbers, generated in minutes.

## What exists (don't rebuild)

- Surveys in `contest_survey_responses` with definitions in `lib/surveys.ts`. Useful keys: `heard_from`, `time_on_site`, `travel_time`, `venue_spend`, `weekend_spend`, `recommend_nps`, `overall_rating`, `stream_watch_time`, `watch_mode`; presenting-sponsor block `sponsor_familiarity`, `sponsor_booth`, `sponsor_stream_noticed`, `sponsor_activities`, `sponsor_purchase_intent`, `sponsor_affinity`; sponsor survey `sponsor_delivered`, `sponsor_benefits_value`, `sponsor_next_year`, `sponsor_goals`.
- Note: the presenting-sponsor block only runs when `contest.presentedBy.name` is set. Other sponsors get no per-brand survey questions, so their recap uses event-level numbers plus their own deliverables.
- Registrations, divisions and results (`lib/standings.ts`), the season archive, the sponsor ledger (spec 03), and the admin Surveys tab with CSV export.

## Design

**A printable recap page per sponsor** at `/sponsors/[id]/recap`, gated by `sponsors.manage`, with print CSS so "Save as PDF" in a browser produces the file. No PDF library, no new dependency.

Sections, in order:

1. **The day in numbers:** competitors, divisions, spectators (RSVPs and survey estimate), stream viewers if recorded, states represented.
2. **Where your brand showed up:** the sponsor's deliverables with proof links and done dates (spec 03). Undelivered items are listed honestly as "not delivered".
3. **The audience you reached:** event-level survey numbers (time on site, travel time, spend bands, NPS). For the presenting sponsor only: familiarity before, booth visits, stream notice, purchase intent.
4. **What attendees said:** up to 3 quotes from `quote_text` where `allow_quote` is true (the survey route already stores a quote only with consent).
5. **Next year:** VSYC-27 date (if set) and a link to the sponsor form.

**Recap types:** sponsor (above), venue (attendance, dwell time, spend, sentiment), and a public State of the Scene summary (no per-sponsor data). Same engine, different section lists in config.

**Numbers rules:** every figure shows its base ("62% of 48 spectator responses"). Fewer than 10 responses for a question → show counts, not percentages. No personal data: no names, emails or minors' details.

## Out of scope

Emailing recaps (staff send them; a later step may queue them through the outbox); charts beyond simple bars in HTML/CSS; per-sponsor survey questions for non-presenting sponsors (a survey change, separate spec).

## Acceptance criteria

- [ ] `/sponsors/[id]/recap` renders for any sponsor with seeded test data, prints to letter size on two pages or fewer, and passes axe.
- [ ] Every percentage shows its base; any question with fewer than 10 answers shows counts only.
- [ ] Quotes appear only where quoting was allowed; no names, emails or minor data appear anywhere.
- [ ] Undelivered deliverables are listed as not delivered, not hidden.
- [ ] Venue and State of the Scene variants render from the same engine.
- [ ] Pure functions for the number crunching with unit tests; typecheck, lint, test, build pass; VA-States port PR follows.

## Open questions for Brandon

- Which VSYC-26 recap layout to copy as the reference (the Goodles recap or a standard-tier one)?
- Should standard-tier sponsors get a short survey block of their own next year? (Separate spec if yes.)

## Claude Code handoff

```
Repo: yoyo-registration-template. Read AGENTS.md, docs/PARITY.md and
docs/hub/specs/04-sponsor-recap-generator.md (in dmvthrowers.github.io). Build pure
recap functions in lib/recap.ts (tests first) over surveys, registrations, results and
sponsor deliverables; then app/sponsors/[id]/recap with print CSS, gated by
sponsors.manage server-side. Apply the numbers rules (base on every %, counts under
10 answers, no personal data). Add venue and State of the Scene variants. No new
dependencies. Run typecheck, lint, test, build. Branch claude/sponsor-recap-generator;
parity line "ports to VA-States".
```
