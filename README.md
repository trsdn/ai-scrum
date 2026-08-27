# AI-Scrum

[![CI](https://github.com/trsdn/ai-scrum/actions/workflows/ci.yml/badge.svg)](https://github.com/trsdn/ai-scrum/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

🌐 **Live site**: [trsdn.github.io/ai-scrum](https://trsdn.github.io/ai-scrum/)

GitHub Pages site for the AI-Scrum framework — a Scrum-inspired methodology for human-AI collaboration using GitHub Copilot CLI.

## Template Repositories

- **[Autonomous](https://github.com/trsdn/copilot-scrum-autonomous)** — AI is PO + Scrum Master, human is stakeholder
- **[Guided](https://github.com/trsdn/copilot-scrum-guided)** — Human is PO, AI is Scrum Master + developer

## Working on this site

A hand-written static site: `index.html` plus `assets/css/style.css` and
`assets/js/main.js`. There is no build step and no dependencies to install.
Preview it locally with `python3 -m http.server 8000`, then open
<http://localhost:8000>.

The checks CI runs — all of which you can run locally — and the conventions to
follow are documented in [AGENTS.md](AGENTS.md). Notable changes are recorded in
[CHANGELOG.md](CHANGELOG.md).

## License

Released under the [MIT License](LICENSE).

