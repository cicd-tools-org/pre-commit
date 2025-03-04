#!/bin/bash

# Builds Sphinx HTML documentation and provides translation and spelling integrations.

# pre-commit script.

set -eo pipefail

# shellcheck source=./../cicd-tools/libraries/container.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/container.sh"

# shellcheck source=./../cicd-tools/libraries/environment.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/environment.sh"

# shellcheck source=./../cicd-tools/libraries/logging.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../cicd-tools/libraries/logging.sh"

GETTEXT_TRANSLATIONS_EXAMPLE_LANGUAGES_CODES_URL="https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html"

_sphinx_args() {
  local _SPHINX_COMMAND
  local OPTARG
  local OPTIND=1
  local OPTION

  if [[ -z "${1}" ]]; then
    _sphinx_usage
  fi

  _SPHINX_COMMAND="${1}"
  shift

  while getopts "b:c:e:i:g:m:p:r:s:u" OPTION; do
    case "${OPTION}" in
      e)
        _SPHINX_TRANSLATIONS_EMAIL_ADDRESS="${OPTARG}"
        ;;
      i)
        PRECOMMIT_VALE_DOCKER_IMAGE="${OPTARG}"
        ;;
      g)
        _SPHINX_GENERATED_TEMPLATE_PATH="${OPTARG}"
        ;;
      m)
        _SPHINX_TRANSLATIONS_EMPTY_MESSAGE_MATCH="${OPTARG}"
        ;;
      p)
        _SPHINX_BASE_PATH="${OPTARG}"
        ;;
      s)
        _SPHINX_TRANSLATIONS_LANGUAGES_BEING_SKIPPED+=("${OPTARG}")
        ;;
      \?)
        _sphinx_usage
        ;;
      :)
        _sphinx_usage
        ;;
      *)
        _sphinx_usage
        ;;
    esac
  done
  shift $((OPTIND - 1))

  case "${_SPHINX_COMMAND}" in
    add)
      if [[ -z "${_SPHINX_BASE_PATH}" ]] ||
        [[ -z "${_SPHINX_TRANSLATIONS_EMAIL_ADDRESS}" ]]; then
        _sphinx_usage_title
        _sphinx_usage_add_translation
        _sphinx_usage_terminate
      fi
      sphinx_add_translation
      ;;
    build)
      if [[ -z "${_SPHINX_BASE_PATH}" ]]; then
        _sphinx_usage_title
        _sphinx_usage_build
        _sphinx_usage_terminate
      fi
      sphinx_build
      ;;
    missing)
      if [[ -z "${_SPHINX_BASE_PATH}" ]] ||
        [[ -z "${_SPHINX_TRANSLATIONS_EMPTY_MESSAGE_MATCH}" ]]; then
        _sphinx_usage_title
        _sphinx_usage_missing_translations
        _sphinx_usage_terminate
      fi
      sphinx_missing_translations
      ;;
    spell_check)
      if [[ -z "${_SPHINX_BASE_PATH}" ]] ||
        [[ -z "${PRECOMMIT_VALE_DOCKER_IMAGE}" ]]; then
        _sphinx_usage_title
        _sphinx_usage_spell_check
        _sphinx_usage_terminate
      fi
      sphinx_spell_check
      ;;
    update)
      if [[ -z "${_SPHINX_BASE_PATH}" ]] ||
        [[ -z "${_SPHINX_TRANSLATIONS_EMAIL_ADDRESS}" ]]; then
        _sphinx_usage_title
        _sphinx_usage_update_translations
        _sphinx_usage_terminate
      fi
      sphinx_update_translations
      ;;
    :)
      _sphinx_usage
      ;;
    *)
      _sphinx_usage
      ;;
  esac
}

_sphinx_build_documentation() {
  log "INFO" "SPHINX > Preparing to build documentation ..."
  _sphinx_check_python_library sphinx

  if [[ -n "${_SPHINX_GENERATED_TEMPLATE_PATH}" ]] &&
    [[ -e "${_SPHINX_GENERATED_TEMPLATE_PATH}" ]]; then
    log "DEBUG" "SPHINX > Deleting generated templates at '${_SPHINX_GENERATED_TEMPLATE_PATH}' ..."
    rm -r "${_SPHINX_GENERATED_TEMPLATE_PATH}"
  fi

  pushd "${_SPHINX_BASE_PATH}" >> /dev/null

  log "DEBUG" "SPHINX > Cleaning build ..."
  poetry run make clean

  log "INFO" "SPHINX > Building HTML documentation ..."
  poetry run make html

  log "INFO" "SPHINX > Build complete."
  popd >> /dev/null
}

