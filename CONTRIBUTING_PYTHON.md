# Python Contribution Guide

This guide outlines the standards and procedures for contributing Python code to this project.

## Project Structure

Python source code is located in `src/cicd_tools_pre_commit/`.
Each major piece of functionality should be organized into its own module (e.g., `src/cicd_tools_pre_commit/gettext/`).

Each module should contain:

- `__init__.py`: Exporting the public API.
- `*.py`: The core logic.
- `tests/`: A sub-directory containing unit tests.
- `tests/__init__.py`: An empty file to make the directory a package.

## Tooling

We use the following tools for Python development:

- **Poetry**: Dependency management and package building.
- **Ruff**: Linting and code formatting (strict 80-character line limit).
- **Unittest**: The standard Python testing framework.
- **Makefile**: Provides shortcuts for common tasks (`make test-python`, `make format-python`, `make lint-python`).

## Coding Standards

### Imports

- Use **absolute imports** (e.g., `from cicd_tools_pre_commit.cli.types import file_existing`).
- Avoid multi-level relative imports.

### Constants

- Public constants should be named in `UPPER_CASE`.
- Prefix constants related to a specific file format or module for clarity (e.g., `PO_COMMENT_IDENTIFIER`).
- Keep constants sorted alphabetically within their section.

### Functions and Classes

- Follow the `pysed.py` paradigm for pre-commit hooks: the entry point hook function should be at the top of the file, and internal processing logic should be moved to the bottom.
- Include docstrings for all modules and public functions/classes, as required by Ruff.

## Testing Standards

### AAA Pattern
All unit tests must strictly follow the **Arrange-Act-Assert** pattern. Each section should be separated by a single blank line.

```python
def test_example__condition__result(self):
    content = "example"  # Arrange

    result = process(content)  # Act

    self.assertEqual(result, expected)  # Assert
```

Please note the comments are here just to emphasize the compartmentalization, and should not be included in production code.

### Naming Convention
Tests must follow the naming convention: `test_functionname__condition1__condition2__expected_result`.

### Mocking

- Use `unittest.mock.patch` for mocking dependencies.
- Prefer `mock_open` to simulate file operations instead of creating temporary files on disk.
- When using multi-line decorators, place each argument on its own line and include trailing commas.

```python
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="content",
)
```

## Adding New Hooks

When adding new hooks to `.pre-commit-hooks.yaml`:

- Ensure the `id` is descriptive, and lends itself to the conventions established by existing entries.
- Comments can be used if they make it easier for end users to integrate the hooks with their projects.
- Keep the hook definitions sorted alphabetically by their `id`. The [Makefile](Makefile) exposes a `pre-commit-sort-hooks` command for this purpose.
- Ensure the hook is documented in both the Description and Implementation sections of the [README.md](README.md) file.
