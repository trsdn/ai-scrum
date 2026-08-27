# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository publishes a website, not a package. A release here is a tagged
snapshot of the published site with notes — there is no downloadable artifact.

## [Unreleased]

### Added

- `LICENSE` — MIT, referenced from `README.md`.
- `AGENTS.md` describing the repository, the site structure, how GitHub Pages
  publishes it, and the conventions to follow.
- This changelog, seeded from the existing commit history.
- Continuous integration (`.github/workflows/ci.yml`) running on every push and
  pull request: site structure checks, HTML5 validation with WCAG rules, and a
  JavaScript syntax check.
- `.github/scripts/check_site.py` — dependency-free structure checker verifying
  that the files GitHub Pages needs exist, that referenced local assets exist,
  that in-page anchors resolve, that `id`s are unique, that no local URL is
  root-absolute, and that each document declares charset, viewport, `lang`,
  title and description.
- Release workflow (`.github/workflows/release.yml`) triggered by `v*` tags,
  publishing a GitHub Release with notes extracted from this changelog by
  `.github/scripts/extract_changelog.py`.
- Dependabot configuration (`.github/dependabot.yml`) with a weekly schedule for
  the `github-actions` ecosystem.

### Fixed

- Escaped the ambiguous `&` characters in the Google Fonts `<link>` URL, which
  made `index.html` non-conforming HTML5.
- Gave the icon-only GitHub link in the navigation an accessible name
  (`aria-label`) and marked its inline SVG decorative, so screen readers
  announce its purpose.

## [0.1.0] - 2026-02-14

Retroactive baseline covering the site as first written and published. The
repository carried no tags or releases before this entry; the changes below are
reconstructed from the commit history between 2026-02-12 and 2026-02-14.

### Added

- GitHub Pages site for the AI-Scrum framework: single-page `index.html` with
  `assets/css/style.css`, `assets/js/main.js` and `.nojekyll`.
- Constitution, escalation model, Definition of Done and GitHub Copilot CLI
  sections.
- "The Problem" section explaining why the framework exists.
- Comparison table contrasting ad-hoc work, spec-driven work and AI-Scrum.
- Acceptance criteria in the Definition of Done.
- "Two Modes" section introducing the guided and autonomous variants early on
  the page.
- Drift control section covering scope lock, huddle checks and boundary review.
- `/refine` ceremony, taking the sprint cycle to five ceremonies with an
  idea-to-issue pipeline.
- Prerequisites section documenting experimental/autopilot mode.
- Stakeholder Authority as Principle 0 of the constitution and the escalation
  model.

### Changed

- Reframed the framework around an AI agent team rather than a single AI agent.
- Rewrote the variant cards to lead with guided and present autonomous as the
  advanced, multi-hour mode, then simplified them to a clean centered layout.
- Renamed prompts to skills for GitHub Copilot CLI compatibility.

### Fixed

- Corrected the manifesto note to say above/below rather than left/right.
- Aligned variant card and sprint cycle card buttons to the bottom, and
  stretched sprint cards to equal height.
- Reworked the sprint cycle into a five-column grid and removed the arrows.

### Removed

- Stats counter section from the hero.

[unreleased]: https://github.com/trsdn/ai-scrum/compare/850dd34...HEAD
[0.1.0]: https://github.com/trsdn/ai-scrum/commits/850dd34
