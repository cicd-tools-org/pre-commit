# AI Agent Instructions

These instructions are specifically for AI agents working on this repository to ensure consistency with the established patterns and constraints.

## Testing Standards

- **Naming Pattern:** Tests must follow `test_functionname__condition__expected_result`.
- **No Comments:** Tests should be self-documenting; avoid using comments within test methods.
- **Mocking Strategy:**
    - Prefer inline mocking in `@patch` decorators for simple dependencies (e.g., `@patch("module.func", Mock(return_value=[]))`).
    - When testing CLI components, mock internal dependencies (like custom argparse types) directly rather than system modules like `os`.
    - Mock `sys.argv` using the `@patch` decorator rather than context managers.
- **Separation of Concerns:** Separate the validation of logical changes (e.g., file modifications) from the validation of execution flow (e.g., non-zero exit codes) into distinct test cases.
- **Cleanup:** Use trailing commas in function argument lists within tests for cleaner style.

## Coding Practices

- **Circular Imports:** To prevent circular dependencies, move shared utilities into dedicated modules (e.g., `src/cicd_tools_pre_commit/system/call.py`) and re-export them via `__init__.py`.
- **System Calls:** Use the project's internal `call` utility (`src/cicd_tools_pre_commit/system/call.py`) for system commands. It handles output printing and standardized error exits.
- **Argument Parsing:** Prefer `argparse` for command-line tools.
- **Poetry Scripts:** Python scripts intended to be invoked via `tool.poetry.scripts` should NOT include an `if __name__ == "__main__":` block.
- **Line Length:** Maintain a strict **80-character limit**. Ruff will enforce this.

## Pre-Commit Hooks

- **Exit Codes:** Hooks that perform file modifications (or detect issues that require user action) MUST exit with a non-zero return code (e.g., `sys.exit(1)`) to signal the framework.
- **Definitions:** Hook definitions in `.pre-commit-hooks.yaml` must be sorted alphabetically by their `id`. Run `make pre-commit-sort-hooks` to fix ordering.

## Memory and Context

- If you encounter a new pattern or solve a complex repository-specific issue, record it using the memory tool.
- Always check `.vale/Vocab/pre-commit/accept.txt` before adding new technical terms to ensure they won't fail spell check.
