# Share cards

`cards.html` is the source for the two link-preview images:

- `assets/images/og/dmvt-share.png`: the club (Playfair Display and DM Sans)
- `assets/images/og/vsyc26-share.png`: VSYC-26 (Montserrat)

Both are 1200 x 630 and use the self-hosted fonts in `assets/fonts/` through `assets/css/fonts.css`.

To change the wording or the logo, edit `cards.html`, then regenerate:

```sh
npm install playwright            # once, anywhere you like; or use a global install
node scripts/share-cards/render.js
```

If Playwright can't find a browser, point `CHROMIUM_PATH` at a Chromium or Chrome binary.
Check the two PNGs by eye and keep them under 500 KB. Date, venue and place on the VSYC card must
match `vsyc26.html`.

Social sites cache preview images. After you change a card, ask the site to refresh it (for example
Facebook's Sharing Debugger) or rename the file and update the `og:image` and `twitter:image` tags.
