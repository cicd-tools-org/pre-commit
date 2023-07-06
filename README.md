# Pre-Commit Hooks for CICD-Tools

(Powered by [CICD-Tools](https://github.com/cicd-tools-org/cicd-tools).)

This repository provides [pre-commit](https://pre-commit.com/) hooks for the [CICD-Tools](https://github.com/cicd-tools-org/cicd-tools) project.

#### Master Branch (Follows the latest production tag)
[![workflow-link](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml/badge.svg?branch=master)](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml)

#### Dev Branch
[![workflow-link](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml/badge.svg?branch=dev)](https://github.com/cicd-tools-org/pre-commit/actions/workflows/workflow-push.yml)

### Containerization and Pre-Commit

These hooks all rely on 3rd party software to perform different types of static analysis:

- Some of this software can be managed by the end user project's themselves.
- Other software packages are provided by containers.

**For this reason we strongly recommend installing a container runtime such as [Docker](https://www.docker.com/) or [Colima](https://github.com/abiosoft/colima) on your development machine if you are consuming these hooks.**

### Included Pre-Commit Hooks

| Hook Name                   | Description                                                                                                      |
|-----------------------------|------------------------------------------------------------------------------------------------------------------|
| format-shell                | Runs [shfmt](https://github.com/mvdan/sh) to format your shell scripts.                                          |
| format-toml                 | Runs [tomll](https://github.com/pelletier/go-toml) to format your TOML configuration files.                      |
| lint-ansible                | Runs [ansible-lint](https://github.com/ansible/ansible-lint) to check for Ansible best practices and behaviours. |
| lint-github-workflow        | Optionally runs [actionlint](https://github.com/rhysd/actionlint) on all GitHub workflows.                       |
| lint-github-workflow-header | Optionally runs a shell script to lint GitHub workflow headers.                                                  |
| lint-markdown               | Runs [markdown-lint](https://github.com/davidanson/markdownlint) on your Markdown files.                         |
| lint-shell                  | Runs [shellcheck](https://www.shellcheck.net/) to lint all shell scripts.                                        |
| security-credentials        | Runs [trufflehog](https://trufflesecurity.com) to ensure you don't commit secrets to your codebase.              |
| spelling-commit-message     | Runs [vale](https://github.com/errata-ai/vale) on your git commit messages to check for spelling errors.         |
| spelling-markdown           | Runs [vale](https://github.com/errata-ai/vale) on your Markdown files to check for spelling errors.              |
| spelling-vale-synchronize   | Enables manually running [vale](https://github.com/errata-ai/vale) to download remote packages.                  |

### Implementation Details

| Hook Name                   | Exe Source   | Implementation                                                                                                                                                                                              |
|-----------------------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| format-shell                | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| format-toml                 | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| lint-ansible                | user project | A custom [CICD-Tools script](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/boxes/bootstrap/pre-commit/lint-ansible.sh) invokes ansible-lint in [poetry](https://python-poetry.org/). |
| lint-github-workflow        | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| lint-github-workflow-header | shell        | A custom [CICD-Tools script](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/boxes/bootstrap/pre-commit/lint-github-workflow-header.sh) is invoked.                                    |
| lint-markdown               | 3rd party    | The [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) container is used to invoke this tool.                                                                                            |
| lint-shell                  | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| security-credentials        | 3rd Party    | The official [trufflehog](https://hub.docker.com/r/trufflesecurity/trufflehog/) container is used to invoke this tool.                                                                                      |
| spelling-commit-message     | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| spelling-markdown           | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |
| spelling-vale-synchronize   | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                          |

## License

[MPL-2](LICENSE)
