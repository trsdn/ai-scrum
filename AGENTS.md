# AGENTS.md

Guidance for coding agents working in this repository.

## What this repository is

`trsdn/ai-scrum` is the marketing/documentation website for the **AI-Scrum**
framework — a Scrum-inspired methodology for human-AI collaboration with GitHub
Copilot CLI. It is published at <https://trsdn.github.io/ai-scrum/>.

It is a **hand-written static site**. There is deliberately:

- no package manifest (`package.json`, `requirements.txt`, …),
- no build step, bundler, or transpiler,
- no test suite,
- no framework, no dependencies vendored into the repo.

The framework itself does not live here. It lives in the two template
repositories linked from the site:
[copilot-scrum-autonomous](https://github.com/trsdn/copilot-scrum-autonomous)
and [copilot-scrum-guided](https://github.com/trsdn/copilot-scrum-guided).
Changes to the methodology belong there; this repository only describes it.

## Layout

```
.
├── index.html            # The entire site — one page, section-per-topic
├── assets/
│   ├── css/style.css     # All styling
│   └── js/main.js        # All behaviour (scroll reveal, nav, smooth anchors)
├── .nojekyll             # Disables Jekyll processing on GitHub Pages
├── CHANGELOG.md
├── LICENSE
└── .github/
    ├── workflows/        # ci.yml, release.yml
    ├── scripts/          # check_site.py, extract_changelog.py
    ├── linters/          # html-validate.json
    └── dependabot.yml
```

`index.html` is a single long page. Each topic is a `<section class="section"
id="…">` and the nav links to those `id`s. Adding a section means adding both
the section and (if it should be reachable) its nav entry.

## How the site is published

GitHub Pages serves this repository using the **legacy branch build**: source is
the `main` branch, root (`/`) path. Pushing to `main` republishes the site. There
is no deploy workflow, and none should be added unless the Pages source is
intentionally switched to GitHub Actions.

Consequences an agent must respect:

- **Do not delete `.nojekyll`.** It bypasses Jekyll so files are served verbatim.
- **Never use root-absolute URLs** (`/assets/css/style.css`). The site is served
  from the `/ai-scrum/` subpath, so root-absolute paths 404 in production. Use
  relative URLs (`assets/css/style.css`). CI enforces this.
- Anything committed to `main` is public immediately. There is no staging site.

## Conventions

**HTML** — semantic elements, two-space indentation, `lang` on `<html>`, a
`<meta name="description">` in `<head>`. Escape `&` as `&amp;` inside attribute
values (an unescaped `&` before a word is an ambiguous ampersand). Decorative
inline SVG icons get `aria-hidden="true" focusable="false"`; an icon-only link
needs an `aria-label` so it has an accessible name.

**CSS** — one stylesheet, no preprocessor. Design tokens are CSS custom
properties on `:root` (`--bg`, `--primary`, `--radius`, `--font`, …); use the
tokens rather than hard-coded colours or radii. Sections are separated by
`/* ===== Name ===== */` banner comments. The palette is dark-only. Responsive
rules live in `@media (max-width: 768px)` and `@media (max-width: 480px)` blocks
at the end of each section.

**JavaScript** — one classic (non-module) script, no dependencies, browser APIs
only. It runs inside a single `DOMContentLoaded` listener and uses
`IntersectionObserver` for reveal animations. If you add an animated component,
add its class to the selector list in `assets/js/main.js` so it reveals with the
rest.

**Commits** — Conventional Commits, as used throughout the history:
`feat:`, `fix:`, `docs:`, `chore:`.

**Changelog** — every user-visible change gets an entry under `## [Unreleased]`
in `CHANGELOG.md`, following [Keep a Changelog](https://keepachangelog.com/).
The release workflow reads release notes straight out of this file, so an
entry missing here is a note missing from the release.

## Checks

These are the only checks that exist. Run them from the repository root; each
must exit 0. They are exactly what CI runs.

```bash
# Structure: required Pages files, local assets resolve, in-page anchors
# resolve, ids are unique, no root-absolute URLs, required meta present.
python3 .github/scripts/check_site.py .

# HTML5 validation + WCAG rules (downloads the validator on demand).
npx --yes html-validate@9.7.1 --config .github/linters/html-validate.json index.html

# JavaScript syntax check.
node --check assets/js/main.js
```

To preview the site locally, serve it over HTTP rather than opening the file
directly:

```bash
python3 -m http.server 8000
```

## Things not to do

- Do not introduce a build system, package manager, bundler, or test framework.
  If a change seems to need one, raise it with the maintainer first.
- Do not add a Pages deployment workflow; publishing is branch-based.
- Do not add a `_config.yml` or otherwise re-enable Jekyll.
- Do not fabricate release artifacts. A release here is a tagged snapshot of the
  published site plus notes, nothing more.
- Do not restyle the site or rewrite its copy as a side effect of an unrelated
  change. The visual design and voice are deliberate authorial choices.
