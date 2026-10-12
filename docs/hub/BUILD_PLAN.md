# YoYo Community Organizer Hub — Build Plan (v1.1)

Oct 11, 2026 · Brandon Rogers · Companion to the [Organizer Hub spec](SPEC.md). Folded into the repo-wide [`../BUILD_PLAN.md`](../BUILD_PLAN.md) as Wave 10 and into [`../ROADMAP.md`](../ROADMAP.md). The spec says what and why; this doc says how, when, and who. It is a living document: phases move from upcoming → active → done, and gates are recorded here with dates. Anything marked **Proposed** is new in v1.1 and needs Brandon's approval.

The main change from v1: the plan now runs in four lanes, so the Cloudflare blocker stops only the work that needs the app. Kits, the governance pack and seed retros are markdown and can start now.

## 1. Build principles

Pulled from the spec and the Oct 11, 2026 decisions — these are non-negotiable unless Brandon changes them:

- **Spec-first per piece; build once specs exist.** No implementation PR without an approved spec section. This is a hard gate, not a suggestion.
- **Net-new gap filling first; self-hosted alternatives last.** Organizer tooling, kits, Exchange, governance pack. Player-facing apps are covered by existing products — do not rebuild them.
- **Templates over advice.** Every guide ships with something you can copy and deploy.
- **Event hub is the central app.** The Exchange, calendar, and hub features live in the event hub (Cloudflare Pages + Workers + D1, isolated email). The calendar ties into event features rather than standing alone. Cross-links between all DMVT apps and sites.
- **Rides under DMV Throwers.** No separate charter, no separate org.
- **Open source everything.** The hub ships as a self-hostable template so other hobbies can copy and adapt it.
- **Integrate where good open source exists; build where only closed or paid exists.**
- **Markdown doesn't wait on apps (Proposed).** Guides, kits, retros and governance templates ship as markdown in a repo as soon as their spec is approved.
- **Youth-safe by default (Proposed).** Anything that stores people gets a privacy check before merge (spec §1).

## 2. Roles & process

| Role | Who | Does |
| --- | --- | --- |
| Decider | Brandon | Approves specs, merges PRs, sends external mail, holds the NYYL conversations |
| Spec author / reviewer | Nova | Writes specs and acceptance criteria, reviews PRs with real-world context Claude lacks, feeds details from mail/calendar/Drive into issues |
| Implementer | Claude Code | Implements from specs; opens PRs from `claude/*` branches |
| Design partners (Proposed) | the Bmore YoYo Club and SWVA Throwers organizers, plus one juggling club (Fairfax Jugglers or Ashburn Juggling Society) | Try each path or tool before it's called done; the juggling club is the Phase 7 "other hobby" test |

GitHub (`dmvthrowers`) is the shared workspace. Nova never merges; Claude never decides scope. **Proposed:** hub repos move to the DMV-Throwers org with a second owner.

Workflow per build:

1. Nova drafts (or refines) the spec section.
2. Brandon approves the spec.
3. Nova writes acceptance criteria.
4. Claude Code implements, opens PR from a `claude/*` branch.
5. Nova reviews the PR (real-world context, edge cases, spec fit).
6. Brandon merges.
7. Deploy / publish where it lives.
8. Hub index updated — the thing is findable from the hub.

Phase gates: a phase starts only when its entry criteria are met, and ends only when its exit criteria are met. Gates are recorded in §8 with dates as they happen.

## 3. Definition of done

Applies to every build, no exceptions:

- Spec section approved by Brandon.
- Acceptance criteria written before implementation.
- PR from a `claude/*` branch, CI green.
- Nova review pass complete.
- Brandon merged.
- Deployed / published where it lives.
- Hub index updated.
- **Proposed:** a design partner completes the path or uses the tool without help.
- **Proposed:** privacy check passed for anything that stores people's data.

A build is not done when the PR merges — it is done when a stranger can find and use the thing from the hub.

## 4. Lanes

