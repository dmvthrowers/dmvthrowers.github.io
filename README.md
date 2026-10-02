# DMV Throwers · Yo-Yo & Skill Toy Club

**The Washington DC, Northern Virginia, and Maryland yo-yo and skill toy community.**

**Website:** [dmvthrowers.club](https://dmvthrowers.club)
**YoYo Player Map:** [map.dmvthrowers.club](https://map.dmvthrowers.club)
**Instagram:** [@dmv_throwers](https://instagram.com/dmv_throwers)
**Linktree:** [linktr.ee/dmvthrowers](https://linktr.ee/dmvthrowers)
☕ **Support us:** [ko-fi.com/dmvthrowers](https://ko-fi.com/dmvthrowers)

Last updated: 2026-10-02

---

## About the Club

DMV Throwers is a free, community-run yo-yo and skill toy club serving the DC, Maryland, and Virginia area. Founded in 2021, we host free monthly meetups at Arlington Central Library in Arlington, VA — open to all ages and skill levels, from total beginners to competitive players.

We welcome yo-yo, kendama, diabolo, juggling, and all skill toys. All ages, all levels, always free.

---

## Monthly Meetups

- **Every 3rd Sunday · 1–4 PM** (next: Sunday, October 18, 2026)
- **Arlington Central Library** · Barbara M. Donnellan Auditorium
- 1015 N Quincy St, Arlington, VA 22201
- **Free to attend · No registration required · Loaner yo-yos available**

The NEXT MEET banner and past meetup cards are advanced automatically each week by `scripts/update_meetup.py` (`.github/workflows/update-meetup.yml`).

---

## VSYC-26 · Virginia State Yo-Yo Contest 2026

The **16th annual Virginia State Yo-Yo Contest** was held **September 19, 2026** at **Dulles Town Center · Center Court · Sterling, VA**, brought to you by Goodles. Results, recap and videos are up:

- **Contest hub:** [dmvthrowers.club/vsyc26.html](https://dmvthrowers.club/vsyc26.html)
- **Results:** [dmvthrowers.club/vsyc26-results.html](https://dmvthrowers.club/vsyc26-results.html) · full leaderboard at [register.dmvthrowers.club/results](https://register.dmvthrowers.club/results)
- **Recap:** [dmvthrowers.club/vsyc26-recap.html](https://dmvthrowers.club/vsyc26-recap.html)
- **Sponsor inquiries:** <vastateyoyocontest@gmail.com>

VSYC-27 planning is tracked in this repo's issues (#76–#96).

---

## Contact

| | |
| --- | --- |
| **Club Email** | <contact@dmvthrowers.club> |
| **Contest Email** | <vastateyoyocontest@gmail.com> |
| **Phone** | 850-284-1613 |
| **Instagram** | @dmv_throwers |
| **Coordinator** | Brandon Rogers |

---

## Site Structure

| Section | Pages |
| --- | --- |
| Club | [Home](https://dmvthrowers.club) · [About](https://dmvthrowers.club/about.html) · [Team](https://dmvthrowers.club/team.html) · [Events](https://dmvthrowers.club/events.html) · [Gallery](https://dmvthrowers.club/gallery.html) · [Resources](https://dmvthrowers.club/resources.html) · [FAQ](https://dmvthrowers.club/faq.html) · [Contact](https://dmvthrowers.club/contact.html) · [Privacy](https://dmvthrowers.club/privacy.html) · [Code of Conduct](https://dmvthrowers.club/code-of-conduct.html) |
| Guides | [How to Yo-Yo](https://dmvthrowers.club/learn-yoyo.html) (4 parts) · [Gear & Maintenance](https://dmvthrowers.club/yoyo-gear.html) (4 parts) · [Science & DIY](https://dmvthrowers.club/yoyo-science.html) · [History](https://dmvthrowers.club/yoyo-history.html) · [Collecting](https://dmvthrowers.club/yoyo-collecting.html) · [Filipino Yo-Yo History](https://dmvthrowers.club/filipino-yoyo-history.html) |
| VSYC-26 | [Hub](https://dmvthrowers.club/vsyc26.html) · [Results](https://dmvthrowers.club/vsyc26-results.html) · [Recap](https://dmvthrowers.club/vsyc26-recap.html) · [Schedule](https://dmvthrowers.club/vsyc26-schedule.html) · [Divisions & Register](https://dmvthrowers.club/vsyc26-register.html) · [Rules](https://dmvthrowers.club/vsyc26-rules.html) · [Venue](https://dmvthrowers.club/vsyc26-venue.html) · [Sponsors](https://dmvthrowers.club/vsyc26-sponsors.html) · [Dueling Stars](https://dmvthrowers.club/vsyc26-dueling-stars.html) · [Twirly Tour](https://dmvthrowers.club/vsyc26-twirly-tour.html) · [Merch](https://dmvthrowers.club/vsyc26-merch.html) · [FAQ](https://dmvthrowers.club/vsyc26-faq.html) · [Terms](https://dmvthrowers.club/vsyc26-terms.html) |
| Other club apps | [YoYo Player Map](https://map.dmvthrowers.club) ([repo](https://github.com/dmvthrowers/yoyo-player-map)) · [Contest registration](https://register.dmvthrowers.club) ([repo](https://github.com/dmvthrowers/VA-States)) |

The full page map, boilerplate pattern and gotchas are in [`CLAUDE.md`](CLAUDE.md) (identical to [`AGENTS.md`](AGENTS.md)).

---

## Working on the Site

Static HTML/CSS/JS on GitHub Pages — no build step. Preview from the repo root (the pages use `<base href="/">`, so they must be served from the root):

```sh
python -m http.server 8000   # then open http://localhost:8000/
```

Optional local guards: `pip install pre-commit && pre-commit install` (protects `CNAME`, flags off-brand colors, border-radius, shadows, new font hosts and tracking scripts).

Never edit `CNAME` — it must stay `dmvthrowers.club`.

```text
/ (root)                 every .html file is a live page
├── assets/css/          main.css (club site), vsyc26.css (contest pages)
├── assets/js/           mobile-enhancements.js (the only shared script)
├── assets/images/       logos, favicons, events/, gallery/, history/, vsyc26*/ photos
├── assets/documents/    charter, press kit, trick checklists, run sheets
├── assets/videos/       local video files
├── scripts/             update_meetup.py (weekly NEXT MEET update)
├── docs/                cross-repo overview + roadmap (not deployed)
├── sitemap.xml, robots.txt, CNAME, .nojekyll
└── .github/workflows/   Pages deploy, CodeQL, super-linter, meetup update, hygiene bots
```

---

## Docs

- [`CLAUDE.md`](CLAUDE.md) / [`AGENTS.md`](AGENTS.md) — contributor rules and page map
- [`docs/README.md`](docs/README.md) — how the five club repos and shared services fit together
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — open work for the site
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Full October 2026 technical audit (Google Drive, access-restricted): [Technical docs - Oct 2026](https://drive.google.com/drive/folders/1Jt7amThKNkeVJenksPtA87cBtR-nwZiq)

---

DMV Throwers · Est. 2021 · DC · MD · VA · @dmv_throwers
