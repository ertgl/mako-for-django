.DEFAULT_GOAL := all

base_dir := $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

E2E_PROJECT_DIR := $(base_dir)

E2E_VENV_DIR_NAME := .venv
E2E_VENV_DIR := $(E2E_PROJECT_DIR)/$(E2E_VENV_DIR_NAME)

E2E_GLOBAL_PYTHON ?= $(shell which python)
E2E_PYTHON := $(E2E_VENV_DIR)/bin/python

E2E_UV ?= $(shell which uv)

E2E_MANAGE_PY := $(E2E_PROJECT_DIR)/manage.py

$(E2E_VENV_DIR)/:
	$(E2E_GLOBAL_PYTHON) -m venv $(E2E_VENV_DIR_NAME)

$(E2E_PYTHON): $(E2E_VENV_DIR)/

.PHONY: e2e.venv
e2e.venv: $(E2E_VENV_DIR)/

.PHONY: e2e.uv.install
e2e.uv.install: e2e.venv
	VIRTUAL_ENV=$(E2E_VENV_DIR) $(E2E_UV) --directory $(E2E_PROJECT_DIR) sync --all-extras --all-groups --all-packages

.PHONY: e2e.uv.install.frozen
e2e.uv.install.frozen: e2e.venv
	VIRTUAL_ENV=$(E2E_VENV_DIR) $(E2E_UV) --directory $(E2E_PROJECT_DIR) sync --all-extras --all-groups --all-packages --dev --frozen

.PHONY: e2e.install
e2e.install: e2e.uv.install

.PHONY: e2e.install.frozen
e2e.install.frozen: e2e.uv.install.frozen

.PHONY: e2e.prepare
e2e.prepare: e2e.install

.PHONY: e2e.prepare.frozen
e2e.prepare.frozen: e2e.install.frozen

.PHONY: e2e.test
e2e.test: e2e.prepare
	$(E2E_PYTHON) $(E2E_MANAGE_PY) test --pattern="*_test_case.py" django_mako_e2e.modules.samples

.PHONY: all
all: e2e.prepare
