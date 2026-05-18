---
name: fabric-darkmode-project
description: "Use when working in the Fabric-DarkMode demo repo, especially to run Playwright demos/tests, update shell helpers, or regenerate leadership slides."
---

# Fabric DarkMode Project Skill

Use this skill when working in the Fabric-DarkMode workspace.

## Main workflow

- Demo and test work lives in `tests/demo-acts-2-3.spec.ts`.
- Shared selectors and shell assertions live in `tests/helpers/shell.ts`.
- Playwright settings live in `playwright.config.ts`.
- Leadership slide generation lives in `scripts/generate_leadership_ppt.py`.
- Generated deck output is written to `slides/dark-mode-private-preview-leadership-review.pptx`.

## Useful commands

- Run the full test suite with `npm test`.
- Run the headed demo flow with `npm run demo`.
- Run the slower demo flow with `npm run demo:slow`.
- Open the HTML report with `npm run report`.

## Working rules

- Prefer updating shared helpers in `tests/helpers/shell.ts` instead of duplicating selectors in specs.
- Keep demo flows deterministic and screenshot-friendly.
- When changing the slide generator, validate the generated deck path and the styling used by the existing report.
- Keep changes focused on the demo, shell theme, or leadership-review flow for this repo.