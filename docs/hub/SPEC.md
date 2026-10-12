# YoYo Community Organizer Hub — Spec (v1.2)

Oct 12, 2026 (v1.1 Oct 11) · Brandon Rogers · v1.1 revises v1 after a review against the repos, mail and Drive. Changes are listed at the end. Anything marked **Proposed** is new in v1.1 and needs Brandon's approval before it binds.

**This file is the source of truth.** Its build order is [`BUILD_PLAN.md`](BUILD_PLAN.md) in this folder, build facts are in [`REFERENCE.md`](REFERENCE.md), and draft feature specs are in [`specs/`](specs/); both are folded into [`../ROADMAP.md`](../ROADMAP.md) and [`../BUILD_PLAN.md`](../BUILD_PLAN.md) (Wave 10). The Google Drive copies are Oct 11 snapshots and keep organizer contact names, which stay out of this public repo.

## 1. Vision

The missing layer of the skill-toy world: everything an organizer needs to start and run a club, contest, or event — guides, templates, software, and peer knowledge — open source, no paid platform required.

NYYL standardized judging. YoYo Contest Central archives footage. Nobody standardized organizing. This hub fills that gap.

Principles:

- Open source everything. Integrate where good open source exists; build where only closed or paid exists.
- Net-new community building and gap filling first; self-hosted alternatives to existing apps last.
- Templates over advice: every guide ships with something you can copy and deploy.
- The hub itself is built in the open — spec first, build once specs exist.
- **Youth-safe by default (Proposed).** Minors appear by nickname or first name + last initial unless a parent opts in (the rule VA-States already enforces). No accounts for under-13s; a parent holds them. Check-ins collect no personal data.
- **Outlives its founder (Proposed).** Hub repos live in the DMV-Throwers GitHub org with at least two owners, not on one personal account.

## 2. Who it's for (paths)

The front door offers four paths. Each is guide + templates + checklist, in order, and opens with what it takes: time, money and people.

- **Start a club** — from idea to first meetup.
- **Run a contest** — from bid to teardown, any size.
- **Host a meetup or demo** — one-off events, workshops, school/library programs.
- **Run an online event or challenge (Proposed)** — themed months, trick challenges, video contests (see §10: Boomer Club and ANTE formats).

## 3. Sections

### 3.1 Club kit

How to run a club, not just how to make its website.

- Have: yoyoclub-template (+ prerequisites), club charter (v5), officer roles, code of conduct, meetup formats. Source material for "make it official": DMV Throwers' EIN, Virginia SCC fictitious-name filing, business bank account and payment stack (done March 2026).
- Gaps: a written "running a club" guide (cadence, roles, money, burnout), venue-finding playbook, youth-safety notes, loaner yoyo program guide, **"Make it official" guide (Proposed)** — EIN, state filing, bank account, payment stack, ledger.

### 3.2 Contest kit

How to organize a contest at any scale.

