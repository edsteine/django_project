# =================================================================
# Django Development Makefile 2024
# Author: [Your Name]
# Last Updated: 2024-11-23
# =================================================================

# =================================================================
# Terminal Output Configuration
# =================================================================
RED := \033[0;31m
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
CYAN := \033[0;36m
NC := \033[0m  # No Color

# =================================================================
# Project Configuration
# =================================================================
PYTHON := python
PROJECT_NAME := ed_project
PIP := $(PYTHON) -m pip
DJANGO_SETTINGS := config.settings
COVERAGE_THRESHOLD := 80
CURRENT_TIME := $(shell date "+%Y%m%d_%H%M%S")
# Test path definitions
UNIT_TESTS = tests/unit
INTEGRATION_TESTS = tests/integration
E2E_TESTS = tests/e2e
ALL_TESTS = tests
# Directory Configuration
BACKUP_DIR := backups
LOG_DIR := logs
STATIC_DIR := static
MEDIA_DIR := media
DOCS_DIR := docs
FIXTURES_DIR := fixtures

# Docker Configuration
DOCKER_COMPOSE := docker compose
DOCKER_REGISTRY := your-registry.com
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(PROJECT_NAME)
DOCKER_TAG := latest

# Kubernetes Configuration
K8S_NAMESPACE := development
K8S_CONTEXT := dev-cluster

# =================================================================
# Script Paths
# =================================================================
MAKE_EXECUTABLE_SCRIPTS = \
	scripts/dev/dev_database_create.sh \
	scripts/dev/dev_database_delete.sh \
	scripts/dev/dev_database_install.sh \
	scripts/dev/dev_database_uninstall.sh \
	scripts/dev/dev_database_start.sh \
	scripts/dev/dev_environment_install.sh \
	scripts/dev/dev_environment_uninstall.sh \
	scripts/dev/dev_environment_start.sh \
	scripts/deployment/*.sh \
	scripts/monitoring/*.sh \

# =================================================================
# Help Command
# =================================================================
.PHONY: help
help:
	@echo "$(CYAN)Django Development Makefile 2024$(NC)"
	@echo ""
	@echo "$(YELLOW)Core Commands:$(NC)"
	@echo "  setup				 - Initialize complete development environment"
	@echo "  install-dependencies  - Install all project dependencies"
	@echo "  runserver			- Start Django development server"
	@echo ""
	@echo "$(YELLOW)Database Commands:$(NC)"
	@echo "  database-install	 - Install and configure database"
	@echo "  database-start	   - Start database server"
	@echo "  database-backup	  - Create database backup"
	@echo "  database-restore	 - Restore database from backup"
	@echo "  database-migrate	 - Run database migrations"
	@echo "  database-reset	   - Reset database to clean state"
	@echo ""
	@echo "$(YELLOW)Development Commands:$(NC)"
	@echo "  dev-setup		   - Set up development environment"
	@echo "  dev-clean		   - Clean development environment"
	@echo "  dev-reset		   - Reset development environment"
	@echo ""
	@echo "$(YELLOW)Testing Commands:$(NC)"
	@echo "  test				- Run all tests"
	@echo "  test-unit		   - Run unit tests"
	@echo "  test-integration	- Run integration tests"
	@echo "  test-e2e			- Run end-to-end tests"
	@echo "  coverage			- Generate test coverage report"
	@echo ""

# =================================================================
# Environment Setup and Management
# =================================================================
.PHONY: setup-scripts-executable
setup-scripts-executable:
	@echo "$(BLUE)🔑 Making scripts executable...$(NC)"
	@chmod +x scripts/**/*
	@echo "$(GREEN)✅ Scripts are now executable$(NC)"


# =================================================================
# Virtual Environment and Dependencies
# =================================================================
.PHONY: install-dependencies-dev update-dependencies-dev install-dependencies-prod update-dependencies-prod


install-dependencies-dev:
	@echo "$(BLUE)📦 Installing project dependencies development...$(NC)"
	git init   || true # Initialize git if not already initialized
	$(PIP) install --upgrade pip pip-tools || true
	# pip install . || true
	$(PIP) install -e ".[dev]" || true
	# $(PIP) freeze --no-deps > requirements-dev.txt|| true
	$(PIP) freeze > requirements-dev.txt|| true
	pip-sync requirements-dev.txt || true
	pre-commit clean || true
	pre-commit install || true
	pre-commit autoupdate || true
	$(PIP) check || true
	$(PIP) list --outdated || true
	rm requirements-dev.txt || true  # Clean up temporary file
	@echo "$(GREEN)✅ Dependencies installed development$(NC)"

install-dependencies-prod:
	@echo "$(BLUE)📦 Installing project dependencies production...$(NC)"
	$(PIP) install --upgrade pip pip-tools || true
	$(PIP) install -e ".[prod]" || true
	$(PIP) freeze > requirements-prod.txt || true
	pip-sync requirements-prod.txt || true
	git init  || true # Initialize git if not already initialized
	pre-commit install || true
	pre-commit autoupdate || true
	$(PIP) check || true
	$(PIP) list --outdated || true
	rm requirements-prod.txt  || true # Clean up temporary file
	@echo "$(GREEN)✅ Dependencies installed production$(NC)"

update-dependencies-dev:
	@echo "$(BLUE)📦 Updating project dependencies development...$(NC)"
	$(PIP) install --upgrade pip pip-tools || true
	$(PIP) install --upgrade -e ".[dev]" || true
	$(PIP) freeze > requirements-dev.txt || true
	pip-sync requirements-dev.txt || true
	pre-commit autoupdate || true
	$(PIP) check || true
	$(PIP) list --outdated || true
	rm requirements-dev.txt  || true # Clean up temporary file
	@echo "$(GREEN)✅ Dependencies updated development$(NC)"

update-dependencies-prod:
	@echo "$(BLUE)📦 Updating project dependencies production...$(NC)"
	$(PIP) install --upgrade pip pip-tools || true
	$(PIP) install --upgrade -e ".[prod]" || true
	$(PIP) freeze > requirements-prod.txt || true
	pip-sync requirements-prod.txt || true
	pre-commit autoupdate || true
	$(PIP) check || true
	$(PIP) list --outdated || true
	rm requirements-prod.txt  || true # Clean up temporary file
	@echo "$(GREEN)✅ Dependencies updated production$(NC)"


install-dependencies-all:  install-dependencies-dev update-dependencies-dev
	@echo "$(GREEN)✅ All dependencies install completed successfully$(NC)"
# =================================================================
# Evirement Management
# =================================================================
.PHONY: environment-install environment-uninstall environment-start

environment-install: setup-scripts-executable
	@echo "$(BLUE)🔧 Installing environment...$(NC)"
	./scripts/dev/dev_environment_install.sh
	@echo "$(GREEN)✅ environment installed$(NC)"

environment-uninstall: setup-scripts-executable
	@echo "$(BLUE)🗑️ Uninstalling environment...$(NC)"
	./scripts/dev/dev_environment_uninstall.sh
	@echo "$(GREEN)✅ environment uninstalled$(NC)"

environment-start: setup-scripts-executable
	@echo "$(BLUE)🚀 Starting environment...$(NC)"
	./scripts/dev/dev_environment_start.sh
	@echo "$(GREEN)✅ environment started$(NC)"


# =================================================================
# Database Management
# =================================================================
.PHONY: postgress-install postgress-uninstall postgress-start postgress-stop \
		database-backup database-restore database-reset database-seed \
		database-create database-delete

postgress-install: setup-scripts-executable
	@echo "$(BLUE)🔧 Installing postgress...$(NC)"
	./scripts/dev/dev_postgress_install.sh
	@echo "$(GREEN)✅ postgress installed$(NC)"

postgress-uninstall: setup-scripts-executable
	@echo "$(BLUE)🗑️ Uninstalling postgress...$(NC)"
	./scripts/dev/dev_postgress_uninstall.sh
	@echo "$(GREEN)✅ postgress uninstalled$(NC)"

postgress-start: setup-scripts-executable
	@echo "$(BLUE)🚀 Starting postgress...$(NC)"
	./scripts/dev/dev_postgress_start.sh
	@echo "$(GREEN)✅ postgress started$(NC)"


database-create: setup-scripts-executable
	@echo "$(BLUE)🚀 Creating database...$(NC)"
	./scripts/dev/dev_database_create.sh
	@echo "$(GREEN)✅ Database created$(NC)"

database-delete: setup-scripts-executable
	@echo "$(BLUE)🚀 Starting database...$(NC)"
	./scripts/dev/dev_database_delete.sh
	@echo "$(GREEN)✅ Database started$(NC)"

database-backup:
	@echo "$(BLUE)💾 Creating database backup...$(NC)"
	@mkdir -p $(BACKUP_DIR)
	$(PYTHON) manage.py dumpdata --indent 2 > $(BACKUP_DIR)/backup_$(CURRENT_TIME).json
	@echo "$(GREEN)✅ Backup created at $(BACKUP_DIR)/backup_$(CURRENT_TIME).json$(NC)"

database-restore:
	@echo "$(BLUE)📥 Restoring database from backup...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)❌ Please specify BACKUP_FILE to restore from$(NC)"; \
		exit 1; \
	fi
	@$(PYTHON) manage.py loaddata $(BACKUP_FILE)
	@echo "$(GREEN)✅ Database restored from $(BACKUP_FILE)$(NC)"
#  make database-restore BACKUP_FILE=backups/backup_20241125_192846.json
database-reset: setup-scripts-executable
	@echo "$(BLUE)🔄 Resetting database...$(NC)"
	@$(PYTHON) manage.py flush --noinput || true
	@$(PYTHON) manage.py migrate || true
	@echo "$(GREEN)✅ Database reset complete$(NC)"


database-seed:
	@echo "$(BLUE)🌱 Seeding database...$(NC)"
	@$(PYTHON) manage.py loaddata $(FIXTURES_DIR)/*.json
	@echo "$(GREEN)✅ Database seeded$(NC)"

# =================================================================
# Django Management
# =================================================================
.PHONY: migrations migrate superuser static collectstatic runserver

migrations:
	@echo "$(BLUE)🔄 Creating database migrations...$(NC)"
	$(PYTHON) manage.py makemigrations || true
	$(PYTHON) manage.py flush || true
	$(PYTHON) manage.py makemigrations users || true
	@echo "$(GREEN)✅ Migrations created$(NC)"

migrate:
	@echo "$(BLUE)🔄 Applying database migrations...$(NC)"
	$(PYTHON) manage.py migrate
	@echo "$(GREEN)✅ Migrations applied$(NC)"
collectstatic:
	@echo "$(BLUE)🔄 Applying database migrations collectstatic...$(NC)"
	$(PYTHON) manage.py  collectstatic
	@echo "$(GREEN)✅ Migrations collectstatic applied$(NC)"


superuser:
	@echo "$(BLUE)👤 Creating superuser...$(NC)"
	$(PYTHON) manage.py createsuperuser
	@echo "$(GREEN)✅ Superuser created$(NC)"

runserver:
	@echo "$(BLUE)🚀 Starting development server...$(NC)"
	$(PYTHON) manage.py runserver

clean:
	@echo "$(BLUE)🧹 Cleaning project artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +  || true
	find . -type f -name "*.pyc" -delete  || true
	find . -type f -name "*.DS_Store" -delete  || true
	find . -type f -name "*.log" -delete  || true
	find . -type f -name "*.pyo" -delete  || true
	find . -type f -name "*.pyd" -delete  || true
	find . -type f -name ".coverage" -delete  || true
	find . -type f -name "coverage.xml" -delete || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + || true
	find . -type d -name "*.egg" -exec rm -rf {} + || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + || true
	rm -rf build/ dist/ htmlcov/ .coverage staticfiles/ .ruff_cache/ backups/ || true
	@echo "$(GREEN)✅ Clean complete$(NC)"

# =================================================================
# Testing and Quality Assurance
# =================================================================
.PHONY: test test-unit test-integration test-e2e coverage lint format security type-check check-all pre-commit

# Unit tests
test-unit:
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	pytest $(UNIT_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "not integration and not e2e"

# Integration tests
test-integration:
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	pytest $(INTEGRATION_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "integration"

# End-to-end tests
test-e2e:
	@echo "$(BLUE)🧪 Running end-to-end tests...$(NC)"
	pytest $(E2E_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "e2e"

# Full test suite with comprehensive coverage
test:
	@echo "$(BLUE)🧪 Running all tests...$(NC)"
	pytest \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-report=xml \
		--cov-fail-under=$(COVERAGE_THRESHOLD) \
		$(ALL_TESTS)
	@echo "$(GREEN)✅ All tests complete$(NC)"
# Coverage report generation
coverage: test
	@echo "$(BLUE)📊 Generating coverage reports...$(NC)"
	coverage combine  || true
	coverage report  || true
	coverage html  || true
	@echo "$(GREEN)✅ Coverage reports generated in htmlcov/$(NC)"

# Pytest configuration tracing
pytest-trace:
	pytest --trace-config  || true


lint2:
	@echo "$(BLUE)🔍 Running comprehensive code linting and fixing...$(NC)"
	ruff check . --fix  || true
	ruff check .  || true
	black --check .  || true
	black .  || true
	ruff format .  || true
	@echo "$(GREEN)✅ Code analysis complete$(NC)"
lint:
	@echo "$(BLUE)🔍 Running comprehensive code linting and fixing...$(NC)"
	ruff check . --fix || true
	ruff format . || true
	@echo "$(GREEN)✅ Code analysis complete$(NC)"


security:
	@echo "$(BLUE)🔒 Running security checks...$(NC)"
	bandit -r .  || true
	pip-audit  --ignore ed_project  || true
	@echo "$(GREEN)✅ Security checks complete$(NC)"


type-check:
	@echo "$(BLUE)📝 Running type checks...$(NC)"
	mypy .   || true
	@echo "$(GREEN)✅ Type checks complete$(NC)"

# checkall: lint  security type-check
checkall: lint  type-check
# Run all pre-commit hooks
pre-commit:
	pre-commit run --all-files
	# pre-commit run ruff --all-files
	# pre-commit run mypy --all-files

.PHONY: commit-push
# commit-push-reset:  install-dependencies-dev pre-commit
commit-push-reset-install:  install-dependencies-dev
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	git init
	git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git
	git branch -M main
	git add . || true
	git commit -m "Commit changes" || true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main || true
	@echo "$(GREEN)✅ Changes pushed$(NC)"
commit-push-reset:
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	git init
	git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git
	git branch -M main
	git add . || true
	git commit -m "Commit changes" || true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main || true
	@echo "$(GREEN)✅ Changes pushed$(NC)"

commit-push:
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	git add . || true
	git commit -m "Commit changes" || true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main || true
	@echo "$(GREEN)✅ Changes pushed$(NC)"





check-all: lint type-check security test
	@echo "$(GREEN)✅ All quality checks completed successfully$(NC)"

# =================================================================
# Default Target
# =================================================================
.DEFAULT_GOAL := help