| Lane | Where the work lives | Waits on | Phases |
| --- | --- | --- | --- |
| A. Start now | Markdown in a repo | Spec approval only | 3, 5, seed retros |
| B. Back office | yoyo-registration-template first, then VA-States | Spec approval only | 4 |
| C. Commons | Event hub on Cloudflare | Workers Scripts Edit permission | 1 → 2 → 7 |
| D. Circuit | Hub standings + data | NYYL standard (6b only) | 6a, 6b |

## 5. Phases

### Phase 0 — Foundations (DONE Oct 11, 2026)

Spec v1 complete; all four open questions decided (event hub as central app, hosted board for the Exchange, Brandon seeds the standards library, everything under DMV Throwers). Event hub platform decided: Cloudflare Pages + Workers + D1 with isolated email.

Parallel track (non-blocking): NYYL conversations — sanctioning checklist, seeding/bypass terms, calendar coordination. Owner: Brandon.

### Phase 1 — Event hub replatform + central app shell (Lane C)

Cloudflare Pages + Workers + D1, isolated email (its own Resend key), cross-links between all DMVT apps and sites, calendar as a tied-in event feature. This phase IS Fall 2026 Build 1. One plan, one owner, tracked once.

Scope it as a rebuild: the Lovable app's Supabase RLS policies, edge functions (submit, verify, manage, renew, daily maintenance) and pg_cron job become Workers code, D1 queries and Cron Triggers. The React front end carries over.

- **Entry:** Workers Scripts Edit permission resolved. Check first whether it's an API-token scope: a token created from the "Edit Cloudflare Workers" template in the Cloudflare dashboard may be the whole fix. Separate Resend key created.
- **Exit:** events.dmvthrowers.club live on the new stack; a test submission receives its verify email; the renewal cron runs; the club site reads the calendar feed; all DMVT apps cross-linked; deploy documented as the Cloudflare reference architecture.

### Phase 2 — The Exchange (Lane C)

Hosted board in the event hub, segmented by org/event type (state contest directors, club runners, meetup hosts, demo/school program leads). Retros are markdown rendered by the board (Proposed).

- **Entry:** Phase 1 shell live. Seed retros already written in Lane A (VSYC-26 and DMVT).
- **Exit:** board live with seed content; retro template published; first external retro submitted.

### Phase 3 — Kits (Lane A, start now)

Fill the documented gaps, one kit at a time (each kit = guide + templates + checklist). No dependency on Phase 1: kits are markdown.

Order (Proposed), by what's happening soonest:

1. **Event kit** — package the Event Planning Kit + Workshop Run Sheet; write the Conway, SC playbook from the Nov 23 program; demo scripts; library-partnership pattern.
2. **Contest kit** — organizer's guide (bid to teardown), judge recruiting playbook, day-of run sheet, music/format ops, venue contract + COI checklist, hotel-block playbook, press playbook. Feeds VSYC-27 prep.
3. **Club kit** — "running a club" guide (cadence, roles, money, burnout), venue-finding playbook, youth-safety notes, loaner program guide, "make it official" guide.

- **Entry:** spec section per kit approved.
- **Exit:** each kit linked from its front-door path and tried by a design partner. Until the hub shell exists, the front door is a page on dmvthrowers.club.

### Phase 4 — Organizer software: finish and generalize (Lane B, start now)

Most of this exists in VA-States for one contest (spec §3.6). Each build finishes the missing piece in yoyo-registration-template first, then ports to VA-States (the repo-wide "template first, then live" rule, with a parity line on every PR). Ordered by VSYC-27 need (Proposed):

