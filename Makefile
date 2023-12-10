#!/usr/bin/make -f

.PHONY: help fmt lint format-toml lint-markdown lint-workflows lint-yaml release security spelling

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  fmt               to format all files"
	@echo "  lint              to lint all files"
	@echo "  format-toml       to format TOML files"
	@echo "  lint-markdown     to lint Markdown files"
	@echo "  lint-workflows    to lint GitHub workflows"
	@echo "  lint-yaml         to lint YAML files"
	@echo "  release           to create a release"
	@echo "  security          to check for credential leaks"
	@echo "  spelling          to check spelling"

fmt: format-toml
hog: security
lint: lint-markdown lint-workflows lint-yaml

format-shell:
	@echo "Checking shell scripts ..."
	@poetry run bash -c "pre-commit run format-shell --all-files --verbose"
	@echo "Done."

format-toml:
	@echo "Checking TOML files ..."
	@poetry run bash -c "pre-commit run format-toml --all-files --verbose"
	@echo "Done."


lint-markdown:
	@echo "Checking Markdown files ..."
	@poetry run bash -c "pre-commit run markdownlint --all-files --verbose"
	@echo "Done."

lint-workflows:
	@echo "Checking workflows ..."
	@poetry run bash -c "pre-commit run lint-github-workflow --all-files --verbose"
	@poetry run bash -c "pre-commit run lint-github-workflow-header --all-files --verbose"
	@echo "Done."

lint-yaml:
	@echo "Checking YAML files ..."
	@poetry run bash -c "pre-commit run yamllint --all-files --verbose"
	@echo "Done."

release:
	@echo "Creating Release ..."
	@poetry run bash -c "cz bump -s"
	@echo "Done."

security:
	@echo "Checking security ..."
	@poetry run bash -c "pre-commit run security-credentials --all-files --verbose"
	@echo "Done."

spelling:
	@echo "Checking spelling ..."
	@poetry run bash -c "pre-commit run spelling-markdown --all-files --verbose"
	@echo "Done."
