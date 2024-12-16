#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Project configuration
PYTHON_VERSION="3.13.0"
PROJECT_NAME="myproject"
PYENV_NAME="PY${PYTHON_VERSION}"

log() {
    echo -e "${BLUE}➜ $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

show_command() {
    echo -e "${YELLOW}$ $1${NC} 2>&1"
}

install_system_dependencies() {
    log "Installing system dependencies..."

    if [[ "$(uname)" == "Darwin" ]]; then
        show_command "brew update"
        brew update 2>&1 || error "Failed to update Homebrew"

        show_command "brew install openssl readline sqlite3 xz zlib"
        brew install openssl readline sqlite3 xz zlib 2>&1 || error "Failed to install brew packages"
    else
        show_command "sudo apt-get update"
        sudo apt-get update 2>&1 || error "Failed to update apt"

        show_command "sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"
        sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
            libbz2-dev libreadline-dev libsqlite3-dev curl \
            libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
            libffi-dev liblzma-dev 2>&1 || error "Failed to install system packages"
    fi
}

install_pyenv() {
    log "Installing pyenv..."

    if ! command -v pyenv &> /dev/null; then
        show_command "curl https://pyenv.run | bash"
        curl https://pyenv.run | bash 2>&1 || error "Failed to install pyenv"

        # Add pyenv to shell config
        {
            echo 'export PYENV_ROOT="$HOME/.pyenv"'
            echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"'
            echo 'eval "$(pyenv init -)"'
        } >> ~/.bashrc

        if [ -f ~/.zshrc ]; then
            {
                echo 'export PYENV_ROOT="$HOME/.pyenv"'
                echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"'
                echo 'eval "$(pyenv init -)"'
            } >> ~/.zshrc
        fi

        success "Pyenv installed"
    else
        show_command "brew upgrade pyenv"
        brew upgrade pyenv 2>&1 || error "Failed to update pyenv"
        success "Pyenv updated"
    fi
}

uninstall_python() {
    log "Uninstalling Python ${PYTHON_VERSION}..."

    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"

    # Uninstall Python version
    if pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
        show_command "pyenv uninstall -f ${PYTHON_VERSION}"
        pyenv uninstall -f ${PYTHON_VERSION} 2>&1 || error "Failed to uninstall Python ${PYTHON_VERSION}"
        success "Uninstalled Python ${PYTHON_VERSION}"
    else
        error "Python ${PYTHON_VERSION} is not installed"
    fi

    # Uninstall the virtualenv associated with the Python version
    if pyenv virtualenvs --bare | grep -q "^${PYENV_NAME}$"; then
        show_command "pyenv uninstall -f ${PYENV_NAME}"
        pyenv uninstall -f ${PYENV_NAME} 2>&1 || error "Failed to uninstall virtualenv ${PYENV_NAME}"
        success "Uninstalled virtualenv ${PYENV_NAME}"
    else
        error "Virtualenv ${PYENV_NAME} is not installed"
    fi
}

main() {
    log "Starting development environment setup..."

    install_system_dependencies
    install_pyenv
    uninstall_python
    success "Setup complete! 🎉"
    echo "Please restart your terminal or run:"
    echo "source ~/.bashrc  # or source ~/.zshrc for zsh users"
}

main


# chmod +x scripts/dev/dev_environment_uninstall.sh
# ./scripts/dev/dev_environment_uninstall.sh
# done
