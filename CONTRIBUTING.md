# Contributing to CICD-Tools Pre-Commit Hooks

Thank you for your interest in contributing! This project provides pre-commit hooks for the CICD-Tools ecosystem. To maintain quality and consistency, please follow these guidelines.

## Development Environment

This project uses [Poetry](https://python-poetry.org/) for dependency management.

- **Install dependencies:** `poetry install`
- **Run tests:** `make test-python`
- **Format code:** `make format-python`
- **Lint code:** `make lint-python`

## Coding Standards

### Python Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

- **Line Length:** Strictly **80 characters**.
- **Formatting:** Use `ruff format` to ensure consistency.
- **Imports:** Re-export functions in `__init__.py` using `from .module import func as func` to satisfy linting rules.
- **Docstrings:** Required for modules and public functions/classes, except in tests.

### Project Structure

- Python-based hooks are in `src/cicd_tools_pre_commit/`.
- Shell-based hooks are in `src/pre-commit/`.
- Reusable system utilities should go in `src/cicd_tools_pre_commit/system/`.

## Commit Guidelines

We enforce [Conventional Commits](https://www.conventionalcommits.org/).

- **Format:** `<type>(<scope>): <description>`
- **Common Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Scope:** Usually the name of the hook or module (e.g., `sphinx`, `git`, `system`).

## Pull Request Process

1.  **Create a branch:** Use a descriptive name like `feat/new-hook`.
2.  **Add tests:** Ensure new functionality is covered by unit tests.
3.  **Run pre-commit:** Ensure all hooks pass locally before submitting.
4.  **Documentation:** Update `README.md` and hook definitions in `.pre-commit-hooks.yaml` if necessary.
5.  **Alphabetical Order:** Ensure hooks in `.pre-commit-hooks.yaml` are sorted by `id`. Use `make pre-commit-sort-hooks` to automate this.

## Spell Checking

We use [Vale](https://vale.sh/) for spell checking. If you add new technical terms that trigger warnings, add them to `.vale/Vocab/pre-commit/accept.txt` and keep the list sorted alphabetically.