| Order | Build | Missing piece | Needed by |
| --- | --- | --- | --- |
| 1 | 9 Sponsor pipeline | Fulfillment ledger: per-tier promises tracked to delivery, drafted shoutout queue | VSYC-27 sponsor outreach (Nov–Dec) |
| 2 | 5 Sponsor recap generator | Recaps from contest and survey data, not by hand | Same outreach: open with last year's numbers |
| 3 | 8 Volunteer module | Shift scheduling (T8), briefing email, role cards | Volunteer recruiting (spring 2027) |
| 4 | 10 Livestream overlay | Live scores and standings overlay (#96) | Contest season 2027 |
| — | Check-in + passport, loaner tracker | Net new; spec first | Unscheduled |

- **Entry:** per-build spec + acceptance criteria approved.
- **Exit:** per §3 definition of done, each build, including the template port.

### Phase 5 — Governance pack + standards library (Lane A)

Generalize DMV Throwers docs into reusable templates (charter, officer roles, code of conduct, budget, youth protection, financial transparency). Brandon seeds the standards library from VA-States and DMVT, including the open contest results format and the canonical division map (spec §5).

- **Entry (changed):** DMV Throwers' conduct team and report routing decided (BUILD_PLAN 5.2). No longer waits on Phase 2; GitHub issues are the contribution channel until the Exchange exists.
- **Exit:** pack published; library seeded with contest + club standards; contributions flow through the Exchange once Phase 2 lands.

### Phase 6 — Circuit support (Lane D)

Split into two parts so the data work doesn't wait on NYYL (Proposed):

- **6a — Back-test (start now).** Collect VSYC-26 `results.json` from the season-archive tool plus 2026 results from seed states. Run the v0 power ranking and OpenSkill side by side; settle the season-points rules (spec §11). Exit: a back-test report ready for the NYYL pitch.
- **6b — Standings tool.** Season points + power ranking, standings pages, sanction-ready checklist tooling. Entry: NYYL conversations far enough along to know the standard. Exit: a participating state contest can report results and see standings.

### Phase 7 — Template packaging (Lane C)

Package the hub as a self-hostable open-source template: docs, one-click deploy, sample content — so any other hobby can stand up its own hub.

- **Entry:** Phases 1–5 done (there is something worth packaging).
- **Exit:** a stranger from another hobby — the juggling design partner first — can deploy a working hub from the template.

### Parking lot (unphased)

From spec §10 — each gets specced when its turn comes. Net-new community building stays the top priority: challenge platform, online event template (Boomer Club playbook), online contest format (ANTE reference), mentorship matching, throw-it-forward, charity throwdown, regional circuit, State of the Scene report, new-player journey, demo-in-a-box, content drumbeat, sponsor-funded challenges, judge pool registry, regional sponsor directory, verified press list, venue pitch pack.

## 6. One plan: mapping

Phases 1 and 4 share work with the Fall 2026 scope and the repo's `docs/BUILD_PLAN.md`. This table is authoritative: each piece of work is tracked once, here.

| Fall 2026 build | Hub phase | Repo BUILD_PLAN item |
| --- | --- | --- |
| 1 Event hub relaunch on Cloudflare | Phase 1 | 7.1 launch, 9.30 launch security gate |
| 2 VSYC-27 reset + idea board | Outside the hub (VA-States); its retro feeds Lane A | #76, idea-board spec v2.1 |
| 3 Media pipeline | Parking lot: content drumbeat | — (home lab) |
| 4 Contest auto-clipper | Parking lot: content drumbeat | — (home lab) |
| 5 Sponsor recap generator | Phase 4 | — |
| 6 Contest front door | Spec §3.4, front door for Phase 3 | — |
| 7 Calendar sync | Phase 1 (calendar feed) | 7.3 club events page reads the hub's feed |
| 8 Volunteer module | Phase 4 | T8 volunteer shifts (Wave 6) |
| 9 Sponsor pipeline | Phase 4 | 5.1 sponsor form on the forms engine |
| 10 Livestream scoring overlay | Phase 4 | #96 livestream wishlist |

If the Fall 2026 doc and this doc ever disagree, this doc wins for hub work and the Fall 2026 doc gets updated to match.

## 7. Ambiguity reduction

How this doc keeps the build from drifting:

- **Entry/exit criteria per phase (§5).** No phase starts fuzzy and none ends by vibes.
- **Acceptance criteria before implementation.** Written by Nova, approved by Brandon, handed to Claude Code with the spec.
- **Decision log (§8).** Every decision carries a date.
- **Single owner, single spec author, single implementer.** Brandon decides, Nova specs, Claude builds. If a task doesn't fit one of those lanes, it isn't a build task.
- **The spec is the scope boundary.** If it isn't in the spec (or a spec-approved addition), it isn't in the build. Parking-lot ideas get specced before they get built.
- **One plan, not two.** The mapping table (§6) is authoritative.
- **Where agents can read it.** This plan and the spec live in `dmvthrowers.github.io/docs/hub/`, the single source agents read. The Fall 2026 scope, the repo's BUILD_PLAN.md and the registration template's HUB_ROADMAP.md link here instead of restating hub work.

## 8. Dependencies, decisions and risks

### Dependency map

- Lanes A and B start now; they need only spec approval.
- Phase 2 (Exchange) depends on Phase 1. Phase 7 depends on Phases 1–5.
- Phase 5 depends on the conduct-team decision, not on Phase 2.
- Phase 6a starts now; 6b depends on the NYYL track. Nothing else waits on NYYL.
- Phase 4 and the VSYC-27 calendar: the sponsor ledger and recaps before outreach (Nov–Dec), volunteers before recruiting, the overlay before contest season.

### Decision log

| Date | Decision |
| --- | --- |
| Oct 11, 2026 | Event hub is the central app |
| Oct 11, 2026 | Exchange phase 1 is a hosted board |
| Oct 11, 2026 | Brandon seeds the standards library from VA-States and DMVT |
| Oct 11, 2026 | Everything rides under DMV Throwers |
| Oct 11, 2026 | Event hub replatforms to Cloudflare Pages + Workers + D1 with isolated email, as a reference architecture |
| Oct 11, 2026 | Phase 0 done |
| Oct 11, 2026 | Spec and build plan live in `docs/hub/`; folded into the repo ROADMAP and BUILD_PLAN (Wave 10) |

Pending (from spec §9): commons / back-office boundary; youth-safe and outlives-its-founder principles; conduct team; OpenSkill back-test; circuit money custody and committee; contribution license; design partners; lanes and phase changes in this v1.1.

### Risks & watch items

- **Cloudflare Workers Scripts Edit permission** — known blocker for Phase 1. May be a token scope (§5, Phase 1). Blocks Lane C only.
- **D1 rebuild effort** — leaving Lovable means rewriting the backend, not redeploying it. Budget 1–2 weekends honestly, not one evening.
- **Supabase Management API access down** — it needs a fresh personal access token. Lane B database work means manual SQL-editor runs until then.
- **Free-tier ceilings** — Cloudflare Workers/D1 limits for the hub; Supabase free projects pause when idle; Vercel's free plan is for non-commercial use, which a fee-charging contest may not meet.
- **NYYL responsiveness** — external dependency; the 2027 pilot gives runway, and 6a uses the wait.
- **Scope creep into player-facing apps** — the spec marks them covered and low priority. Enforce it at spec review.
- **Minors' data** — passport, check-in and Exchange accounts touch kids. Privacy check before merge (§3).
- **Bus factor** — every repo sits on one personal GitHub account.
- **Circuit money custody** — a circuit fee means holding other states' money. No fee until custodian, ledger and payout rules exist.
- **Plan drift** — five overlapping planning docs; the §6 mapping and `docs/hub/` as the single source are the fix.
- **Brandon bandwidth** — he is the decision and merge bottleneck. Keep phases small and sequential where he's the constraint; parallelize where he isn't (lanes A and B vs C). Design partners take some review load.
- **Burnout** — the club kit literally calls for a burnout guide. Take the hint: sustainable pace, or the hub becomes another unfinished project.

## Changes in v1.1

- Plan reorganized into four lanes (§4); kits, governance and seed retros no longer wait on Phase 1.
- Phase 1: scoped as a backend rebuild onto D1; concrete exit criteria; the token-scope check for the blocker.
- Phase 3: kits ordered by what's soonest (event kit first, around the Nov 23 Conway program).
- Phase 4: renamed "finish and generalize"; builds ordered by VSYC-27 need; template first, then VA-States.
- Phase 5: entry changed from "Phase 2 live" to "conduct team decided."
- Phase 6: split into 6a back-test (now) and 6b standings tool (after NYYL).
- Added: design partners (§2), two definition-of-done checks (§3), the Fall-build mapping table (§6), a dated decision log (§8), and six risks.