- Have: yoyo-contest-template, yoyo-registration-template (+ prerequisites), VSYC-26 lessons (issues #76–#96; 19 open per the idea-board spec — recount before seeding), NYYL rules + judge certification links, Financial Infrastructure Guide for a Volunteer-Run Yo-Yo Contest (Drive), VSYC-26 sponsor package and sponsor agreement (Drive), four VSYC-26 surveys (competitor, spectator, volunteer, sponsor), the sponsor and venue recaps, and the season-archive tool (freeze + verify).
- Gaps: the organizer's guide (bid to teardown), judge recruiting playbook, day-of run sheet template, music/format ops. **Added (Proposed):** venue contract and COI checklist, hotel-block playbook (cover Fri + Sat, promote early), press playbook with verified contacts, venue pitch pack.

### 3.3 Event kit

Meetups, demos, workshops, school/library programs.

- Have: Event Planning Kit, Workshop Run Sheet (on the club resources page). The Nov 23, 2026 Conway, SC library program is confirmed and is the live test for the playbook.
- Gaps: package them as a kit, school/library-visit guide (write the Conway, SC playbook from running the Nov 23 program), demo scripts, library-partnership pattern (Arlington Central, Loudoun, LibraryFest).

### 3.4 Templates & requirements

The four templates + prerequisite lists + the hub page connecting them. (Fall 2026 Build 6.)

### 3.5 Governance pack

Charter template, officer roles template, code of conduct, budget template, youth protection notes, financial transparency norms. Mostly exists in DMV Throwers docs; the gap is generalizing them into reusable templates.

Dependency: DMV Throwers' own conduct team and report routing must be decided first (BUILD_PLAN 5.2 is blocked on it). The pack can't template a process the reference club doesn't run.

### 3.6 Organizer software

v1 said "nothing like these exists today." That was wrong: VA-States already runs most of it for one contest. The gap is finishing and generalizing. New work lands in yoyo-registration-template first, then ports to VA-States (the repo's "template first, then live" rule).

| Piece | Exists today (VA-States) | Gap | Build |
| --- | --- | --- | --- |
| Volunteers | `/volunteer` signup with roles and shift preferences; `/volunteers` admin | Shift scheduling (T8), briefing email, day-of role cards | 8 |
| Sponsors | `/sponsors` with prospect, contacted, committed, paid and declined; a per-sponsor deliverables checklist (`contest_sponsors.deliverables`, label + done, added by hand); `/sponsor` inquiry form with tier slots and an "Add as prospect" step | Fulfillment ledger: deliverables seeded from the tier, with due dates, proof links and an owner, plus a drafted shoutout queue ([spec](specs/03-sponsor-fulfillment-ledger.md)) | 9 |
| Sponsor recaps | 17 recaps built by hand (Sept 30) | Generator from contest and survey data ([spec](specs/04-sponsor-recap-generator.md)) | 5 |
| Stream overlays | `/overlay/schedule`, `/overlay/battle`, `/overlay/side-event` | Live scores and standings overlay (issue #96) | 10 |
| Meetup check-in + passport | — | QR stamps, nickname-only profiles; attendance feeds sponsor data and gamification | Unassigned |
| Loaner library tracker | — | Pairs with throw-it-forward (§10) | Unassigned |

Software that touches contest data lives in/around VA-States; check-in/passport can start on the club site.

### 3.7 Examples

Reference implementations: DMV Throwers (club), VSYC-26 (contest) with the wrap-up page.

## 4. The Exchange (organizer idea-sharing)

The hub's living layer: organizers sharing what worked, segmented by org/event type — state contest directors, club runners, meetup hosts, demo/school program leads. Segmentation matters: a state director's venue-contract problems are nothing like a meetup host's library-room problems.

- **Phase 1:** hosted board for structured retrospectives. Every contest/event using the templates publishes a retro; the retros become the seed content.
- **Phase 2:** peer Q&A per segment. The Exchange lives in the event hub as the central app — calendar and other event features tie in alongside it.

Retro template (Proposed): built from the four VSYC-26 survey audiences (competitor, spectator, volunteer, sponsor) and the recap structure — the numbers, what worked, what to fix, what it cost.

Content rules (Proposed):

- Retros are stored as markdown (versioned, PR-able, portable) and rendered by the board. Seed retros can be written now, before the board exists.
- Moderation runs under the code of conduct.
- Contributions are licensed CC BY 4.0; code stays Unlicense.

## 5. Standards library (long-term)

Standard practices for contests and clubs: sanctioning checklist, division structures, sponsor tiers, volunteer roles, run-of-show, youth-safety baseline, financial transparency norm. Complementary to NYYL — they standardize judging, this standardizes organizing.

Added (Proposed):

- **Open contest results format.** The season-archive `results.json` (already minor-safe) becomes the standard every template emits and the circuit ingests, until NYYL publishes a format. Gap: rows carry a public name and city/state but no stable player key, so cross-contest matching needs one (an opt-in player id, or a documented name + state matching rule).
- **Canonical division map.** One division list plus a per-contest mapping table (VSYC-26 combined Sport/Beginner/Junior and ran X-Division as one group).
- Versioned as v0.x with named editors.

## 6. Player-facing: covered, low priority

Do not rebuild. Trick tracking (Level Up!, Skill Addicts) and collections (Yoyo Collection — open source, YOYOLOG) are covered by existing free apps.

Self-hosted alternatives tier (lowest priority — a self-hosted option, never a replacement):

- Forum — Discourse already exists as open source; package the self-host path.
- Discord-style chat — Mattermost/Revolt/Element exist; package the self-host path.
- Trick tracker — no good open-source equivalent; the only real build candidate in this tier, if ever.

## 7. Where it lives

- **Event hub = the commons and central app.** The Exchange, calendar, kits index, circuit standings and club directory live here: public, cross-organizer, light accounts. Platform: Cloudflare Pages + Workers + D1 with isolated email (its own Resend key), replatformed off Lovable (decided Oct 11, 2026). Leaving Lovable means re-implementing the Supabase RLS policies, edge functions and pg_cron jobs as Workers code, D1 queries and Cron Triggers, so scope it as a rebuild, not a redeploy. The backend today is 12 tables and 13 edge functions (submit, verify, manage, renew, report, geocode, feeds, feed subscriptions, sitemap, service status, admin actions, daily maintenance) ([spec](specs/05-event-hub-cloudflare.md)).
- **Registration platform = the back office (Proposed boundary).** Money, registrations, judging, volunteers and sponsors, scoped per organizer and per event (the approved multi-event design). It publishes public facts — results and events — as feeds the commons reads.
- **Feeds out (Proposed).** The calendar publishes iCal and JSON. Offer the feed to Yoyo Archive rather than compete with its US events list.
- Guides as markdown in a repo (versioned, PR-able); templates stay in their repos.
- Organizer software in VA-States per the Fall 2026 scope, ported to the registration template.
- **Open-source template.** The hub ships as an open-source, self-hostable template — anyone can host their own hub, and other hobbies can copy and adapt what they like.

## 8. Priority stack & sequencing

1. Spec the hub (this document).
2. Build: net-new gap filling first — organizer software, kits, Exchange phase 1, governance pack.
3. Self-hosted alternatives last.

Spec-first for each piece; build once specs exist. Markdown work (kits, governance pack, seed retros) doesn't wait on app work.

## 9. Decisions and open questions

Decided:

- **Hub location** — the event hub is the central app (Oct 11, 2026).
- **Exchange phase 1 format** — hosted board (Oct 11, 2026).
- **Standards library seeding** — Brandon creates the initial seeds from VA States and DMVT (clubs + contests); others contribute after (Oct 11, 2026).
- **Governance** — everything rides under DMV Throwers; no separate charter (Oct 11, 2026).
- **Event hub platform** — Cloudflare Pages + Workers + D1, isolated email, built as a Cloudflare reference architecture (Oct 11, 2026).
- **Plan location** — this spec and its build plan live in `dmvthrowers.github.io/docs/hub/` as the single source agents read (Oct 11, 2026).

Open (raised in v1.1):

- Approve the commons / back-office boundary (§7)?
- Adopt the youth-safe and outlives-its-founder principles (§1)?
- Who is on DMV Throwers' conduct team (§3.5)?
- Back-test OpenSkill against the v0 power ranking before the NYYL pitch (§11)?
- Who holds circuit prize money, and who sits on the circuit committee (§11)?
- CC BY 4.0 for Exchange contributions (§4)?
- Design partners: the Bmore and SWVA Throwers organizers, one juggling club?

## 10. Community building ideas (parking lot)

Net-new community building is the highest build priority. These are captured here for speccing later:

- **Multi-club by design.** Build the hub, passport, and event calendar for the sister-club network (Bmore, DC Kendama, Seven Cities, SWVA), not just DMV Throwers. Every club that adopts the templates becomes a distribution channel. (Connects to §7.)
- **New-player journey.** Top of funnel (demos, school programs, beginner checklists) and the core (meetups) exist; the middle is undefined. Design the welcome sequence: buddy pairing, second-visit nudge, early passport stamps. Check-in data will show where people drop off. (Connects to §3.1, §3.6.)
- **Demo-in-a-box.** Productize the library-demo playbook (Conway, SC) into a kit any member can run: 45-minute script, loaner-set checklist, handout, booking email template. Turns one ambassador into ten. (Connects to §3.3.)
- **Content drumbeat.** Point the Local-AI media pipeline at community content, not just contests: auto-generated meetup recaps, member spotlights, trick of the month. A club that publishes weekly feels alive. (Connects to §3.6, Fall 2026 Builds 3–4.)
- **Sponsor-funded challenges.** Monthly trick challenges with product prizes from sponsors. Sponsors get visibility, players get stakes, and the sponsor pipeline funds the fun directly. (Connects to §3.6, Builds 5/9.)
- **Challenge platform (from the forums).** Trick-a-Week threads ran 52 weeks and thousands of posts (MoonageMin & Twitch 2020); Modern Responsive March added weekly lists, video submissions, and prize draws. The format is proven, the mega-thread isn't. A dedicated home: weekly trick, submissions, archive, drawings.
- **Throw-it-forward (yoyo drive).** Forum history: one member's drive sent 44 throws to NH Yo-Yo Club, which grew and ran its first contest. A structured donation pipeline: donate old throws to school programs, new players, and clubs in need. Pairs with the loaner tracker.
- **Mentorship matching.** Forum wisdom from gifting threads: give to people you can stick around for as a mentor. Pair new players with experienced throwers; ties into the new-player journey.
- **Charity throwdown (event format).** Forum-proven: entry fees go to charity, a donated yoyo is the prize, companies chip in. A charity-contest playbook for the event kit.
- **Trick graph (mount-to-mount).** The one novel data model nobody's built: navigate tricks by starting/ending mount ("what can I learn from a 1.5?"). Player-facing, low priority — parked.
- **Regional circuit.** A traveling meetup series across sister clubs; the passport tracks the tour. (Connects to multi-club by design.)
- **State of the Scene (annual report).** Attendance, new players, contests — published yearly. Feeds sponsors and the standards library. Generated by the same engine as the sponsor recaps (Build 5).
- **Online event template (from the Boomer Club playbook).** Generalize the YYBC themed-month online events (Fixed Axle February, Modern Responsive March, 2April, 5A May) into a reusable template: the three-tier format (beginner trick ladder — 3 tricks/week, per-trick entries plus a completion bonus; intermediate trick-a-week; free-form/creative category for original content, combos, and tutorials), video-submission-as-entry prize drawings, trick lists with member-presented tutorial videos, weekly hype posts, forum thread as HQ plus Discord for help, and the two-tier sponsor package (donors get thread + video mentions; sponsors get logo on video banners, social posts, Linktree link, ship-direct-to-winner, and discount-code support). Source: YYBC Full Reference and Charter (Drive).
- **Online contest format (ANTE YoYo Cup as reference).** A true judged online contest, distinct from the challenge format: video freestyle submissions by division (1A Pro, 1A Sport, X divisions, plus a two-player Duo division), prelims and finals, a multi-day streamed watch party with same-day results, and a 100% sponsor-funded prize pool with published splits (e.g. 1A Pro 40/25/15/10/10%, Duo 1st $100 cash) — organizers take no personal cut. YYBC already sponsors ANTE (Bronze, from merch/proto funds), so the relationship is warm.
- **Judge pool registry (Proposed).** Opt-in, cross-state list of NYYL-certified judges and their availability. The 1A panel was finalized day-of at VSYC-26 (#91), and the circuit standard requires certified judges.
- **Regional sponsor directory (Proposed).** Opt-in list of brands that back events: tiers, what they valued, public contact only. VSYC-26 had 17 sponsors, several new to sponsoring.
- **Verified press list (Proposed).** Shared, checked media contacts per metro, plus a press-kit generator. Three VSYC-26 press addresses bounced (#93).
- **Venue pitch pack (Proposed).** A "why host a yo-yo contest" deck with real numbers — attendance, dwell time, spend, sentiment — from the Dulles Town Center recap. Malls are an underused venue class.

## 11. State Contest Circuit (proposal draft)

A voluntary season-long circuit across participating state contests. NASCAR-style: win a track, but the season title goes to the most consistent performer across judged results. Gives players a reason to travel to multiple states, gives state contests a bigger story, and feeds NYYL regionals a healthier pipeline.

### Two ranking systems

The circuit runs two complementary rankings:

- **Season points (NASCAR-style):** the title race. Simple, fan-friendly: placement points per contest, best results count, consistency wins seasons. This is what players follow week to week.
- **Power ranking:** the analytical rating. A cross-contest skill measure that weights who you beat and the strength of the field, updated per contest. This is what backs the seeding case to NYYL. (v1 called this "Elo"; the v0 formula isn't Elo, see below.)

### How it works

- **Participating contests:** any state contest run to the circuit standard (see sanction-ready checklist).
- **Scoring:** placement points per division from official judged results, NASCAR-style descending scale — 1st=40, 2nd=35, 3rd=34, 4th=33, descending by 1 per place. Plus 5 participation points per contest entered.
- **Season total:** best 4 of up to 6 contests count, so players aren't punished for missing events.
- **Tiebreaks:** most wins, then highest single-contest score, then head-to-head.
- You can win a track and lose the season — consistency beats single wins, exactly like NASCAR.

Rules to close (Proposed defaults):

- **Field size:** full points at 8+ entrants in a division; below that, points scale by entrants ÷ 8. First of 3 shouldn't equal first of 32.
- **Participation points:** count for every contest entered (up to 6, so 30 max), on purpose, as the travel incentive.
- **Floor:** placement points never drop below 1.
- **Head-to-head:** "finished ahead in the contests both entered"; if they share none, go to the next tiebreak.
- **Divisions:** scored through the canonical division map (§5).

### Power ranking methodology

**v0 (iantheman60 formula).** Adapted from the community-run NYYL 1A Pro Power Ranking (iantheman60, 2024) — the working prototype this circuit generalizes beyond 1A Pro:

- **Base:** every competitor starts at 1000 at their first contest of the year; fresh start each season.
- **Contest value (time-dependent):** average competitor rating ÷ number of competitors = x; placement points descend from x/2 − 1 (1st takes the top value, −1 per place).
- **Round multiplier:** prelims = points + #competitors; 2-min final = points + (#competitors × 1.3); 3-min final = points + (#competitors × 1.5). Finals-only contests use the prelim multiplier.
- **Top-5 multiplier:** 1st ×1.5, 2nd ×1.4, 3rd ×1.3, 4th ×1.2, 5th ×1.1.
- **Final-score multiplier:** value × (1 + finalScore/100), the 1–2x range.
- **Adjustments:** nationals use a 2 − 0.1×place scale for the top 10; contests with <10 competitors use scaled deductions; if more than 5 newcomers sit at base 1000, only one counts toward the field average.
- **Scope:** NYYL-judged contests only — the same filter as the sanction-ready checklist.

Known issues with v0:

- It only adds points, so a rating never falls after a bad result. That makes it a points ranking, not Elo.
- Dividing by field size rewards small fields. At an average rating of 1000, a prelim and a final score of 90, a 6-person win is worth 251.8 and a 20-person win 125.4.
- Raw final scores aren't comparable across contests: VSYC-26's winners scored 95.50 (1A), 91.00 (X) and 74.03 (Sport). Use score relative to the field or the winner.

**Under evaluation (Proposed): OpenSkill.** An open-source rating system for ranked multiplayer results (Weng-Lin, the TrueSkill family). Each placement counts as wins over everyone below and losses to everyone above, so field strength is handled automatically. Each player carries a skill and an uncertainty, which removes the newcomer patch; publish the conservative rating (skill − 3 × uncertainty). Plan: back-test v0 and OpenSkill on 2024–26 results with iantheman60, then pick one for the NYYL pitch.

### Divisions

Standard NYYL divisions, plus a proposed intermediate **Advanced** division between Sport/Amateur and Pro. Eligibility: never placed top-3 in Pro at a regional or higher. Keeps traveling talent from farming local amateurs; gives competitive non-pros a home. (Standards library item. Checking eligibility needs a results history — the circuit's own results data.)

### Incentives (low-cost)

- **Points series + season standings** on the hub (free) — the prestige engine.
- **Participation raffle:** each contest entered = tickets; season-end drawing for sponsor-donated throws (near-free; sponsors donate product, not cash).
- **Iron thrower status:** compete in 3+ states in a season → title + patch (free).
- **Optional circuit fee:** $2–3 per registration at participating contests → season prize pool. Deferred until the circuit proves itself; start with sponsor product. Before any fee: name the custodian, publish the ledger and the payout rules.
- **Competitive incentive:** circuit results feed regional prelim-bypass agreements (needs NYYL + regional directors).

### Sanction-ready checklist (what NYYL needs)

- Judging run to the current NYYL freestyle ruleset, with NYYL-certified judges.
- Standard divisions matching the regional's.
- Results reported in NYYL Compete's format, or the open contest results format (§5) until NYYL publishes one.
- Note: no published NYYL sanctioning checklist found as of Oct 2026 — this draft is meant to start that conversation.

### Seeding proposal

Circuit champion (and/or top-3) in each division bypasses prelims at their home regional. Requires NYYL and regional director agreement.

### Governance

Neutral operator (proposed: the organizer hub). Opt-in per contest per season. Season calendar published before the season; standings updated after each contest. **Circuit committee (Proposed):** DMV Throwers runs VSYC, so a "neutral" operator needs at least two other state directors on a small committee that owns the rules.

### Asks

- **Of NYYL:** recognize the circuit, endorse the sanction-ready standard, agree seeding terms, coordinate calendar.
- **Of state organizers:** opt in, run to the standard, report results in the standard format, and share 2026 results for the back-test.

### Timeline (proposed)

Draft Oct 2026 → back-test on real results → present to NYYL + state organizers winter 2026–27 → pilot season 2027.

### Seed relationships

Virginia, Indiana (Indy States wants Oct 23, 2027; VSYC-27 avoids that weekend), Minnesota, Colorado, Michigan. Existing organizer relationships to seed the pilot; contacts are in the Drive copy.

**Methodology:** iantheman60, creator of the community NYYL 1A Pro power ranking — natural collaborator on the power ranking and the back-test.

## Changes in v1.2 (Oct 12)

- Links to `REFERENCE.md` and the draft specs in `specs/`.
- §3.6: the sponsor deliverables checklist already exists; Build 9's gap narrowed to tier-seeded deliverables, due dates, proof and a shoutout queue.
- §5: results format needs a stable player key for circuit matching.
- §7: event hub rebuild sized at 12 tables and 13 edge functions.

## Changes in v1.1

- §1: two proposed principles — youth-safe by default; outlives its founder.
- §2: fourth path for online events; each path states time, money and people.
- §3.1–3.3: added existing source material (filings, Financial Infrastructure Guide, surveys, recaps, archive tool, Nov 23 Conway program) and new gaps (make it official, venue/COI, hotel block, press, venue pitch, library partnerships).
- §3.5: governance pack depends on the DMV Throwers conduct team decision.
- §3.6: corrected "nothing exists" — table of what VA-States already has and the real gap per build; template first, then VA-States.
- §4: retro template, markdown storage, moderation and license (proposed).
- §5: open contest results format and canonical division map (proposed).
- §7: commons / back-office boundary (proposed); Cloudflare + D1 recorded as decided, scoped as a rebuild; feeds out to Yoyo Archive (proposed).
- §9: renamed to decisions and open questions; added the Cloudflare and plan-location decisions and seven open questions; removed empty bullets.
- §10: four new parking-lot ideas; State of the Scene tied to the recap engine.
- §11: "Elo" renamed power ranking; v0 issues documented; OpenSkill back-test proposed; five season-points rules proposed; fee custody and circuit committee; Indiana date confirmed as 2027.
