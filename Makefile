# Copyright (c) 2026 Dawid Kurek <hello@dawikur.dev>

# ---- arguments ----

# Python executable
PYTHON     ?= python3
# Python executable used for project targets
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_STAMP := $(VENV_DIR)/.installed.stamp
# log tag prefix
LOG_PREFIX ?=
# show commands
V          ?= 0

# ---- options ----

Q.0 := @
Q.1 :=
Q   := $(Q.$(V))

HELP_DESCRIPTION_COLUMN := 26

# ---- variables ----

NAME              := chiroptera
PACKAGE_DIR   := chiroptera
TEST_DIR      := tests
SITE_DIR      := site
SITE_OUTPUT_DIR := build/site
SITE_EXPORT_STAMP := build/.site.stamp
SITE_UI_DIR := .site-ui
SITE_ASSET_DIR ?= $(SITE_OUTPUT_DIR)/assets
SITE_UI_STAMP := $(SITE_UI_DIR)/.fetch.stamp
SITE_UI_ASSETS := foundation.css components.css theme.js scroll-top.js
SITE_UI_REMOTE_REPOSITORY := https://github.com/dawikur/site-ui.git
SITE_UI_REPOSITORY ?= $(if $(shell test -d "$(CURDIR)/../site-ui/.git" && actual="$$(git -C "$(CURDIR)/../site-ui" remote get-url origin 2>/dev/null | sed -E 's|^git@github.com:|https://github.com/|; s|^ssh://git@github.com/|https://github.com/|; s|\.git$$||')" && expected="$$(printf '%s' "$(SITE_UI_REMOTE_REPOSITORY)" | sed -E 's|^git@github.com:|https://github.com/|; s|^ssh://git@github.com/|https://github.com/|; s|\.git$$||')" && test "$$actual" = "$$expected" && printf yes),$(CURDIR)/../site-ui,$(SITE_UI_REMOTE_REPOSITORY))
GENERATE      := scripts/generate_chiroptera
PYTHON_FILES  := $(shell rg --files -g '*.py') \
	bin/chiroptera scripts/generate_chiroptera scripts/generate_screenshots scripts/generate_site
LOG_TAG           = $(if $(LOG_PREFIX),$(LOG_PREFIX)-$(1),$(1))

# ---- settings ----

.DEFAULT_GOAL := build
.DELETE_ON_ERROR:
.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
SHELL := /bin/bash

MAKEFLAGS += --no-print-directory

# ---- targets ----

FORCE:
.PHONY: FORCE

$(SITE_UI_STAMP): FORCE
	$(Q)echo " [ $(call LOG_TAG,fetch-site-ui) ]"
	if [ ! -d "$(SITE_UI_DIR)/.git" ]; then git clone --no-checkout -- "$(SITE_UI_REPOSITORY)" "$(SITE_UI_DIR)"; fi
	git -C "$(SITE_UI_DIR)" fetch --prune origin main
	git -C "$(SITE_UI_DIR)" checkout --detach FETCH_HEAD
	touch "$@"

$(VENV_STAMP): pyproject.toml requirements.txt
	$(Q)$(PYTHON) -m venv "$(VENV_DIR)"
	$(Q)$(VENV_PYTHON) -m pip install -r requirements.txt
	$(Q)$(VENV_PYTHON) -m pip install --editable .
	touch "$@"

$(SITE_EXPORT_STAMP): FORCE $(VENV_STAMP) $(SITE_UI_STAMP)
	rm -rf -- "$(SITE_OUTPUT_DIR)"
	mkdir -p -- "$(SITE_OUTPUT_DIR)"
	cp -R "$(SITE_DIR)/." "$(SITE_OUTPUT_DIR)/"
	+$(Q)$(MAKE) SITE_ASSET_DIR="$(SITE_OUTPUT_DIR)/assets" build
	$(Q)$(VENV_PYTHON) scripts/generate_site "$(SITE_OUTPUT_DIR)"
	mkdir -p "$(SITE_OUTPUT_DIR)/assets/site-ui"
	cp $(addprefix $(SITE_UI_DIR)/,$(SITE_UI_ASSETS)) "$(SITE_OUTPUT_DIR)/assets/site-ui/"
	rm -f -- "$(SITE_OUTPUT_DIR)/assets/chiroptera_tmpl.svg" \
		"$(SITE_OUTPUT_DIR)/assets/og_preview_tmpl.svg" \
		"$(SITE_OUTPUT_DIR)/sample_tmpl.vim" \
		"$(SITE_OUTPUT_DIR)/screenshot_sample.py" \
		"$(SITE_OUTPUT_DIR)/generated-sample.vim"
	touch "$@"

# ---- development targets ----

b build: $(VENV_STAMP) # generate all colorscheme variants and artwork
	$(Q)echo " [ $(call LOG_TAG,build) ]"
	mkdir -p -- "$(SITE_ASSET_DIR)"
	$(VENV_PYTHON) $(GENERATE) --output-dir "$(SITE_ASSET_DIR)"
.PHONY: b build

x screenshots: build # capture terminal screenshots and Open Graph preview
	$(Q)echo " [ $(call LOG_TAG,screenshots) ]"
	$(VENV_PYTHON) scripts/generate_screenshots --output-dir "$(SITE_ASSET_DIR)"
