# Repository Guidelines

## Project Structure & Module Organization

This repository builds the `portdb.yaleman.org` Zola site. Port source data lives under `data/{tcp,udp}/<port>/`; `generatecontent.py` turns it into Markdown in `content/{tcp,udp}/`. Keep hand-written notes in the source data directories rather than editing generated pages. Python types and shared code belong in `portdb/`, while Zola templates and site assets live in `templates/` and `static/`. Tests are under `tests/`. Zola writes the ignored build output to `output/`.

## Build, Test, and Development Commands

Use Python 3.13 and `uv`; keep `uv.lock` synchronized with `pyproject.toml`.

- `uv sync --all-groups` installs runtime and development dependencies.
- `make build` builds the site into `output/` using `config.toml`.
- `make serve` rebuilds on changes and serves the local site on port 1111.
- `uv run python generatecontent.py` regenerates port Markdown and protocol indexes from `data/`.
- `uv run pytest` runs the test suite.
- `uv run ruff check` and `uv run ty check` reproduce the lint and type-check CI jobs.

Run the generator only from the repository root because its paths are relative.

## Coding Style & Naming Conventions

Use four-space indentation and type annotations for Python. Follow Ruff's configured 200-character line limit, but prefer readable, focused functions over long statements. Use `snake_case` for modules, functions, and variables; use `UPPER_CASE` for constants and `PascalCase` for types. Name port content and data by protocol and numeric port, for example `data/tcp/443/notes.md`. Keep documentation and comments project-relative.

## Testing Guidelines

Pytest discovers `test_*.py` files and `test_*` functions in `tests/`. Add focused tests for parsing, generation, and shared library behavior; do not place test helpers or library functions in executable entry points. There is currently no enforced coverage threshold. Before submitting, run pytest, Ruff, the type checker, and `make check`.

## Commit & Pull Request Guidelines

Recent human commits use short, imperative summaries such as `moving to uv`; automated dependency commits use `Bump <package> from <old> to <new> (#123)`. Keep each commit scoped to one change. Pull requests should explain the reason and observable effect, link the relevant issue, and note commands run. Include screenshots for theme or rendered-page changes, and do not commit `output/`, downloaded IANA XML, caches, or local environment files.

## Security

Report vulnerabilities through the process in `SECURITY.md`; do not disclose sensitive findings in a public issue.
