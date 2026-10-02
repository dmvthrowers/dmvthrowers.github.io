# Contributing to DMV Throwers

Thank you for helping improve the DMV Throwers website.
This project is community-driven, and contributions of all sizes are welcome.

## Purpose

Our goal is to keep the site accurate, accessible, and helpful for players, families, and organizers across DC, Maryland, and Virginia.

## Ways to Help

We welcome contributions such as:

- Updating meetup and contest details
- Improving copy clarity and accessibility
- Fixing broken links and formatting issues
- Adding youth-safe learning resources
- Improving performance, SEO, or mobile behavior
- Submitting photos or media you have rights to share

## Before You Start

- Open an issue for significant changes so we can align first
- Check existing issues and pull requests to avoid duplicate work
- Follow the current structure and naming conventions in this repository
- Keep changes focused and easy to review

## Pull Request Checklist

1. Fork the repository and create a branch for your change.
2. Make edits with clear, minimal diffs.
3. Verify pages render correctly on desktop and mobile.
4. Confirm links, dates, and contact details are accurate.
5. Open a pull request with a short summary of what changed, why it changed, and screenshots for UI or content updates.

## Local Checks

- Read [`CLAUDE.md`](CLAUDE.md) first: page map, boilerplate, and gotchas.
- Preview with `python -m http.server 8000` from the repo root (pages use `<base href="/">`).
- Install the guards once: `pip install pre-commit && pre-commit install`. They protect `CNAME`
  and flag off-brand colors, rounded corners, shadows, new font hosts and tracking scripts.
- Never edit `CNAME`. Use relative links. Keep the nav identical on every page.
- New or changed pages: update `sitemap.xml` `lastmod`, check the page at 360px wide with no
  horizontal scroll, and give every image alt text (or `alt=""` if decorative).
- Open work is listed in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Content and Media Rules

- Only submit media you created or have explicit permission to use
- Include attribution where required
- Do not upload personal or sensitive information
- Avoid identifiable minors unless you have verified permission

## Code of Conduct

All participation in this project is governed by the Code of Conduct in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

For security issues, do not file a public issue.
Follow the reporting guidance in [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are licensed under this repository's license.
