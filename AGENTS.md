# AI Agent Instructions

Welcome, Agent. This repository contains pre-commit hooks for the CICD-Tools project. To ensure high-quality contributions, please follow these guidelines.

## Project Context

- **Primary Language**: Python (Poetry for management).
- **Core Tooling**: Ruff (formatting/linting), Unittest, Makefile.
- **Hook Definition**: `.pre-commit-hooks.yaml` (sorted alphabetically).

## Development Guidelines

Please read the [CONTRIBUTING_PYTHON.md](CONTRIBUTING_PYTHON.md) file thoroughly to ensure commits are consistent and maintainable.

### General Guidance

- Keep commit messages to one line change descriptions that are commitizen compatible.
- Leverage the [Makefile](Makefile) to both understand and utilize the codebase tooling.
- The codebase should 'eat it's own dog food' and apply the pre-commit hooks to itself where applicable.

### Modernizing Hooks

This repository is slowly transitioning from legacy Bash code to Python.

- If a legacy Bash script has functionality that is replaced by a Python hook, confirm with a human user that they wish to decommission the unused Bash logic and variables.

## Common Makefile Targets

- `make test-python`: Run the Python test suite.
- `make format-python`: Fix formatting issues using Ruff.
- `make lint-python`: Check for linting errors.
- `make pre-commit-sort-hooks`: (Environment permitting) Sort the hook definitions.

## Repository Specific Patterns

- Custom Vale vocabulary is managed in `.vale/Vocab/pre-commit/accept.txt`. Add new technical terms there if they cause spell check failures in commit messages.
- Always verify your changes with `read_file` or `ls` before marking a plan step as complete.
