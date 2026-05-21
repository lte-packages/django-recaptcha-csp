# Development Tasks
.PHONY: help install lint format # test clean pre-commit

ENV_NAME := .venv
# PYTHON_ENV := $(or $(VIRTUAL_ENV),$(ENV_NAME))
PYTHON_ENV := $(ENV_NAME)
# Use absolute path for Python to avoid path issues
ROOT_DIR := $(shell pwd)
PY?=$(ROOT_DIR)/$(PYTHON_ENV)/bin/python
PIP?=$(ROOT_DIR)/$(PYTHON_ENV)/bin/pip

# check if a python virtual environment is activated
PYTHON = $(PY)

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
	git tag -a "$$VERSION" -m "Release version $$VERSION"; \
	git push origin "$$VERSION"
	@echo "Created and pushed git tag $$VERSION"

### Demo Site Tasks ###

demo-install: pip_env  ## Install demo site dependencies
	@echo "Installing django-recaptcha-csp in editable mode..."
	@$(PIP) install -e . --quiet
	@echo "Installing demo site requirements..."
	@$(PIP) install -r demo_site/requirements.txt --quiet
	@echo "✓ Demo dependencies installed"

demo-migrate: pip_env  ## Run database migrations for demo site
	@echo "Running database migrations..."
	@cd demo_site && $(PYTHON) manage.py makemigrations --no-input
	@cd demo_site && $(PYTHON) manage.py migrate --no-input
	@echo "✓ Database ready"

demo-setup: demo-install demo-migrate  ## Complete demo site setup (install + migrate)
	@echo ""
	@echo "=========================================="
	@echo "  Demo site is ready!"
	@echo "  Run: make demo-run"
	@echo "=========================================="

demo-run: pip_env  ## Run the demo development server
	@echo "========================================"
	@echo "  Demo site running at:"
	@echo "  http://localhost:8000/"
	@echo "========================================"
	@echo ""
	@echo "Press Ctrl+C to stop the server"
	@echo ""
	@cd demo_site && $(PYTHON) manage.py runserver

demo-clean:  ## Clean demo site database and temporary files
	@echo "Cleaning demo site..."
	@rm -f demo_site/db.sqlite3
	@rm -rf demo_site/demo_app/migrations/0*.py
	@find demo_site -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Demo site cleaned"