_sphinx_check_base_path() {
  if [[ ! -d "${_SPHINX_BASE_PATH}" ]]; then
    log "ERROR" "SPHINX > The specified path '${_SPHINX_BASE_PATH}' does not exist."
    return 127
  fi
  if [[ ! -f "${_SPHINX_BASE_PATH}/Makefile" ]]; then
    log "ERROR" "SPHINX > The specified path '${_SPHINX_BASE_PATH}' does not contain a Sphinx Makefile."
    return 127
  fi
}

_sphinx_check_project_has_translations() {
  if [[ ! -d "${_SPHINX_BASE_PATH}/locales" ]]; then
    log "WARNING" "SPHINX > The specified path '${_SPHINX_BASE_PATH}' does not contain any translations."
    return 127
  fi
}

_sphinx_check_python_library() {
  # 1:  The Python library shim to search for.

  if ! poetry show -q "${1}"; then
    log "ERROR" "SPHINX > The required Python library '${1}' needs to be added to your virtual environment."
    return 127
  fi
}

_sphinx_check_vale_docker_image_env_var() {
  environment -m "PRECOMMIT_VALE_DOCKER_IMAGE"
  container_cache_image "${PRECOMMIT_VALE_DOCKER_IMAGE}"
}

_sphinx_extract_translations() {
  log "INFO" "SPHINX > Preparing to extract translations ..."
  _sphinx_check_python_library sphinx

  pushd "${_SPHINX_BASE_PATH}" >> /dev/null
  poetry run make gettext
  popd >> /dev/null
}

