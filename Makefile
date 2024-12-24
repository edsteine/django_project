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
ALL_TESTS := $(UNIT_TESTS) $(INTEGRATION_TESTS) $(E2E_TESTS)

# Docker Configuration
DOCKER_COMPOSE := docker compose
DOCKER_REGISTRY := your-registry.com
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(PROJECT_NAME)
DOCKER_TAG := latest

# Kubernetes Configuration
K8S_NAMESPACE := development
K8S_CONTEXT := dev-cluster

# Define a helper to run a command and print it in yellow
RUN = @printf "$(YELLOW)%s$(NC)\n" "$1" && eval $1
# Test configuration variables
PYTEST_COMMON_FLAGS := -v --cov=$(PROJECT_NAME) --cov-report=term-missing
PYTEST_PARALLEL := -n auto
PYTEST_FAIL_FAST := --maxfail=1
PYTEST_CACHE := --cache-clear
TIMESTAMP := $(shell date +'%Y%m%d_%H%M%S')
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

check-tools:
	@echo "$(BLUE)🔍 VCheck if required tools are installe...$(NC)"
	@command -v poetry >/dev/null  || { echo "$(RED)❌ Poetry is not installed$(NC)"; exit 1; }
	@command -v pre-commit >/dev/null  || { echo "$(RED)❌ pre-commit is not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Required tools are installed$(NC)"

validate:
	@echo "$(BLUE)🔍 Validating development environment...$(NC)"
	poetry check
	@echo "$(YELLOW) poetry run pytest --version >/dev/null $(NC)"
	@poetry run pytest --version >/dev/null || { echo "$(BLUE)⚠️ pytest not installed$(NC)"; exit 1; }
	@echo "$(YELLOW) poetry run mypy --version >/dev/null $(NC)"
	@poetry run mypy --version >/dev/null  || { echo "$(BLUE)⚠️ mypy not installed$(NC)"; exit 1; }
	@echo "$(YELLOW) poetry run ruff --version >/dev/null $(NC)"
	@poetry run ruff --version >/dev/null  || { echo "$(BLUE)⚠️ ruff not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✅ Validation complete$(NC)"

# Install development environment
install-dev: check-tools clean
	@echo "$(BLUE)📦 Installing project...$(NC)"
	$(call RUN, poetry lock --no-update)
	$(call RUN, poetry install --with dev --sync)
	$(call RUN, pre-commit install --install-hooks --hook-type pre-commit --hook-type pre-push --hook-type commit-msg)
	$(call RUN, poetry check)
	@echo "$(GREEN)✅ Development environment ready$(NC)"

# Update dependencies and tools
update-dev: check-tools
	@echo "$(BLUE)🔄 Updating dependencies...$(NC)"
	$(call RUN, poetry lock --no-update)
	$(call RUN, poetry check)
	$(call RUN, poetry show --outdated)
	$(call RUN, poetry update)
	$(call RUN, pre-commit autoupdate)
	@echo "$(GREEN)✅ Dependencies updated successfully$(NC)"


# =================================================================
# Testing and Quality Assurance
# =================================================================
.PHONY: all-tests unit integration e2e trace coverage validate

all-tests:
	@echo "$(BLUE)🧪 Running all tests...$(NC)"
	pytest $(PYTEST_COMMON_FLAGS) \
		--cov-report=html \
		--cov-report=xml \
		--cov-fail-under=$(COVERAGE_THRESHOLD) \
		$(PYTEST_PARALLEL) \
		$(ALL_TESTS)
	@echo "$(GREEN)✅ All tests complete$(NC)"

unit:
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	pytest $(PYTEST_COMMON_FLAGS) \
		-m "not integration and not e2e" \
		$(PYTEST_PARALLEL) \
		$(UNIT_TESTS)
	@echo "$(GREEN)✅ Unit tests complete$(NC)"

integration:
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	pytest $(PYTEST_COMMON_FLAGS) \
		-m "integration" \
		$(INTEGRATION_TESTS)
	@echo "$(GREEN)✅ Integration tests complete$(NC)"

e2e:
	@echo "$(BLUE)🧪 Running end-to-end tests...$(NC)"
	pytest $(PYTEST_COMMON_FLAGS) \
		-m "e2e" \
		$(E2E_TESTS)
	@echo "$(GREEN)✅ E2E tests complete$(NC)"

trace:
	@echo "$(BLUE)🧪 Running trace...$(NC)"
	pytest --trace-config $(PYTEST_CACHE)
	@echo "$(GREEN)✅ Trace complete$(NC)"

coverage: all-test
	@echo "$(BLUE)📊 Generating coverage reports...$(NC)"
	coverage combine || true
	coverage report
	coverage html
	@echo "$(GREEN)✅ Coverage reports generated$(NC)"
	@echo "$(BLUE)📂 Coverage report available at htmlcov/index.html$(NC)"

# =================================================================
# Quality Assurance
# =================================================================
.PHONY: lint security mypy vulture security

# Linting and formatting
lint:
	@echo "$(BLUE)📝 Formatting code...$(NC)"
	$(call RUN, poetry run ruff format .)
	$(call RUN, poetry run ruff check . --fix)
	$(call RUN, poetry run pylint .)
	@echo "$(GREEN)✓ Lint complete$(NC)"

mypy:
	@echo "$(BLUE)📋 Load environment variables from .env file and export them to the shell...$(NC)"
	$(call RUN, set -a; source .env; set +a)
	@echo "$(BLUE)📋 Running type checks...$(NC)"
	$(call RUN, poetry run mypy .)
	@echo "$(GREEN)✓ Type checking complete$(NC)"


# Security checks
security:
	@echo "$(BLUE)🔒 Running security checks...$(NC)"
	$(call RUN, poetry run bandit -r .)
	$(call RUN, poetry run pip-audit --ignore ed_project)
	@echo "$(GREEN)✅ Security checks complete$(NC)"

vulture:
	@echo "$(BLUE)🔒 Running vulture checks...$(NC)"
	$(call RUN, poetry run vulture)
	@echo "$(GREEN)✅ vulture checks complete$(NC)"


# all-lint: lint mypy security vulture
all-lint: lint mypy
# =================================================================
# Django Commands
# =================================================================
.PHONY: runserver shell collectstatic superuser db-status

status:
	@echo "$(BLUE)📊 Checking migration status...$(NC)"
	$(call RUN, poetry run python manage.py showmigrations)
	@echo "$(GREEN)✓ Migration status check complete$(NC)"

migrate-reset:
	@echo "$(BLUE)🔄 Running database migrations...$(NC)"
	@echo "$(BLUE)Making migrations...$(NC)"
	$(call RUN,poetry run python manage.py makemigrations)
	$(call RUN,poetry run python manage.py migrate)
	$(call RUN,poetry run python manage.py flush --noinput)
	$(call RUN,poetry run python manage.py makemigrations users)
	$(call RUN,poetry run python manage.py migrate users)
	@echo "$(GREEN)✅ Migrations complete$(NC)"
show_urls:
	@echo "$(BLUE)🔄 show_urls...$(NC)"
	python manage.py show_urls
migrate:
	@echo "$(BLUE)🔄 Running database migrations...$(NC)"
	@echo "$(BLUE)Making migrations...$(NC)"
	$(call RUN,poetry run python manage.py makemigrations)
	$(call RUN,poetry run python manage.py migrate)
	@echo "$(GREEN)✅ Migrations complete$(NC)"
superuser:
	@echo "$(BLUE)👤 Creating superuser...$(NC)"
	$(call RUN,poetry run python manage.py createsuperuser)
	@echo "$(GREEN)✅ Superuser created$(NC)"

runserver:
	@echo "$(BLUE)🚀 Starting development server...$(NC)"
	$(call RUN,poetry run python manage.py runserver)
ssl:
	@echo "$(BLUE)🚀 Starting development server...$(NC)"
	$(call RUN,python manage.py runserver_plus 0.0.0.0:8000 --cert-file certs/localhost.crt --key-file certs/localhost.key)


shell:
	@echo "$(BLUE)🐚 Starting Django shell...$(NC)"
	$(call RUN,poetry run python manage.py shell_plus --ipython)
db-shell:
	@echo "$(BLUE)🐚 Starting Django shell...$(NC)"
	$(call RUN,poetry run python manage.py dbshell)

collectstatic:
	@echo "$(BLUE)📦 Collecting static files...$(NC)"
	$(call RUN,poetry run python manage.py collectstatic --noinput)

db-backup:
	@echo "$(BLUE)💾 Creating database backup...$(NC)"
	mkdir -p $(BACKUP_DIR)
	$(call RUN, poetry run python manage.py dumpdata --indent 2 > $(BACKUP_DIR)/backup_$(CURRENT_TIME).json)
	@echo "$(GREEN)✅ Backup created$(NC)"
BACKUP_FILE="backups/backup_20241222_171440.json"
db-restore:
	@echo "$(BLUE)📥 Restoring database...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then echo "$(RED)❌ Please specify BACKUP_FILE to restore from$(NC)"; exit 1; \
	fi
	$(call RUN,poetry run python manage.py loaddata $(BACKUP_FILE))
	@echo "$(GREEN)✅ Database restored$(NC)"

db-seed:
	@echo "$(BLUE)🌱 Seeding database...$(NC)"
	$(call RUN,poetry run python manage.py loaddata $(FIXTURES_DIR)/*.json)
	@echo "$(GREEN)✅ Database seeded$(NC)"

cache-clear:
	@echo "$(BLUE)🗑️ Checking if Redis is running...$(NC)"
	@if redis-cli ping > /dev/null 2>&1; then \
		echo "$(GREEN) Redis is running, clearing cache...$(NC)"; \
		echo "$(YELLOW) poetry run python manage.py clear_cache$(NC)"; \
		poetry run python manage.py clear_cache; \
	else \
		echo "$(RED)Redis is not running! Cache not cleared.$(NC)"; \
	fi


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
	chmod +x ./scripts/dev/dev_database_delete.sh
	chmod +x ./scripts/dev/dev_database_create.sh
	./scripts/dev/dev_database_delete.sh
	./scripts/dev/dev_database_create.sh
	make migrate-reset
	make superuser
	@echo "$(GREEN)✅ Database reset complete$(NC)"


# =================================================================
# Git Commands
# =================================================================
.PHONY: commit-push clean-git pre-commit commit-push-reset-install commit-push-reset


pre-commit: clean
	@echo "$(BLUE)🔄 Running pre-commit checks...$(NC)"
	$(call RUN, poetry lock --no-update)
	$(call RUN, poetry run pre-commit run --all-files)
	@echo "$(GREEN)✓ Pre-commit checks complete$(NC)"


commit-push-reset-install:clean install-dev lint
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	find . -type d -empty -exec touch {}/.gitkeep \;
	$(call RUN, git init)
	$(call RUN, git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git)
	$(call RUN, git branch -M main)
	$(call RUN, git add .)
	$(call RUN, git commit -m "Update_$(TIMESTAMP)")
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	$(call RUN, git push --force --set-upstream origin main)
	@echo "$(GREEN)✅ Changes pushed$(NC)"

commit-push-reset: lint
	@echo "$(BLUE)🎯 Committing changes...$(NC)"
	find . -type d -empty -exec touch {}/.gitkeep \;
	$(call RUN, poetry lock --no-update)
	$(call RUN, git init)
	$(call RUN, git remote get-url origin || git remote add origin https://github.com/edsteine/django_project.git)
	$(call RUN, git branch -M main)
	$(call RUN, git add .)
	$(call RUN, git commit -m "Update_$(TIMESTAMP)")
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	$(call RUN, git push --force --set-upstream origin main)
	@echo "$(GREEN)✅ Changes pushed$(NC)"


commit:
	@echo "$(BLUE)📝 Committing and pushing changes...$(NC)"
	$(call RUN,git add .gitignore)
	$(call RUN, poetry lock --no-update)
	$(call RUN, git add .)
	$(call RUN, git commit -m "Update_$(TIMESTAMP)")
	@echo "$(GREEN)✅ Changes committed$(NC)"
	@echo "$(BLUE)🚀 Pushing changes...$(NC)"
	$(call RUN, git push --force --set-upstream origin main)
	@echo "$(GREEN)✅ Changes pushed$(NC)"

clean-git: clean
	pre-commit clean
	pre-commit gc
	git config --global http.postBuffer 1048576000
	git gc --prune=now
	git remote prune origin
	git config --global core.compression 9
	git config --global http.lowSpeedLimit 500
	git config --global http.lowSpeedTime 600


clean:
	@echo "$(BLUE)🧹 Cleaning project...$(NC)"
	@find . -type d -name "backups" -exec rm -rf {} +
	@find . -type d -name "logs" -exec rm -rf {} +
	@find . -type d -name "staticfiles" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@find . -type d -name "poetry.lock" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name "dist" -exec rm -rf {} +
	@find . -type d -name "build" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type f -name "poetry.lock" -delete
	@find . -type f -name "dump.rdb" -delete
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type f -name "coverage.xml" -delete

	@poetry env remove --all
	@pre-commit clean
	@rm -rf .pytest_cache .coverage .mypy_cache .ruff_cache
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
	set -a; source .env; set +a && mypy .
