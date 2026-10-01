<!--
  Reference copy of the dmvthrowers.github.io Claude Code spec, added 2026-10-01.
  The spec below is verbatim. Status as of 2026-10-01:
  1. OSV-Scanner workflow -> pending: v2.5.1 and v2.6.0 both hit startup_failure; delete osv-scanner.yml (Brandon)
  2. Dependabot #67       -> merged
  3. Photo audit #110     -> merged
  4. Split mega-pages     -> merged in #111 (link check 0 broken before/after)
  The "no GitHub token" delivery note is outdated: PRs were opened from the session.
-->

---

# dmvthrowers.github.io — Claude Code specs

Repo: `dmvthrowers/dmvthrowers.github.io` (club site, dmvthrowers.club).
Pure static HTML, GitHub Pages, no build step, ~35 pages. README and AGENTS.md/CLAUDE.md rule files exist — read them before starting.

**Delivery mechanism (all items below):** Work on a `claude/<short-name>` branch, push the branch, and open a PR from it. Brandon reviews and merges on GitHub. You do not have a GitHub token; do not try to open issues or PRs via the API. Pushing a branch and opening the PR from the checked-out checkout with `gh` will not work without auth — instead, describe the PR-ready state in your final report to Brandon (branch name + summary + test evidence) and he will open it.

---

## 1. Fix or remove the OSV-Scanner workflow

**Context:** `.github/workflows/osv-scanner.yml` fails at startup on every run, including main. This is a static HTML site with no lockfiles (only `environment.yml` with `python=3.10`), so the scanner produces roughly zero value — it's permanently red noise.

**Task:**
1. Open `.github/workflows/osv-scanner.yml` and identify the pinned reusable-workflow SHA / `osv-scanner-action` version.
2. Check whether a newer osv-scanner-action release exists that still starts successfully on this repo's content (scan-only repos with no lockfiles often just no-op).
3. Decide, in this order:
   - If a newer pinned release starts and passes on a test branch, bump the SHA and merge.
   - If no release behaves sanely on lockfile-free static content, **delete `osv-scanner.yml` outright.** Do not replace it with a different scanner — this site has nothing to scan.

**Acceptance criteria:**
- Either the workflow is green on a test run against main, or `osv-scanner.yml` no longer exists.
- All other workflows (Lint, CodeQL, Pages deploy) still pass unchanged.
- No other workflow files are modified.

**Constraints/risks:**
- If deleting: keep the rest of `.github/workflows/` untouched. Do not touch CodeQL or Dependabot configs in the same change.
- Do not add new dependencies to "fix" the scan.

---

## 2. Resolve dependabot PR #67 (patch-and-minor group)

**Context:** Dependabot PR #67 has been sitting since Sep 21. The repo has no `package.json`, so this is almost certainly just GitHub Actions version bumps.

**Task:**
1. Read the PR diff. Confirm every change is a GitHub Actions version bump (or equivalent maintenance) with no code changes.
2. If clean: rebase onto main, verify CI passes, merge. If anything in the diff is not a version bump, or if rebasing is messy: close it with a one-line justification comment and move on.

**Acceptance criteria:**
- PR #67 is merged or closed, and the justification is recorded in the PR (merge commit or close comment).
- If merged: all workflows green on main after merge.

**Constraints/risks:**
- Ten-minute job. Do not expand scope — no refactoring around the bumps, no updating unrelated pins in the same PR.

---

## 3. Finish and ship PR #110 (photo audit: real photos over AI images)

**Context:** PR #110 is a draft replacing AI-generated images with real club/contest photos. Brand authenticity matters for this club — real photos win.

**Task:**
1. Check out the PR branch. Enumerate every image the PR touches and every page that references them.
2. Verify: no broken `<img>` references (search the whole repo for each filename), every image has meaningful `alt` text (no empty or "image" placeholders), file paths are consistent with the repo's existing asset layout (don't introduce a new asset directory convention).
3. Confirm licensing/source is sane for real photos (club's own photos or credited; flag anything questionable in the PR description).
4. If everything checks out: mark the PR ready for review (you can't flip the draft flag without auth — note the branch name in your report to Brandon and tell him it's ready for him to mark ready and merge).

**Acceptance criteria:**
- Zero broken image references across the repo (a link checker or a grep pass over all `src=` values counts as evidence).
- Every touched image has descriptive `alt` text.
- No new asset directory conventions; paths match the existing layout.
- PR description lists what changed and flags any photo of uncertain provenance.

**Constraints/risks:**
- Don't resize or recompress images unless they're absurdly large (>1MB each is worth noting in the PR, not fixing unilaterally).
- Don't touch pages the PR didn't already touch.

---

## 4. Split the mega-pages: learn-yoyo.html (141KB) and yoyo-gear.html (197KB)

**Context:** Two single-file pages are unwieldy. Split them mechanically into sub-pages — no redesign, no content changes, just decomposition.

**Task:**
1. Read each page fully. Map its top-level sections (headings / logical blocks) and every internal anchor (`#...`) plus every inbound link from other pages.
2. Propose a split (e.g., one sub-page per major section) in a short plan note at the top of your report to Brandon — do the split in a `claude/split-megapages` branch.
3. For each sub-page: preserve all content verbatim, preserve styling (same CSS/includes as the original), keep the site nav identical, and add a small section index at the top of the parent page linking to each sub-page.
4. Update all inbound links (repo-wide grep for the old filenames and their anchors) so nothing points at sections that moved. Preserve anchor IDs on the new pages so external/deep links keep working.
5. Run a link checker (e.g., `htmlproofer` or equivalent) over the built site and report the result.

**Acceptance criteria:**
- Byte-identical content modulo the split (no lost text, no lost images, no altered wording).
- Every internal anchor still resolves; every inbound link still resolves.
- Link checker reports zero new broken links (report the before/after counts).
- Nav, header, footer, and styling identical to the original pages.

**Constraints/risks:**
- This is a mechanical split, not a rewrite. Do not "improve" the copy or restyle anything.
- Work page by page: finish learn-yoyo.html first, verify, then yoyo-gear.html — or split into two branches if the change gets large.
- Don't touch any other page's content.
