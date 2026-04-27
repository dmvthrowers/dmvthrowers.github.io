# AGENTS.md

Contributor notes for `dmvthrowers.github.io` — the source for **dmvthrowers.club**.

## What this is

A hand-maintained static site served by GitHub Pages at a custom domain. No build step, no Jekyll (`.nojekyll` is present), no templating engine, no JS framework. Every page is a standalone `.html` file that repeats the same top bar / nav / mobile menu / footer boilerplate.

Two clusters of pages share a common look but live in separate stylesheets:

- **Main club site** — `index.html`, `about.html`, `team.html`, `events.html`, `gallery.html`, `resources.html`, `faq.html`, `contact.html`, `privacy.html`, `code-of-conduct.html`, `404.html`. Uses `assets/css/main.css`.
- **VSYC-26 contest sub-site** — `vsyc26.html` and `vsyc26-*.html` (schedule, register, sponsors, venue, rules, faq, terms). Uses `assets/css/vsyc26.css`.

One shared JS file (`assets/js/mobile-enhancements.js`) is loaded on every page for progressive enhancement.

## Page map

### Main site

| Page | Purpose |
| --- | --- |
| `index.html` | Landing page — big hero, about, upcoming highlights, sponsors, CTA |
| `about.html` | About the club. **Canonical footer template — copy its footer structure when editing others.** |
| `team.html` | Officers + member cards. Placeholder cards use emoji `🪀` inside an `aria-hidden="true"` div |
| `events.html` | Monthly meetups + special events + holidays. **Hand-sorted by date; keep chronological** |
| `gallery.html` | Photo grid with `<picture>` WebP + PNG fallbacks and `width`/`height` to reserve layout |
| `resources.html` | Links to PDFs in `assets/documents/` + external yo-yo resources |
| `faq.html` | Accordion with inline `toggleFaq` script + matching `FAQPage` JSON-LD |
| `contact.html` | Formspree-backed contact form (form-action locked to a specific endpoint) + honeypot field |
| `privacy.html` | Privacy policy body; long-form static content |
| `code-of-conduct.html` | Community code of conduct with a version tag + effective date |
| `404.html` | Custom "page not found"; `noindex,follow` |

### VSYC-26 contest sub-site

| Page | Purpose |
| --- | --- |
| `vsyc26.html` | Landing — hero with live countdown + Event JSON-LD |
| `vsyc26-schedule.html` | Day-of schedule |
| `vsyc26-register.html` | Divisions + JotForm registration embed |
| `vsyc26-sponsors.html` | Tiers + current-sponsor list + JotForm inquiry embed |
| `vsyc26-venue.html` | Venue details (Dulles Town Center · Center Court) |
| `vsyc26-rules.html` | Contest ruleset (freestyle, equipment, music, judging) |
| `vsyc26-faq.html` | Accordion with inline `toggleFaq` + matching `FAQPage` JSON-LD |
| `vsyc26-terms.html` | Competitor terms (refund, waiver, photo release, conduct, minors) |
| `vsyc26-divisions.html` | **Redirect stub** — meta-refresh + JS redirect to `vsyc26-register.html#divisions`. Don't add content here |

## Boilerplate pattern

Every content page repeats the same outer skeleton:

```html
<head>
  charset / viewport / author / <base href="/">
  CSP meta / title / description / OG + Twitter
  favicons / preconnect + font stylesheet
  JSON-LD (BreadcrumbList, sometimes Event / FAQPage / Organization)
  <link rel="stylesheet" href="assets/css/main.css">
  <style> page-specific rules </style>
</head>
<body>
  skip-link
  top bar (NEXT MEET / contest date + shortcut)
  <nav> main nav
  mobile-menu (hidden until .open)
  <main id="main-content" role="main">
    page hero
    content sections
  </main>
  footer (about.html is the canonical structure)
  inline hamburger toggle script
  <script src="/assets/js/mobile-enhancements.js" defer></script>
</body>
```

`aria-current="page"` marks the active nav link on each page.

## Conventions

- **Styles**: shared components + brand variables in `assets/css/main.css`; per-page layout tweaks in each page's inline `<style>` block. Don't migrate page-specific rules to `main.css` unless they're reused.
- **Brand palette**: `--red`, `--navy`, `--cream`, `--border`. Use the variables, not raw hex.
- **Images**:
  - Gallery and hero images use `<picture>` with WebP `<source>` + PNG/JPG fallback `<img>`.
  - `width`/`height` are always set on content images to reserve layout (CLS).
  - Decorative images get `alt=""` + `aria-hidden="true"`. Content images get descriptive alt text.
- **External links**: `target="_blank"` gets `rel="noopener noreferrer"`. The JS enforces this as a safety net, but add it in the HTML too.
- **Formspree contact form**: the CSP `form-action` is locked to a specific Formspree endpoint; changing endpoints means updating `contact.html`'s CSP meta tag.
- **JSON-LD**: every page has a `BreadcrumbList`. The landing pages add an `Event` (vsyc26.html) or `Organization` (index.html); FAQ pages add `FAQPage`. JSON-LD is consumed by search engines, not rendered.

## Gotchas

- **`<base href="/">` affects every relative URL on the page.** When adding a link, assume root-relative paths. Test with the custom domain, because file:// and some local servers behave differently.
- **CSP meta tags block every external origin that isn't listed.** Adding a new embed (new form provider, new font host, new analytics) means updating the `<meta http-equiv="Content-Security-Policy">` tag on *every page that needs it* — there's no global config.
- **Event cards on `events.html` are hand-sorted by date.** When adding or updating cards, keep chronological order and update the JSON-LD `Event` entries to match.
- **Footer structure has been standardized.** If you're building a new page, copy `about.html`'s footer exactly — don't improvise. The main-site footer and the VSYC-26 footer have different structures; don't mix.
- **FAQ pages have the questions duplicated in JSON-LD.** If you change the visible Q/A, change the `FAQPage` schema too.
- **`vsyc26-divisions.html` is a redirect, not a content page.** If you want to update division info, edit `vsyc26-register.html` instead.
- **`.nojekyll`** prevents GitHub Pages from running its default Jekyll processing. Don't remove it unless you want Jekyll to start mangling files.

## How to add a new main-site page

1. `cp about.html newpage.html`.
2. Update `<title>`, `<meta name="description">`, OG/Twitter tags, `<link rel="canonical">`, and the `BreadcrumbList` JSON-LD.
3. Replace the page hero + main content with the new page's content.
4. Add a nav link to the new page on every other page, and set `aria-current="page"` on the matching link within the new page.
5. Add a footer link to the new page on every other page (footers list all pages; keep them in sync).
6. Load it over the local dev server and check that the skip link, hamburger, and footer all work.

## Local preview

Any static file server from the repo root works. The `<base href="/">` means root-relative paths only resolve correctly when served from the root.

```sh
python -m http.server 8000
# or
npx serve .
```

Then open `http://localhost:8000/`.

## Where things live

- `assets/css/main.css` — shared main-site styles. Sectioned with `===== N. Name =====` banners.
- `assets/css/vsyc26.css` — VSYC-26 sub-site styles.
- `assets/js/mobile-enhancements.js` — shared progressive-enhancement layer (deferred; idempotent).
- `assets/images/` — logos, hero art, sponsor logos, team placeholders, favicons.
- `assets/documents/` — PDFs linked from `resources.html`.
- `CNAME` — custom-domain config for GitHub Pages.
- `robots.txt` + `sitemap.xml` — SEO plumbing.
