# =================================================================
# Django Development Makefile 2024
# Last Updated: 2024-12-21
# =================================================================

# Terminal Colors and Emojis
RED := \033[0;31m
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Project Configuration
PROJECT_NAME := ed_project
DJANGO_SETTINGS := config.settings
COVERAGE_THRESHOLD := 80
CURRENT_TIME := $(shell date "+%Y%m%d_%H%M%S")

# Directory Configuration
BACKUP_DIR := backups
LOG_DIR := logs
STATIC_DIR := static
MEDIA_DIR := media
DOCS_DIR := docs
FIXTURES_DIR := fixtures

# Test Paths
UNIT_TESTS := tests/unit
INTEGRATION_TESTS := tests/integration
E2E_TESTS := tests/e2e
ALL_TESTS :=  $(UNIT_TESTS) $(INTEGRATION_TESTS) $(E2E_TESTS)

# Docker Configuration
DOCKER_COMPOSE := docker compose
DOCKER_REGISTRY := your-registry.com
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(PROJECT_NAME)
DOCKER_TAG := latest

# Kubernetes Configuration
K8S_NAMESPACE := development
K8S_CONTEXT := dev-cluster


# =================================================================
# Help Command
# =================================================================
.PHONY: help
help:
	@echo "$(CYAN)Django Development Makefile 2024$(NC)"
	@echo ""
	@echo "$(YELLOW)Core Commands:$(NC)"
	@echo " setup - Complete project setup"
	@echo " install - Install dependencies"
	@echo " update - Update dependencies"
	@echo "$(YELLOW)Development Commands:$(NC)"
	@echo " dev - Setup development environment"
	@echo " lint - Run all linters"
	@echo " test - Run all tests"
	@echo "$(YELLOW)Database Commands:$(NC)"
	@echo " db-setup - Setup database"
	@echo " db-migrate - Run migrations"
	@echo " db-backup - Backup database"
	@echo "$(YELLOW)Deployment Commands:$(NC)"
	@echo " build - Build project"
	@echo " deploy - Deploy project"

# =================================================================
# Core Installation & Setup
# =================================================================
.PHONY: install-dev update-dev check-tools

# Check if required tools are installed
check-tools:
	@command -v poetry >/dev/null 2>&1 || { echo "$(RED)❌ Poetry is not installed$(NC)"; exit 1; }
	@command -v pre-commit >/dev/null 2>&1 || { echo "$(RED)❌ pre-commit is not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Required tools are installed$(NC)"


# Install development environment
install-dev: check-tools clean
	@echo "$(BLUE)📦 Installing project...$(NC)"

	poetry lock --no-update
	poetry install --with dev --sync || { echo "$(RED)❌ Failed to install dependencies$(NC)"; exit 1; }

	@echo "$(YELLOW)⚡ Setting up pre-commit hooks...$(NC)"
	pre-commit install --install-hooks \
		--hook-type pre-commit \
		--hook-type pre-push \
		--hook-type commit-msg || { echo "$(RED)❌ Failed to install pre-commit hooks$(NC)"; exit 1; }

	@echo "$(YELLOW)🔍 Validating installation...$(NC)"
	poetry check
	poetry run pre-commit run --all-files || true
	@echo "$(GREEN)✅ Development environment ready$(NC)"

# Update dependencies and tools
update-dev: check-tools
	@echo "$(BLUE)🔄 Updating dependencies...$(NC)"

	poetry lock --no-update
	poetry check || { echo "$(RED)❌ Poetry check failed$(NC)"; exit 1; }

	@echo "$(YELLOW)📝 Showing outdated packages...$(NC)"
	poetry show --outdated

	@echo "$(YELLOW)⬆️  Updating packages...$(NC)"
	poetry update || { echo "$(RED)❌ Failed to update dependencies$(NC)"; exit 1; }

	@echo "$(YELLOW)🔄 Updating pre-commit hooks...$(NC)"
	pre-commit autoupdate

	@echo "$(GREEN)✅ Dependencies updated successfully$(NC)"


# =================================================================
# Testing and Quality Assurance
# =================================================================
.PHONY: all-test unit integration e2e trace coverage validate

all-test:
	@echo "$(BLUE)🧪 Running all tests...$(NC)"
	pytest \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-report=xml \
		--cov-fail-under=$(COVERAGE_THRESHOLD) \
		$(ALL_TESTS)
	@echo "$(GREEN)✅ All tests complete$(NC)"

unit:
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	pytest $(UNIT_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "not integration and not e2e"

integration:
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	pytest $(INTEGRATION_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "integration"

e2e:
	@echo "$(BLUE)🧪 Running end-to-end tests...$(NC)"
	pytest $(E2E_TESTS) \
		--cov=$(PROJECT_NAME) \
		--cov-report=term-missing \
		-v -m "e2e"

trace:
	pytest --trace-config

coverage: all-test
	@echo "$(BLUE)📊 Generating coverage reports...$(NC)"
	coverage combine
	coverage report
	coverage html
	@echo "$(GREEN)✅ Coverage reports generated$(NC)"

validate:
	@echo "$(BLUE)🔍 Validating development environment...$(NC)"
	poetry check
	poetry run pytest --version >/dev/null 2>&1 || echo "$(YELLOW)⚠️  pytest not installed$(NC)"
	poetry run mypy --version >/dev/null 2>&1 || echo "$(YELLOW)⚠️  mypy not installed$(NC)"
	poetry run ruff --version >/dev/null 2>&1 || echo "$(YELLOW)⚠️  ruff not installed$(NC)"
	pre-commit run --all-files || true
	@echo "$(GREEN)✅ Validation complete$(NC)"
# =================================================================
# Quality Assurance
# =================================================================
.PHONY: lint security  mypy vulture-check security

# Linting and formatting
lint:
	@echo "$(BLUE)📝 Formatting code...$(NC)"
	poetry run ruff format . || { echo "$(RED)❌ Formatting failed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Formatting complete$(NC)"
	@echo "$(BLUE)🔍 Running linters...$(NC)"
	poetry run ruff check . --fix || { echo "$(RED)❌ Ruff check failed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Lint complete$(NC)"

mypy:
	@echo "$(BLUE)📋 Running type checks...$(NC)"
	set -a; source .env; set +a
	poetry run mypy . || { echo "$(RED)❌ Type checking failed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Type checking complete$(NC)"


# Security checks
security:
	@echo "$(BLUE)🔒 Running security checks...$(NC)"

	@echo "$(YELLOW)Running Bandit security checks...$(NC)"
	poetry run bandit -r . || { echo "$(RED)❌ Bandit security check failed$(NC)"; exit 1; }

	@echo "$(YELLOW)Running dependency audit...$(NC)"
	poetry run pip-audit --ignore ed_project || { echo "$(YELLOW)⚠️  Security vulnerabilities found$(NC)"; }

	@echo "$(GREEN)✅ Security checks complete$(NC)"

vulture-check:
	@echo "$(BLUE)🔒 Running security checks...$(NC)"
	poetry run vulture  || { echo "\033[0;31m❌ Vulture check failed\033[0m"; exit 1; }



# =================================================================
# Django Commands
# =================================================================
.PHONY: runserver shell collectstatic superuser db-status

status:
	@echo "$(BLUE)📊 Checking migration status...$(NC)"
	poetry run python manage.py showmigrations || { echo "$(RED)❌ Failed to show migrations$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Migration status check complete$(NC)"

migrate:
	@echo "$(BLUE)🔄 Running database migrations...$(NC)"

	@echo "$(YELLOW)Making migrations...$(NC)"
	poetry run python manage.py makemigrations || { echo "$(RED)❌ Failed to make migrations$(NC)"; exit 1; }

	@echo "$(YELLOW)Applying migrations...$(NC)"
	poetry run python manage.py migrate || { echo "$(RED)❌ Failed to apply migrations$(NC)"; exit 1; }

	poetry run python manage.py flush --noinput

	poetry run python manage.py makemigrations users
	@echo "$(GREEN)✅ Migrations complete$(NC)"

superuser:
	@echo "$(BLUE)👤 Creating superuser...$(NC)"
	poetry run python manage.py createsuperuser
	@echo "$(GREEN)✅ Superuser created$(NC)"

runserver:
	@echo "$(BLUE)🚀 Starting development server...$(NC)"
	poetry run python manage.py runserver

shell:
	@echo "$(BLUE)🐚 Starting Django shell...$(NC)"
	poetry run python manage.py shell_plus  --ipython
db-shell:
	@echo "$(BLUE)🐚 Starting Django shell...$(NC)"
	poetry run python manage.py dbshell

collectstatic:
	@echo "$(BLUE)📦 Collecting static files...$(NC)"
	poetry run python manage.py collectstatic --noinput


db-backup:
	@echo "$(BLUE)💾 Creating database backup...$(NC)"
	mkdir -p $(BACKUP_DIR)
	poetry run python manage.py dumpdata --indent 2 > $(BACKUP_DIR)/backup_$(CURRENT_TIME).json
	@echo "$(GREEN)✅ Backup created$(NC)"
db-restore:
	@echo "$(BLUE)📥 Restoring database...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)❌ Please specify BACKUP_FILE to restore from$(NC)"; \
		exit 1; \
	fi
	poetry run python manage.py loaddata $(BACKUP_FILE)
	@echo "$(GREEN)✅ Database restored$(NC)"

db-seed:
	@echo "$(BLUE)🌱 Seeding database...$(NC)"
	poetry run python manage.py loaddata $(FIXTURES_DIR)/*.json
	@echo "$(GREEN)✅ Database seeded$(NC)"

cache-clear:
	@echo "$(BLUE)🗑️ Clearing cache...$(NC)"
	poetry run python manage.py clear_cache



# =================================================================
# Evirement Management
# =================================================================
.PHONY: environment-install environment-uninstall environment-start

environment-install:
	@echo "$(BLUE)🔧 Installing environment...$(NC)"
	chmod +x ./scripts/dev/dev_environment_install.sh
	./scripts/dev/dev_environment_install.sh
	@echo "$(GREEN)✅ environment installed$(NC)"

environment-uninstall: clean
	@echo "$(BLUE)🗑️ Uninstalling environment...$(NC)"
	chmod +x ./scripts/dev/dev_environment_uninstall.sh
	./scripts/dev/dev_environment_uninstall.sh
	@echo "$(GREEN)✅ environment uninstalled$(NC)"

environment-start:
	@echo "$(BLUE)🚀 Starting environment...$(NC)"
	chmod +x ./scripts/dev/dev_environment_start.sh
	./scripts/dev/dev_environment_start.sh
	@echo "$(GREEN)✅ environment started$(NC)"
create-test-files:
	@echo "$(BLUE)🚀 Starting generate_test_structure...$(NC)"
	chmod +x ./scripts/dev/generate_test_structure.sh
	./scripts/dev/generate_test_structure.sh
	@echo "$(GREEN)✅ generate_test_structure started$(NC)"

# =================================================================
# Database Management
# =================================================================
.PHONY: postgress-install postgress-uninstall postgress-start db-reset

postgress-install:
	@echo "$(BLUE)🔧 Installing postgress...$(NC)"
	chmod +x ./scripts/dev/dev_postgres_install.sh
	./scripts/dev/dev_postgres_install.sh
	@echo "$(GREEN)✅ postgress installed$(NC)"

postgress-uninstall: clean
	@echo "$(BLUE)🗑️ Uninstalling postgress...$(NC)"
	chmod +x ./scripts/dev/dev_postgres_uninstall.sh
	./scripts/dev/dev_postgres_uninstall.sh
	@echo "$(GREEN)✅ postgress uninstalled$(NC)"

postgress-start:
	@echo "$(BLUE)🚀 Starting postgress...$(NC)"
	chmod +x ./scripts/dev/dev_postgres_start.sh
	./scripts/dev/dev_postgres_start.sh
	@echo "$(GREEN)✅ postgress started$(NC)"


db-reset: clean
	@echo "$(BLUE)🔄 Resetting database...$(NC)"
	chmod +x ./scripts/dev/dev_database_create.sh
	chmod +x ./scripts/dev/dev_database_create.sh
	./scripts/dev/dev_database_delete.sh
	./scripts/dev/dev_database_create.sh
	make migrate
	make superuser
	@echo "$(GREEN)✅ Database reset complete$(NC)"


# =================================================================
# Git Commands
# =================================================================
.PHONY: commit-push


pre-commit-check: clean
	@echo "$(BLUE)🔄 Running pre-commit checks...$(NC)"
	poetry lock --no-update
	poetry run pre-commit run --all-files || { echo "$(YELLOW)⚠️  Pre-commit checks found issues$(NC)"; }
	@echo "$(GREEN)✓ Pre-commit checks complete$(NC)"


commit-push-reset-install:clean install-dev lint
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	git init
	git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git
	git branch -M main
	# Add empty files or folders by ensuring .gitkeep or other placeholders are added
	find . -type d -empty -exec touch {}/.gitkeep \; # Add .gitkeep to empty folders
	git add . # Add all changes, including empty directories with .gitkeep
	git commit -m "Update: $(shell date '+%Y-%m-%d %H:%M:%S')" || true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main
	@echo "$(GREEN)✅ Changes pushed$(NC)"

commit-push-reset: lint
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	git config --global http.postBuffer 524288000
	poetry lock --no-update
	git init
	git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git
	git branch -M main
	# Add empty files or folders by ensuring .gitkeep or other placeholders are added
	find . -type d -empty -exec touch {}/.gitkeep \; # Add .gitkeep to empty folders
	git add . # Add all changes, including empty directories with .gitkeep
	git commit -m "Update: $(shell date '+%Y-%m-%d %H:%M:%S')" || true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main
	@echo "$(GREEN)✅ Changes pushed$(NC)"

commit-push:lint
	@echo "$(BLUE)📝 Committing and pushing changes...$(NC)"
	git config --global http.postBuffer 524288000
	poetry lock --no-update
	git add .|| true
	git commit -m "Update: $(shell date '+%Y-%m-%d %H:%M:%S')"|| true
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	git push --force --set-upstream origin main

	@echo "$(GREEN)✅ Changes pushed$(NC)"


clean:
	@echo "$(BLUE)🧹 Cleaning project...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	poetry env remove --all
	pre-commit clean
	rm -rf .pytest_cache .coverage .mypy_cache .ruff_cache
	@echo "$(GREEN)✅ Clean complete$(NC)"

# =================================================================
# Deployment
# =================================================================
.PHONY: build deploy docker-build docker-up docker-down

# Docker commands
docker-build:
	@echo "$(BLUE)🐳 Building Docker image...$(NC)"
	docker-compose build

docker-up:
	@echo "$(BLUE)🐳 Starting Docker containers...$(NC)"
	docker-compose up -d

docker-down:
	@echo "$(BLUE)🐳 Stopping Docker containers...$(NC)"
	docker-compose down
build: clean
	@echo "$(BLUE)🏗️ Building project...$(NC)"
	poetry build
	@echo "$(GREEN)✅ Build complete$(NC)"

deploy: check-all build
	@echo "$(BLUE)🚀 Deploying project...$(NC)"
	poetry publish
	@echo "$(GREEN)✅ Deploy complete$(NC)"



# =================================================================
# Documentation commands
# =================================================================
docs:
	@echo "$(BLUE)📚 Building documentation...$(NC)"
	poetry run mkdocs build
	@echo "$(GREEN)✅ Documentation built$(NC)"

docs-serve:
	@echo "$(BLUE)🌐 Serving documentation...$(NC)"
	poetry run mkdocs serve


# Set default target
.DEFAULT_GOAL := help

env:
	set -a; source .env; set +a  && mypy .
