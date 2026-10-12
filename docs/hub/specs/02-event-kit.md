# Spec 02: Event Kit and the School/Library Playbook

**Status:** Draft, needs Brandon's approval · **Repo:** dmvthrowers.github.io · **Lane / phase:** A / 3 (spec §3.3) · **Size:** 2 sessions plus Brandon's notes from the Nov 23 program

## Problem

The club runs demos, workshops and library programs, but the know-how lives in two Word files and Brandon's head. The Nov 23, 2026 Conway, SC library program is confirmed: write the playbook around it, so the first real use tests it.

## Scope

In: an Event Kit guide page, a school/library playbook, a 45-minute demo script, a booking email template, a loaner-set checklist, a post-event recap template. Packaging of the existing `event-checklist.docx` (shown as "Event Planning Kit") and `workshop-run-sheet.docx`.
Out: contest material (contest kit), online events, any app.

## Deliverables

1. **`event-kit.html`** (guide page, main-site styling; card on `guides.html`; linked from the front door's "Host a meetup or demo" path):
   - Pick your format: meetup, workshop, demo/assembly, library program, booth at a festival. One line each on size, length and what to bring.
   - Before / day of / after checklists (from `event-checklist.docx`, rewritten as HTML so they're searchable and link-able).
   - Downloads: the two existing documents plus the new templates below.
2. **School and library playbook** (section of the page, or `event-kit-library.html` if long):
   - Finding the contact, the booking email, what to ask (room, power, tables, age range, headcount, photo policy, insurance or COI needs).
   - Run of show for 45 minutes: welcome and safety (5), demo (5–10), learn the first trick in groups (20), try-a-trick stations or Q&A (5–10), where to go next (5).
   - Loaner set: how many per headcount, string spares, check-out and check-in, cleaning.
   - Youth safety: two adults present, no photos of kids without a parent's OK, no collecting kids' contact details.
   - Afterward: thank-you note, photo selection rules, a 5-line recap for the club's records.
3. **Templates** (Markdown source in `docs/kits/event/`, plus `.docx` exports in `assets/documents/`): booking email, run-of-show sheet, loaner checklist, recap.

## Facts to collect, not invent

These come from Brandon, not from Claude. Leave a visible `TODO(Brandon)` until filled:

- Conway, SC specifics: library, room, date and time, age group, headcount, who booked it and how, what worked and what didn't (fill after Nov 23).
- Loaner ratio the club actually uses.
- Any library insurance or paperwork the club has been asked for.

## Acceptance criteria

- [ ] `event-kit.html` passes `check_site.py`, the W3C validator and axe with no new findings; 360 px wide with no scroll.
- [ ] Card on `guides.html`; the front door's Host path links here.
- [ ] Every template exists as Markdown in `docs/kits/event/` and as a download.
- [ ] No invented facts: every Conway-specific line is either filled by Brandon or marked `TODO(Brandon)`, and the page ships without unfilled TODOs.
- [ ] Youth-safety rules match the club's code of conduct and privacy page.

## Open questions for Brandon

- One page, or a hub plus a separate library playbook page?
- Ship before Nov 23 (playbook as the plan) and revise after, or ship after with real notes? Recommended: ship the plan before, revise after.

## Claude Code handoff

```
Repo: dmvthrowers.github.io. Read CLAUDE.md, docs/hub/specs/02-event-kit.md, and the
contents of assets/documents/event-checklist.docx and workshop-run-sheet.docx.
Build event-kit.html (guide styling, card on guides.html) and the four templates in
docs/kits/event/ as specced. Do not invent Conway, SC details, loaner ratios or
insurance facts: mark them TODO(Brandon) and list them in the PR body. Keep the PR
in draft until every TODO is filled. Run python3 scripts/check_site.py. Branch
claude/event-kit, prefix feat(guides):.
```
