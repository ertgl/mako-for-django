include ./e2e/Makefile

.DEFAULT_GOAL := all

PROJECT_DIR := $(CURDIR)

HACK_DIR := $(PROJECT_DIR)/hack
HACK_SCRIPTS_DIR := $(HACK_DIR)/scripts

VENV_DIR_NAME := .venv
VENV_DIR := $(PROJECT_DIR)/$(VENV_DIR_NAME)

GLOBAL_PYTHON ?= $(shell which python)
PYTHON := $(VENV_DIR)/bin/python

UV ?= $(shell which uv)

MYPY := $(VENV_DIR)/bin/mypy
RUFF := $(VENV_DIR)/bin/ruff

$(VENV_DIR)/:
	$(GLOBAL_PYTHON) -m venv $(VENV_DIR_NAME)

$(PYTHON): $(VENV_DIR)/

$(MYPY): $(VENV_DIR)/
	$(UV) sync --extra mypy --inexact

$(RUFF): $(VENV_DIR)/
	$(UV) sync --extra ruff --inexact

.PHONY: venv
venv: $(VENV_DIR)/

.PHONY: uv.install
uv.install: venv
	$(UV) sync --all-extras --all-groups --all-packages

.PHONY: uv.install.frozen
uv.install.frozen: venv
	$(UV) sync --all-extras --all-groups --all-packages --dev --frozen

.PHONY: install
install: uv.install

.PHONY: install.frozen
install.frozen: uv.install.frozen

.PHONY: prepare
prepare: install

.PHONY: prepare.frozen
prepare.frozen: install.frozen

.PHONY: ruff.lint
ruff.lint: $(RUFF)
	$(RUFF) check .

.PHONY: ruff.lint.fix
ruff.lint.fix: $(RUFF)
	$(RUFF) check . --fix

.PHONY: ruff.format
ruff.format: $(RUFF)
	$(RUFF) format

.PHONY: mypy.lint
mypy.lint: $(MYPY)
	$(MYPY) .

.PHONY: format_exported_python_symbols
format_exported_python_symbols: $(PYTHON)
	$(PYTHON) $(HACK_SCRIPTS_DIR)/format_exported_python_symbols.py

.PHONY: lint
lint: ruff.lint mypy.lint

.PHONY: lint.fix
lint.fix: ruff.lint.fix

.PHONY: format
format: ruff.lint.fix format_exported_python_symbols ruff.format

.PHONY: test
test: e2e.test

.PHONY: check
check: lint test

.PHONY: all
all: prepare
