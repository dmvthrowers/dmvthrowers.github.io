# Spec 00: Meetup Booking Gate

**Status:** Draft, needs Brandon's approval · **Repo:** dmvthrowers.github.io · **Size:** under 1 session · **Deadline:** before the Monday Oct 19, 2026 workflow run

## Problem

`scripts/update_meetup.py` runs every Monday at 12:00 UTC (`.github/workflows/update-meetup.yml`). It computes the next 3rd Sunday with `upcoming_third_sundays()` and writes it to the NEXT MEET bar on every page, then writes the next 12 dates to `meetups.ics`. Nothing checks whether the room is booked. Arlington Central Library is confirmed only through Sunday Oct 18, 2026. After that run, the site will advertise Nov 15 at Arlington, and calendar subscribers will get 12 months of unconfirmed dates.

## Scope

In: a booking cutoff and a "to be announced" state for the updater, its top bar, `events.html` and `meetups.ics`.
Out: changing venues, new pages, the event hub feed (BUILD_PLAN 7.3).

## Design

1. Add a small settings file `scripts/meetup_settings.json`:
   ```json
   { "booked_through": "2026-10-18", "venue": "Arlington Central Library", "skip": [] }
   ```
   `booked_through` is the last date with a confirmed booking. `skip` lists dates with no meetup (holidays, room conflicts).
2. `upcoming_third_sundays()` results are filtered: drop `skip` dates; split the rest into **confirmed** (≤ `booked_through`) and **unconfirmed**.
3. Top bar: if the next date is confirmed, unchanged. If not, the bar reads `NEXT MEET: SUNDAY, NOVEMBER 15 · TO BE CONFIRMED · SEE EVENTS →` (same markup, no venue name).
4. `meetups.ics`: write confirmed dates only. Unconfirmed dates are left out until booked, so phones never hold a wrong date.
5. `events.html`: the updater only removes past cards today. Leave adding cards to people. No change beyond that.
6. Workflow log prints `Booked through 2026-10-18; next date unconfirmed` when the gate trips, so the Monday run shows it.
7. Mirror the setting in `yoyoclub-template` only if it lacks one: its `site.jsonc` already supports skip dates; check before porting (parity line: "live-only" unless a gap is found).

## Acceptance criteria

- [ ] With `booked_through: 2026-10-18` and today = Oct 19, 2026, `python3 scripts/update_meetup.py --dry-run` reports the next date as Nov 15, unconfirmed, and the bar text contains "TO BE CONFIRMED" and no venue.
- [ ] `meetups.ics` contains no event after `booked_through`.
- [ ] A date in `skip` never appears in the bar or the `.ics`.
- [ ] With `booked_through` set a year out, output matches today's output byte for byte (no change for the booked case).
- [ ] `python3 scripts/check_site.py` passes; the W3C validator passes on changed pages.
- [ ] Unit tests for the date split (confirmed, unconfirmed, skipped) run in the workflow or under `scripts/`.

## Open questions for Brandon

- Is any November date booked anywhere? If yes, set `booked_through` and `venue` instead of shipping TBC copy.
- Wording: "TO BE CONFIRMED" or "DATE AND PLACE TBA"?

## Claude Code handoff

```
Repo: dmvthrowers.github.io. Read CLAUDE.md and docs/hub/specs/00-meetup-booking-gate.md.
Implement the booking gate in scripts/update_meetup.py exactly as specced: add
scripts/meetup_settings.json, filter skip dates, split confirmed/unconfirmed by
booked_through, write TBC top-bar copy for an unconfirmed next date, and write only
confirmed dates to meetups.ics. Add tests for the date split. Run --dry-run with a
simulated today of 2026-10-19 and paste the output in the PR. Run
python3 scripts/check_site.py. Branch claude/meetup-booking-gate, commit prefix
fix(events):, PR body lists each acceptance criterion with its evidence.
```
