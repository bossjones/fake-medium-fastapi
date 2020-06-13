
# -*- coding: utf-8 -*-
# SOURCE: https://github.com/autopilotpattern/jenkins/blob/master/makefile
MAKEFLAGS += --warn-undefined-variables

# SOURCE: https://github.com/luismayta/zsh-servers-functions/blob/b68f34e486d6c4a465703472e499b1c39fe4a26c/Makefile
# Configuration.
SHELL = /bin/bash
ROOT_DIR = $(shell pwd)
PROJECT_BIN_DIR = $(ROOT_DIR)/bin
DATA_DIR = $(ROOT_DIR)/var
SCRIPT_DIR = $(ROOT_DIR)/script

.PHONY: pre-commit-install check-connection-postgres monkeytype-stub monkeytype-apply monkeytype-ci

pre-commit-install: ## install all pre-commit hooks
	pre-commit install -f --install-hooks

check-connection-postgres:
	poetry run scripts/check_connection.py

monkeytype-stub:
	poetry run inv ci.monkeytype -vvvv --test --stub

monkeytype-apply:
	poetry run inv ci.monkeytype -vvvv --test --apply

monkeytype-ci: monkeytype-stub monkeytype-apply