.PHONY: x screenshots

p package: $(VENV_STAMP) # build wheel and source-distribution artifacts
	$(Q)echo " [ $(call LOG_TAG,package) ]"
	$(Q)$(RM) -r "$(CURDIR)/dist"
	$(Q)cd "$(CURDIR)/.." && "$(CURDIR)/$(VENV_PYTHON)" -m build --outdir "$(CURDIR)/dist" "$(CURDIR)"
.PHONY: p package

s site: $(SITE_EXPORT_STAMP) # build publishable site
	$(Q)echo " [ $(call LOG_TAG,site) ]"
.PHONY: s site

t test: $(VENV_STAMP) # run the test suite
	$(Q)echo " [ $(call LOG_TAG,test) ]"
	$(Q)$(VENV_PYTHON) -m pytest --cov=$(PACKAGE_DIR) --cov-report=term-missing --cov-fail-under=100
.PHONY: t test

l lint: $(VENV_STAMP) # run static checks
	$(Q)echo " [ $(call LOG_TAG,lint) ]"
	$(Q)$(VENV_PYTHON) -m isort $(PYTHON_FILES)
	$(Q)$(VENV_PYTHON) -m black $(PYTHON_FILES)
	$(Q)$(VENV_PYTHON) -m basedpyright $(PYTHON_FILES)
	$(Q)$(VENV_PYTHON) -m pylint $(PYTHON_FILES)
.PHONY: l lint

c clean: # remove generated artifacts, environments, and caches
	$(Q)echo " [ $(call LOG_TAG,clean) ]"
	$(Q)rm -rf -- \
		"$(SITE_OUTPUT_DIR)" \
		build dist .mypy_cache .pytest_cache .venv venv env ENV \
		.build-venv .site-venv .site-ui chiroptera.egg-info
	$(Q)rm -f -- \
		.nvimlog \
		site/palette.js site/palette.css \
		site/generated-sample.js site/generated-sample.vim \
		site/assets/og_preview.svg
	$(Q)find . -type d -name __pycache__ -prune -exec rm -rf -- {} +
.PHONY: c clean

# ---- help ----

h help: # print help message
	$(Q)echo " [ $(call LOG_TAG,help) ]"

	N="\033[m"
	B="\033[1m"
	I="\033[3m"
	U="\033[4m"

	printf "\n"
	printf " Makefile for the chiroptera colorscheme generator.\n"
	printf "\n"
	printf " %bUsage%b\n" "$$B" "$$N"
	printf "     %bmake%b [%btarget%b] [%barguments%b]...\n" "$$B" "$$N" "$$U" "$$N" "$$U" "$$N"
	printf "\n"
	printf " %bTargets%b\n" "$$B" "$$N"
	awk -v description_column=$(HELP_DESCRIPTION_COLUMN) -F'#' '\
	/^[[:alnum:]_-]+([[:space:]][[:alnum:]_-]+)*:.*#/ { \
		target_part = $$1; \
		sub(/:.*/, "", target_part); \
		split(target_part, a, " "); \
		short = a[1]; \
		long = ""; \
		for (j = 2; j <= length(a); j++) { \
			if (long != "") \
				long = long ", "; \
			long = long a[j]; \
		} \
		++n; \
		shorts[n] = short; \
		longs[n] = long; \
		desc[n] = $$2; \
		if (length(short) > max_short) max_short = length(short); \
		if (length(long) > max_long) max_long = length(long); \
	} \
	END { \
		description_width = description_column - 7; \
		if (max_long > description_width) \
			description_width = max_long; \
		for (i = 1; i <= n; i++) \
			printf "   %" max_short "s %-" description_width "s %s\n", shorts[i], longs[i], desc[i]; \
	}' $(MAKEFILE_LIST)
	printf "\n"
	printf " %bArguments%b\n" "$$B" "$$N"
	awk -v description_column=$(HELP_DESCRIPTION_COLUMN) '\
	/^# ---- arguments ----$$/ { in_arguments = 1; next } \
	in_arguments && /^# ----/ { exit } \
	in_arguments && /^# / { description = substr($$0, 3); next } \
	in_arguments && /^[[:alpha:]_][[:alnum:]_]*[[:space:]]*\?=/ { \
		split($$0, assignment, "?="); \
		name = assignment[1]; \
		default_value = assignment[2]; \
		gsub(/[[:space:]]/, "", name); \
		sub(/^[[:space:]]*/, "", default_value); \
		++n; \
		names[n] = name; \
		descriptions[n] = description; \
		defaults[n] = default_value; \
		if (length(name) > max_name) max_name = length(name); \
		description = ""; \
	} \
	END { \
		description_width = description_column - 6; \
		if (max_name > description_width) description_width = max_name; \
		for (i = 1; i <= n; i++) { \
			printf "     %-" description_width "s %s\n", names[i], descriptions[i]; \
			printf "%" (description_width + 6) "s\033[3mdefault:\033[m %s\n", "", defaults[i]; \
		} \
	}' $(MAKEFILE_LIST)
	printf "\n"
.PHONY: h help
