# Pre-Commit Hooks for CICD-Tools

[![cicd-tools](https://img.shields.io/badge/ci/cd:-cicd_tools-blue)](https://github.com/cicd-tools-org/cicd-tools)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

| Branch                                                         | Build                                                                                                                                                                                                        |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [main](https://github.com/cicd-tools-org/pre-commit/tree/main) | [![workflow-link](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml/badge.svg?branch=main)](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml) |
| [dev](https://github.com/cicd-tools-org/pre-commit/tree/dev)   | [![workflow-link](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml/badge.svg?branch=dev)](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml)  |

This repository provides [pre-commit](https://pre-commit.com/) hooks for the [CICD-Tools](https://github.com/cicd-tools-org/cicd-tools) project.

### Containerization and Pre-Commit

These hooks all rely on 3rd party software to perform different types of static analysis:

- Some of this software can be managed by the end user project's themselves.
- Other software packages are provided by containers.

**For this reason we strongly recommend installing a container runtime such as [Docker](https://www.docker.com/) or [Colima](https://github.com/abiosoft/colima) on your development machine if you are consuming these hooks.**

### Included Pre-Commit Hooks

| Hook Name                      | Description                                                                                                                                                                                                                                 |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cicd-tools-schema-cookiecutter | Runs [json-schema](https://python-jsonschema.readthedocs.io/en/stable/) to validate a [cookiecutter](https://github.com/cookiecutter/cookiecutter) config file against the [CICD-Tools schema](./src/cicd-tools/schemas/cookiecutter.json). |
| cicd-tools-schema-manifest     | Runs [json-schema](https://python-jsonschema.readthedocs.io/en/stable/) to validate a CICD-Tools manifest against the [CICD-Tools schema](./src/cicd-tools/schemas/manifest.json).                                                          |
| format-shell                   | Runs [shfmt](https://github.com/mvdan/sh) to format your shell scripts.                                                                                                                                                                     |
| format-toml                    | Runs [tomll](https://github.com/pelletier/go-toml) to format your TOML configuration files.                                                                                                                                                 |
| gettext-translations-add       | Runs [gettext](https://www.gnu.org/software/gettext/) utilities to support adding additional languages.                                                                                                                                     |
| gettext-translations-compile   | Runs [gettext](https://www.gnu.org/software/gettext/) utilities to compile '.mo' files from '.po' files.                                                                                                                                    |
| gettext-translations-missing   | Runs [gettext](https://www.gnu.org/software/gettext/) utilities to search for missing translations.                                                                                                                                         |
| gettext-translations-update    | Runs [gettext](https://www.gnu.org/software/gettext/) utilities to extract translations and update all files.                                                                                                                               |
| git-conflict-markers           | Runs [git](https://git-scm.com/) to check for left over conflict markers in your commit.                                                                                                                                                    |
| lint-github-workflow           | Optionally runs [actionlint](https://github.com/rhysd/actionlint) on all GitHub workflows.                                                                                                                                                  |
| lint-github-workflow-header    | Optionally runs a shell script to lint GitHub workflow headers.                                                                                                                                                                             |
| lint-markdown                  | Runs [markdown-lint](https://github.com/davidanson/markdownlint) on your Markdown files.                                                                                                                                                    |
| lint-shell                     | Runs [shellcheck](https://www.shellcheck.net/) to lint all shell scripts.                                                                                                                                                                   |
| pre-commit-sort-config         | Runs [yq](https://mikefarah.gitbook.io/yq) to sort your [.pre-commit-config.yaml](.pre-commit-config.yaml) file.                                                                                                                            |
| pre-commit-sort-hooks          | Runs [yq](https://mikefarah.gitbook.io/yq) to sort your [.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) file.                                                                                                                              |
| security-credentials           | Runs [trufflehog](https://trufflesecurity.com) to ensure you don't commit secrets to your codebase.                                                                                                                                         |
| spelling-commit-message        | Runs [vale](https://github.com/errata-ai/vale) on your git commit messages to check for spelling errors.                                                                                                                                    |
| spelling-markdown              | Runs [vale](https://github.com/errata-ai/vale) on your Markdown files to check for spelling errors.                                                                                                                                         |
| spelling-vale-sync             | Enables manually running [vale](https://github.com/errata-ai/vale) to download remote packages.                                                                                                                                             |
| spelling-vale-vocab            | Enables automated sorting of [vale](https://github.com/errata-ai/vale) vocabularies.                                                                                                                                                        |
| poetry-lint-ansible            | Runs [ansible-lint](https://github.com/ansible/ansible-lint) to check for Ansible best practices and behaviours.                                                                                                                            |
| poetry-lint-python             | Runs [pylint](https://github.com/pylint-dev/pylint) on all Python files to perform static code analysis.                                                                                                                                    |
| poetry-types-python            | Runs [mypy](https://github.com/python/mypy) on all Python files to check typing.                                                                                                                                                            |

### Implementation Details

| Hook Name                      | Exe Source         | Implementation                                                                                                                                                                                                               |
|--------------------------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cicd-tools-schema-cookiecutter | pre-commit venv    | The Python package [check-jsonschema](https://check-jsonschema.readthedocs.io/en/stable/) is invoked.                                                                                                                        |
| cicd-tools-schema-manifest     | pre-commit venv    | The Python package [check-jsonschema](https://check-jsonschema.readthedocs.io/en/stable/) is invoked.                                                                                                                        |
| format-shell                   | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| format-toml                    | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| gettext-translations-add       | CICD-Tools         | A custom [script](src/pre-commit/gettext-translations.sh) is invoked which uses the [CICD-Tools gettext container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/gettext/Dockerfile).        |
| gettext-translations-compile   | CICD-Tools         | A custom [script](src/pre-commit/gettext-translations.sh) is invoked which uses the [CICD-Tools gettext container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/gettext/Dockerfile).        |
| gettext-translations-missing   | CICD-Tools         | A custom [script](src/pre-commit/gettext-translations.sh) is invoked which uses the [CICD-Tools gettext container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/gettext/Dockerfile).        |
| gettext-translations-update    | CICD-Tools         | A custom [script](src/pre-commit/gettext-translations.sh) is invoked which uses the [CICD-Tools gettext container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/gettext/Dockerfile).        |
| git-conflict-markers           | local binary       | The local git binary is invoked.                                                                                                                                                                                             |
| lint-github-workflow           | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| lint-github-workflow-header    | shell              | A custom [script](src/pre-commit/lint-github-workflow-header.sh) is invoked.                                                                                                                                                 |
| lint-markdown                  | 3rd party          | The official [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli/pkgs/container/markdownlint-cli) container is used to invoke this tool.                                                                    |
| lint-shell                     | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| pre-commit-sort-config         | CICD-Tools         | A custom [script](src/pre-commit/pre-commit-sort-config.sh) is invoked which uses the [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile).  |
| pre-commit-sort-hooks          | CICD-Tools         | A custom [script](src/pre-commit/pre-commit-sort-hooks.sh) is invoked which uses the [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile).   |
| security-credentials           | 3rd Party          | The official [trufflehog](https://hub.docker.com/r/trufflesecurity/trufflehog/) container is used to invoke this tool.                                                                                                       |
| spelling-commit-message        | CICD-Tools         | A custom [script](src/pre-commit/spelling-commit-message.sh) is invoked which uses the [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile). |
| spelling-markdown              | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| spelling-vale-sync             | CICD-Tools         | The [CICD-Tools utilities container](https://github.com/cicd-tools-org/cicd-tools/blob/main/.cicd-tools/containers/utilities/Dockerfile) is used to invoke this tool.                                                        |
| spelling-vale-vocab            | shell              | The local shell binary is used to invoke a one-liner.                                                                                                                                                                        |
| lint-ansible                   | poetry environment | A custom [script](src/pre-commit/lint-ansible.sh) and the local [poetry](https://python-poetry.org/) environment is used to invoke this tool.                                                                                |
| poetry-lint-python             | poetry environment | The project's [poetry](https://python-poetry.org/) environment is used to invoke this tool.                                                                                                                                  |
| poetry-types-python            | poetry environment | The project's [poetry](https://python-poetry.org/) environment is used to invoke this tool.                                                                                                                                  |

## License

[MPL-2](LICENSE)
