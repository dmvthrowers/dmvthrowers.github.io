# Spec 01: Organizer Front Door Page

**Status:** Draft, needs Brandon's approval · **Repo:** dmvthrowers.github.io · **Lane / phase:** A / 3 (spec §2, §3.4) · **Fall build:** 6 · **Size:** 1 session

## Problem

Five templates, a kit's worth of documents and two live apps exist, but an organizer from another city has no single place to start. The hub shell (event hub, Phase 1) is blocked on Cloudflare. A static page on the club site can be the front door now and move to the hub later.

## Scope

In: one new page, `organize.html`, with four paths; a card on `guides.html`; a link in the footer GUIDES row on every page; sitemap entry.
Out: a main-nav item (nav stays identical; adding one is a separate decision), new kit content (spec 02 and later), any app.

## Content

Hero: "Start Something in Your Town" · one line: "Free guides, templates and tools for skill toy clubs, contests and events. All built and tested by DMV Throwers."

Four path cards, each with **what it takes** (time, money, people), the steps in order, and links. The time, money and people figures below are draft estimates for Brandon to confirm before launch:

| Path | What it takes | Steps and links |
| --- | --- | --- |
| Start a club | About 30 minutes for the site; $0; 1–2 people to start | Club kit (spec 02 follow-on) → `yoyoclub-template` → charter and officer roles (`assets/documents/`) → code of conduct |
| Run a contest | 3–6 months; budget depends on venue; 5–10 volunteers | Contest kit (later) → `yoyo-contest-template` → `yoyo-registration-template` → VSYC-26 recap as the worked example |
| Host a meetup or demo | A few hours; loaner yo-yos; 1–3 people | Event kit (spec 02): Event Planning Kit, Workshop Run Sheet, school/library playbook |
| Run an online event | Weekly posts for a month; sponsor prizes optional | Placeholder card: "Coming next" with a one-line description (spec §10) |

Below the paths: "Find others" (player map, the US events list, sister clubs on `resources.html#clubs`) and "Tell us what worked" (contact link, later the Exchange).

Kits that don't exist yet show "Coming soon", not dead links.

## Build rules

- Copy `about.html`; follow `CLAUDE.md` "How to add a new main-site page" except step 4 (no nav item). Breadcrumb JSON-LD: Home › Guides › Start Something.
- Brand: `main.css` variables, sharp corners, no card shadows, Title Case headings, second person.
- Links root-relative; external links `target="_blank" rel="noopener noreferrer"`.

## Acceptance criteria

- [ ] `organize.html` renders at 360 px wide with no horizontal scroll.
- [ ] Card on `guides.html`; link in the footer GUIDES row on every page (footers identical).
- [ ] `sitemap.xml` has the page with today's `lastmod`.
- [ ] No link points at a file or page that doesn't exist; unbuilt kits say "Coming soon".
- [ ] `python3 scripts/check_site.py` and the W3C validator pass; axe shows no new findings.

## Open questions for Brandon

- Page name: `organize.html` or `start.html`?
- Add ORGANIZE to the main nav now, or after the kits exist?

## Claude Code handoff

```
Repo: dmvthrowers.github.io. Read CLAUDE.md and docs/hub/specs/01-front-door.md.
Create organize.html from about.html with the hero, four path cards (with the
"what it takes" line and ordered links), Find Others and Tell Us sections, exactly
as specced. Do not add a main-nav item. Add a card to guides.html and a link to the
footer GUIDES row on every page. Add the sitemap entry. Mark unbuilt kits "Coming
soon". Run python3 scripts/check_site.py and check 360 px width. Branch
claude/organizer-front-door, prefix feat(guides):, PR lists each acceptance criterion.
```