_sphinx_identify_existing_translations() {
  local _SPHINX_TRANSLATIONS_LANGUAGE_SUB_PATH

  log "DEBUG" "SPHINX > Identifying existing translations ..."

  if ! _sphinx_check_project_has_translations; then
    return 127
  fi

  while IFS= read -r -d '' _SPHINX_TRANSLATIONS_LANGUAGE_SUB_PATH; do
    if ! ls -la "${_SPHINX_TRANSLATIONS_LANGUAGE_SUB_PATH}/LC_MESSAGES/"*.po 1> /dev/null 2>&1; then
      log "WARNING" "Skipping '${_SPHINX_TRANSLATIONS_LANGUAGE_SUB_PATH}' as there are no .po files. "
    else
      _SPHINX_TRANSLATIONS_LANGUAGES+=("$(basename "${_SPHINX_TRANSLATIONS_LANGUAGE_SUB_PATH#*/}")")
    fi
  done < <(find "${_SPHINX_BASE_PATH}/locales" -maxdepth 1 -mindepth 1 -type d -print0)

  if ! ((${#_SPHINX_TRANSLATIONS_LANGUAGES[@]})); then
    log "ERROR" "SPHINX > No existing translations were found."
    return 127
  fi
}

_sphinx_rewrite_pot_headers() {
  # Update the Main PO Files
  sed -i.bak \
    's,^"Report-Msgid-Bugs-To: \\n"$,"Report-Msgid-Bugs-To: '"${_SPHINX_TRANSLATIONS_EMAIL_ADDRESS}"'\\n",g' \
    "${_SPHINX_BASE_PATH}"/build/gettext/*.pot
  sed -i.bak \
    's,^"Language-Team: LANGUAGE <LL@li.org>\\n"$,"Language-Team: LANGUAGE <'"${_SPHINX_TRANSLATIONS_EMAIL_ADDRESS}"'>\\n",g' \
    "${_SPHINX_BASE_PATH}"/build/gettext/*.pot

  # Remove Temporary Files
  find "${_SPHINX_BASE_PATH}/build/gettext" -type f -name "*.bak" -delete
}

_sphinx_usage() {
  _sphinx_usage_title
  _sphinx_usage_add_translation
  _sphinx_usage_build
  _sphinx_usage_missing_translations
  _sphinx_usage_spell_check
  _sphinx_usage_update_translations
  _sphinx_usage_terminate
}

_sphinx_usage_add_translation() {
  log "ERROR" "--------------------------------------------------------------------------------"
  log "ERROR" "add            < add a new language to the project"
  log "ERROR" "documentation-sphinx.sh add"
  log "ERROR" "               -e [CONTACT EMAIL (written to .po and .pot files)]"
  log "ERROR" "               -g [OPTIONAL PATH TO DELETE SPHINX GENERATED TEMPLATES]"
  log "ERROR" "               -p [BASE FILE PATH ('documentation' folder or similar)]"
}

_sphinx_usage_build() {
  log "ERROR" "--------------------------------------------------------------------------------"
  log "ERROR" "build          < build the documentation (for the current system language)"
  log "ERROR" "documentation-sphinx.sh build"
  log "ERROR" "               -g [OPTIONAL PATH TO DELETE SPHINX GENERATED TEMPLATES]"
  log "ERROR" "               -p [BASE FILE PATH ('documentation' folder or similar)]"
}

_sphinx_usage_missing_translations() {
  log "ERROR" "--------------------------------------------------------------------------------"
  log "ERROR" "missing        < search for untranslated strings"
  log "ERROR" "documentation-sphinx.sh missing"
  log "ERROR" "               -g [OPTIONAL PATH TO DELETE SPHINX GENERATED TEMPLATES]"
  log "ERROR" "               -m [EMPTY MESSAGE MATCH STRING (defaults to 'msgstr ""')]"
  log "ERROR" "               -p [BASE FILE PATH ('documentation' folder or similar)]"
  log "ERROR" "               -s [LANGUAGES TO SKIP (use multiple times as needed)]"
}

_sphinx_usage_spell_check() {
  log "ERROR" "--------------------------------------------------------------------------------"
  log "ERROR" "spell_check    < build and check documentation (for the current system language)"
  log "ERROR" "documentation-sphinx.sh spell_check"
  log "ERROR" "               -i [CONTAINER IMAGE WITH VALE BINARIES]"
  log "ERROR" "               -g [OPTIONAL PATH TO DELETE SPHINX GENERATED TEMPLATES]"
  log "ERROR" "               -p [BASE FILE PATH ('documentation' folder or similar)]"
}

_sphinx_usage_terminate() {
  exit 127
}

_sphinx_usage_title() {
  log "ERROR" "documentation-sphinx.sh -- manage Sphinx documentation tasks"
}

_sphinx_usage_update_translations() {
  log "ERROR" "--------------------------------------------------------------------------------"
  log "ERROR" "update         < extract strings from the documentation and update all files"
  log "ERROR" "documentation-sphinx.sh update"
  log "ERROR" "               -e [CONTACT EMAIL (written to .po and .pot files)]"
  log "ERROR" "               -g [OPTIONAL PATH TO DELETE SPHINX GENERATED TEMPLATES]"
  log "ERROR" "               -p [BASE FILE PATH ('documentation' folder or similar)]"
}

sphinx_add_translation() {
  local _SPHINX_TRANSLATION

  # shellcheck disable=SC2128
  if [[ -z "${SPHINX_TRANSLATIONS_LANGUAGES}" ]]; then
    log "ERROR" "You must set the environment variable 'SPHINX_TRANSLATIONS_LANGUAGES' to add new languages."
    log "ERROR" "Please assign a space separated list of new language codes from:"
    log "ERROR" "  ${GETTEXT_TRANSLATIONS_EXAMPLE_LANGUAGES_CODES_URL}"
    log "ERROR" "For example:"
    log "ERROR" "  export SPHINX_TRANSLATIONS_LANGUAGES='en de fr ko'"
    return 127
  fi

  _sphinx_check_base_path
  _sphinx_extract_translations
  _sphinx_rewrite_pot_headers
  _sphinx_check_python_library sphinx-intl

  pushd "${_SPHINX_BASE_PATH}" >> /dev/null
  for _SPHINX_TRANSLATION in ${SPHINX_TRANSLATIONS_LANGUAGES}; do
    log "DEBUG" "SPHINX > Preparing to generate '${_SPHINX_TRANSLATION}' ..."
    poetry run sphinx-intl update -p build/gettext -l "${_SPHINX_TRANSLATION}"
    log "INFO" "SPHINX > Translations for '${_SPHINX_TRANSLATION}' have been created !"
  done
  popd >> /dev/null
}

sphinx_build() {
  _sphinx_check_base_path
  _sphinx_build_documentation
}

sphinx_missing_translations() {
  local _SPHINX_TRANSLATION
  local _SPHINX_TRANSLATION_TO_SKIP
  local _SPHINX_TRANSLATION_PO_FILE
  local _SPHINX_TRANSLATION_MISSING=0

  _sphinx_check_base_path

  if ! _sphinx_identify_existing_translations; then
    return 0
  fi

  for _SPHINX_TRANSLATION in "${_SPHINX_TRANSLATIONS_LANGUAGES[@]}"; do

    for _SPHINX_TRANSLATION_TO_SKIP in "${_SPHINX_TRANSLATIONS_LANGUAGES_BEING_SKIPPED[@]}"; do
      if [[ "${_SPHINX_TRANSLATION_TO_SKIP}" == "${_SPHINX_TRANSLATION}" ]]; then
        log "WARNING" "Skipping checks on '${_SPHINX_TRANSLATION}' ..."
        break
      fi
      _SPHINX_TRANSLATION_TO_SKIP=""
    done

    if [[ -n "${_SPHINX_TRANSLATION_TO_SKIP}" ]]; then
      continue
    fi

    log "INFO" "SPHINX > Checking '${_SPHINX_TRANSLATION}' for missing translations ..."
    for _SPHINX_TRANSLATION_PO_FILE in "${_SPHINX_BASE_PATH}/locales/${_SPHINX_TRANSLATION}/LC_MESSAGES/"*.po; do
      if [[ "$(
        grep \
          -c \
          "${_SPHINX_TRANSLATIONS_EMPTY_MESSAGE_MATCH}" \
          "${_SPHINX_TRANSLATION_PO_FILE}" ||
          true
      )" -gt "1" ]] \
        ; then
        log "ERROR" "SPHINX > Found untranslated strings: '${_SPHINX_TRANSLATION_PO_FILE}' !"
        _SPHINX_TRANSLATION_MISSING=127
        continue
      fi
    done
    log "INFO" "SPHINX > Check for '${_SPHINX_TRANSLATION}' is complete."
  done
  return "${_SPHINX_TRANSLATION_MISSING}"
}

sphinx_spell_check() {
  local _SPHINX_HTML_FILE
  local _SPHINX_HTML_FILES

  _SPHINX_HTML_FILES=()

  _sphinx_check_base_path
  _sphinx_check_vale_docker_image_env_var

  log "INFO" "SPHINX > Starting documentation spell check ..."

  log "DEBUG" "Collecting HTML filenames ..."
  while IFS= read -r -d '' _SPHINX_HTML_FILE; do
    _SPHINX_HTML_FILES+=("${_SPHINX_HTML_FILE}")
  done < <(find ./"${_SPHINX_BASE_PATH}"/build/html -type f -name "*.html" -print0)

  log "DEBUG" "Docker Image: '${PRECOMMIT_VALE_DOCKER_IMAGE}'"
  log "DEBUG" "Running vale ..."

  container_cache_image "${PRECOMMIT_VALE_DOCKER_IMAGE}"
  container "${PRECOMMIT_VALE_DOCKER_IMAGE}" vale "${_SPHINX_HTML_FILES[@]}"

  log "INFO" "SPHINX > Documentation spell check has passed !"
}

sphinx_update_translations() {
  local _SPHINX_TRANSLATION

  _sphinx_check_base_path

  if ! _sphinx_identify_existing_translations; then
    return 0
  fi

  _sphinx_extract_translations
  _sphinx_rewrite_pot_headers

  pushd "${_SPHINX_BASE_PATH}" >> /dev/null
  for _SPHINX_TRANSLATION in "${_SPHINX_TRANSLATIONS_LANGUAGES[@]}"; do
    log "DEBUG" "SPHINX > Preparing to update '${_SPHINX_TRANSLATION}' ..."
    poetry run sphinx-intl update -p build/gettext -l "${_SPHINX_TRANSLATION}"
    log "INFO" "SPHINX > Translations for '${_SPHINX_TRANSLATION}' have been updated !"
  done
  popd >> /dev/null
}

main() {
  local _SPHINX_BASE_PATH
  local _SPHINX_GENERATED_TEMPLATE_PATH
  local _SPHINX_TRANSLATIONS_EMAIL_ADDRESS
  local _SPHINX_TRANSLATIONS_EMPTY_MESSAGE_MATCH
  local _SPHINX_TRANSLATIONS_LANGUAGES
  local _SPHINX_TRANSLATIONS_LANGUAGES_BEING_SKIPPED
  local PRECOMMIT_VALE_DOCKER_IMAGE

  _SPHINX_TRANSLATIONS_EMPTY_MESSAGE_MATCH='msgstr ""'
  _SPHINX_TRANSLATIONS_LANGUAGES=()
  _SPHINX_TRANSLATIONS_LANGUAGES_BEING_SKIPPED=()

  _sphinx_args "$@"
}

main "$@"
