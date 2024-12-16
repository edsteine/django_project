#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PYTHON_VERSION="3.13.0"
PROJECT_NAME="myproject"
PYENV_NAME="PY${PYTHON_VERSION}"

log() {
    echo -e "${BLUE}🔧 $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

show_command() {
    echo -e "${YELLOW}$ $1${NC} 2>&1"
}

deactivate_environment() {
    log "Deactivating any active environment..."
    if [ -n "$VIRTUAL_ENV" ]; then
        show_command "deactivate"
        deactivate 2>/dev/null || true
    fi
    show_command "pyenv deactivate"
    pyenv deactivate 2>/dev/null || true
}

verify_environment_exists() {
    log "Verifying environment exists..."
    show_command "pyenv virtualenvs | grep $PYENV_NAME"
    if ! pyenv virtualenvs | grep -q "$PYENV_NAME"; then
        log "Environment not found. Running initial setup..."
        show_command "./setup.sh"
        ./setup.sh 2>&1 || error "Setup failed"
    fi
}

activate_environment() {
    log "Activating virtual environment..."

    deactivate_environment
    verify_environment_exists

    show_command "eval \$(pyenv init -)"
    eval "$(pyenv init -)" 2>&1

    show_command "pyenv activate $PYENV_NAME"
    if ! pyenv activate "$PYENV_NAME" 2>&1; then
        error "Failed to activate pyenv environment"
    fi

    if [ "$(pyenv version-name)" != "$PYENV_NAME" ]; then
        error "Pyenv activation verification failed"
    fi

    success "Virtual environment activation complete!"
}

main() {
    if [ "$(uname)" != "Darwin" ] && [ "$(uname)" != "Linux" ]; then
        error "Unsupported operating system: $(uname)"
    fi

    activate_environment
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main


# chmod +x scripts/dev/dev_environment_start.sh
# ./scripts/dev/dev_environment_start.sh
# done
