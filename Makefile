#!/usr/bin/make -f

.PHONY: help clean dogfood fmt lint security sort spelling clean-git format-toml lint-markdown lint-workflows lint-yaml pre-commit-sort-config pre-commit-sort-hooks release security-leaks spelling-markdown spelling-sort spelling-sync test-python

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean-git                to run git clean"
	@echo "  dogfood                  to update the dogfood commit"
	@echo "  format-toml              to format TOML files"
	@echo "  lint-markdown            to lint markdown files"
	@echo "  lint-workflows           to lint all files"
	@echo "  lint-yaml                to lint YAML files"
	@echo "  pre-commit-sort-config   to create a release"
	@echo "  pre-commit-sort-hooks    to create a release"
	@echo "  release                  to create a release"
	@echo "  security-leaks           to check for credential leaks"
	@echo "  spelling-markdown        to spellcheck markdown files"
	@echo "  spelling-sort            to sort vale vocabularies"
	@echo "  spelling-sync            to synchronize vale packages"
	@echo "  test-python              to test the python scripts"

clean: clean-git
fmt: format-toml
lint: lint-markdown lint-workflows lint-yaml
security: security-leaks
sort: pre-commit-sort-config pre-commit-sort-hooks spelling-sort
spelling: spelling-markdown
test: test-python

clean-git:
	@echo "Cleaning git content ..."
	@git clean -fd
	@echo "Done."

dogfood:
	@echo "Creating dogfood commit ..."
	@sed -i.bak "s,rev: .\{40\},rev: $(shell git rev-parse HEAD),g" .pre-commit-config.yaml .cicd-tools/configuration/pre-commit-bootstrap.yaml; rm .pre-commit-config.yaml.bak .cicd-tools/configuration/pre-commit-bootstrap.yaml.bak
	@git stage .pre-commit-config.yaml .cicd-tools/configuration/pre-commit-bootstrap.yaml
	@git commit -m "ci(PRE-COMMIT): move dog food hash" --no-verify

format-toml:
	@echo "Checking TOML files ..."
	@poetry run bash -c "pre-commit run format-toml --all-files --verbose"
	@echo "Done."

lint-markdown:
	@echo "Checking Markdown files ..."
	@poetry run bash -c "pre-commit run lint-markdown --all-files --verbose"
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

pre-commit-sort-config:
	@echo "Sorting pre-commit config ..."
	@poetry run bash -c "pre-commit run pre-commit-sort-config --all-files --verbose"
	@echo "Done."

pre-commit-sort-hooks:
	@echo "Sorting pre-commit hooks ..."
	@poetry run bash -c "pre-commit run pre-commit-sort-hooks --all-files --verbose"
	@echo "Done."

release:
	@echo "Creating Release ..."
	@poetry run bash -c "cz bump -s"
	@echo "Done."

security-leaks:
	@echo "Checking security ..."
	@poetry run bash -c "pre-commit run sort-pre-commit-config --all-files --verbose"
	@echo "Done."

spelling-markdown:
	@echo "Checking spelling ..."
	@poetry run bash -c "pre-commit run spelling-markdown --all-files --verbose"
	@echo "Done."

spelling-sort:
	@echo "Sorting vale vocabularies ..."
	@poetry run bash -c "pre-commit run spelling-vale-vocab --all-files --verbose"
	@echo "Done."

spelling-sync:
	@echo "Synchronizing vale ..."
	@poetry run bash -c "pre-commit run --hook-stage manual spelling-vale-sync --all-files --verbose"

test-python:
	@echo "Testing python scripts ..."
	@poetry run python src/cicd_tools_pre_commit/tests/test_cicd_tools_pre_commit.py
	@echo "Done."
