#!/usr/bin/make -f

.PHONY: help clean dogfood fmt lint security spelling clean-git format-toml lint-markdown lint-workflows lint-yaml release security-leaks spelling-add spelling-markdown spelling-sync

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean-git         to run git clean"
	@echo "  dogfood           tp update the dogfood commit"
	@echo "  format-toml       to format TOML files"
	@echo "  lint-markdown     to lint markdown files"
	@echo "  lint-workflows    to lint all files"
	@echo "  lint-yaml         to lint YAML files"
	@echo "  release           to create a release"
	@echo "  security-leaks    to check for credential leaks"
	@echo "  spelling-add      to add a regex to the ignore patterns"
	@echo "  spelling-markdown to spellcheck markdown files"
	@echo "  spelling-sync     to synchronize vale packages"

clean: clean-git
fmt: format-toml
lint: lint-markdown lint-workflows lint-yaml
security: security-leaks
spelling: spelling-markdown

clean-git:
	@echo "Cleaning git content ..."
	@git clean -fd
	@echo "Done."

dogfood:
	@echo "Creating dogfood commit ..."
	@sed -i.bak "s,rev: .\{40\},rev: $(shell git rev-parse HEAD),g" .pre-commit-config.yaml; rm .pre-commit-config.yaml.bak
	@git stage .pre-commit-config.yaml
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

release:
	@echo "Creating Release ..."
	@poetry run bash -c "cz bump -s"
	@echo "Done."

security-leaks:
	@echo "Checking security ..."
	@poetry run bash -c "pre-commit run security-credentials --all-files --verbose"
	@echo "Done."

spelling-markdown:
	@echo "Checking spelling ..."
	@poetry run bash -c "pre-commit run spelling-markdown --all-files --verbose"
	@echo "Done."

spelling-sync:
	@echo "Synchronizing vale ..."
	@poetry run bash -c "pre-commit run --hook-stage manual spelling-vale-sync --all-files --verbose"
