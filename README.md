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

| Hook Name            | Description                                                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| ansible-lint         | Runs [ansible-lint](https://github.com/ansible/ansible-lint) to check your project for best Ansible practices and behaviour. |
| format-shell         | Enables manually running [shfmt](https://github.com/mvdan/sh) to format your shell scripts.                                  |
| format-toml          | Enables manually running [tomll](https://github.com/pelletier/go-toml) to format your TOML configuration files.              |
| markdown-linting     | Runs [markdown-lint](https://github.com/davidanson/markdownlint) on your Markdown files.                                     |
| markdown-spelling    | Runs [vale](https://github.com/errata-ai/vale) on your Markdown files to check for spelling errors.                          |
| toml-lint            | Optionally runs [tomll](https://github.com/pelletier/go-toml) on your TOML configuration file.                               |
| shell-fmt            | Runs [shfmt](https://github.com/mvdan/sh) to format all shell scripts.                                                       |
| shell-lint           | Runs [shellcheck](https://www.shellcheck.net/) to lint all shell scripts.                                                    |
| vale-synchronize     | Enables manually running [vale](https://github.com/errata-ai/vale) to download remote packages.                              |
| workflow-lint        | Optionally runs [actionlint](https://github.com/rhysd/actionlint) on all GitHub workflows.                                   |
| workflow-header-lint | Optionally runs a simple shell script to parse the headers on GitHub workflows.                                              |

### Implementation Details

| Hook Name               | Exe Source   | Implementation                                                                                                                                                                                                 |
| ----------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ansible-lint            | user project | A custom [CICD-Tools script](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/boxes/bootstrap/pre-commit/ansible-lint.sh) invokes ansible-lint in [poetry](https://python-poetry.org/).    |
| commit-message-spelling | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| format-shell            | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| format-toml             | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| markdown-linting        | 3rd party    | The [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) container is used to invoke this tool.                                                                                               |
| markdown-spelling       | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| toml-lint               | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| shell-fmt               | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| shell-lint              | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| vale-synchronize        | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| workflow-lint           | CICD-Tools   | The [CICD-Tools container](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/container/Dockerfile) is used to invoke this tool.                                                             |
| workflow-header-lint    | shell        | A custom [CICD-Tools script](https://github.com/cicd-tools-org/cicd-tools/blob/master/.cicd-tools/boxes/bootstrap/pre-commit/workflow-header-lint.sh) is invoked.                                              |

## License

[MPL-2](LICENSE)
