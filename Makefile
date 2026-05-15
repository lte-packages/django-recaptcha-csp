# Development Tasks
.PHONY: help install lint format # test clean pre-commit

ENV_NAME := .venv
# PYTHON_ENV := $(or $(VIRTUAL_ENV),$(ENV_NAME))
PYTHON_ENV := $(ENV_NAME)
PY?=$(PYTHON_ENV)/bin/python
PIP?=$(PYTHON_ENV)/bin/pip

# check if a python virtual environment is activated
PYTHON = $(PYTHON_ENV)/bin/python

PHONY: help lint format clean install_build_deps sdist build tag

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

### Python Environment Tasks ##

pip_env:  ## Ensure the Python virtual environment is set up
	# check if PYTHON_ENV = $(ENV_NAME) and if it is then check whether the directory exists
	@-echo "PYTHON_ENV is set to $(PYTHON_ENV)";
	@-if [ "$(PYTHON_ENV)" = $(ENV_NAME) ]; then \
		if [ ! -d "$(PYTHON_ENV)" ]; then \
			echo "Virtual environment created."; \
			python3 -m venv $(ENV_NAME) && $(ENV_NAME)/bin/pip install --upgrade pip; \
		fi; \
	fi

### Ruff Tasks ###

lint: pip_env  ## Run linting with ruff
	$(PYTHON) -m ruff check . --output-format=concise

format: pip_env  ## Format code with ruff
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix . --output-format=concise

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf $(PYTHON_ENV) demo_site/db.sqlite3 demo_site/staticfiles demo_site/media
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# pre-commit-install:  ## Ensure pre-commit is installed and run hooks on all files
# 	$(PYTHON) -m pip install --quiet pre-commit
# 	$(PYTHON) -m pre_commit install

# pre-commit: pre-commit-install ## Run pre-commit hooks on all files
# 	$(PYTHON) -m pre_commit run --all-files

### Build and Release Tasks ###

install_build_deps: pip_env  ## Install build dependencies
	$(PYTHON) -m pip install --quiet build

sdist: install_build_deps  ## Build source distribution
	$(PYTHON) -m build --sdist

build: install_build_deps  ## Build the package
	$(PYTHON) -m build

# create git tag for the current version
tag:  ## Create a git tag for the current version
	@VERSION=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	git tag -a "v$$VERSION" -m "Release version $$VERSION"; \
	git push origin "v$$VERSION"
	@echo "Created and pushed git tag v$$VERSION"