#!/bin/bash

# Performs tests on the pre-commit hooks.

# Implementation:
# Templates implementing this script will likely also have to customize their .job-50-precommit.yml workflow.
# The API demonstrated here is more for example purposes.

# 1:                  The name of a pre-commit test scenario. (See 'main' below.)
# TEST_PROJECT_NAME:  The name of the rendered test project.

# CI only script.

set -eo pipefail

main() {
  pushd "${TEST_PROJECT_NAME}" >> /dev/null
  poetry run pre-commit run --hook-stage manual spelling-vale-sync
  scenario "${1}"
  popd >> /dev/null
}

scenario() {

  local TEMP_FILE

  test_commit_lint_fails() {
    util "git_reset"
    TEMP_FILE=$(util "create_tmp")
    touch "${TEMP_FILE}"
    git stage "${TEMP_FILE}"
    git commit -m 'test - pre-commit: improperly formatted commit' || exit 0
    util "fail"
  }

  test_toml_lint_fails() {
    util "git_reset"
    sed -i.bak 's/authors =/    authors = /g' pyproject.toml
    git stage pyproject.toml
    git commit -m 'test(PRE-COMMIT): fail due to tomll' || exit 0
    util "fail"
  }

  test_commit_spelling_fails() {
    util "git_reset"
    TEMP_FILE=$(util "create_tmp")
    touch "${TEMP_FILE}"
    git stage "${TEMP_FILE}"
    git commit -m 'test(PRE-COMMIT): ssspelling error' || exit 0
    util "fail"
  }

  test_toml_lint_passes() {
    util "git_reset"
    sed -i.bak "s/description = '.*'/description = 'updated description'/g" pyproject.toml
    git stage pyproject.toml
    git commit -m 'test(PRE-COMMIT): upgrade python without issue'
  }

  test_shell_lint_fails() {
    echo "Disabled."
  }

  test_shell_format_fails() {
    echo "Disabled."
  }

  test_workflow_lint_fails() {
    util "git_reset"
    find .github/workflows -type f -name '*.yml' -exec sed -i.bak 's/uses:/illegal-yaml-key:/g' {} \;
    git stage .github
    git commit -m 'test(PRE-COMMIT): fail due to actionlint' || exit 0
    util "fail"
  }

  test_workflow_header_lint_fails() {
    util "git_reset"
    sed -i.bak 's,-github-workflow,-github-wrong-name,g' .github/workflows/workflow-*.yml
    git stage .github
    git commit -m 'test(PRE-COMMIT): fail due to workflow header lint' || exit 0
    util fail
  }

  "$@"

}

util() {

  local COMMAND
  local PREFIX

  _util_create_tmp() {
    mktemp tmp.XXXXXXX
  }

  _util_fail() {
    echo "This commit should have failed."
    exit 127
  }

  _util_git_reset() {
    git reset HEAD
    git clean -fd
    git checkout .
  }

  _util_unknown_command() {
    echo "Unknown utility command: '${COMMAND}'"
    exit 127
  }

  PREFIX="_util"
  COMMAND="${PREFIX}_${1}"
  if [[ $(type -t "${COMMAND}") == function ]]; then
    shift
    "${COMMAND}" "$@"
  else
    "${PREFIX}_unknown_command"
  fi

}

main "$@"
