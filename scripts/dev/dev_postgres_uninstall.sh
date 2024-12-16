#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# PostgreSQL versions to check
PG_VERSIONS=("" "@14" "@15")

log() {
    echo -e "${BLUE}🗑️ $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

show_command() {
    echo -e "${YELLOW}$ $1${NC}"
    eval "$1"
}

check_sudo() {
    if [ "$(id -u)" != "0" ]; then
        if ! sudo -v; then
            error "This script needs sudo privileges to remove some PostgreSQL directories"
        fi
    fi
}

uninstall_postgresql() {
    local version=$1
    log "Uninstalling PostgreSQL${version}..."

    # Stop service
    log "Stopping PostgreSQL${version} service..."
    show_command "brew services stop postgresql${version} || true"

    # Uninstall PostgreSQL
    log "Uninstalling PostgreSQL${version} via Homebrew..."
    show_command "brew uninstall postgresql${version} || true"

    # Remove data directories
    log "Removing PostgreSQL${version} data directories..."
    show_command "rm -rf /usr/local/var/postgresql${version} || true"
    show_command "rm -rf /usr/local/var/log/postgres${version} || true"
    show_command "rm -rf /usr/local/share/postgresql${version} || true"
    show_command "sudo rm -rf /Library/PostgreSQL${version} || true"

    success "PostgreSQL${version} uninstalled"
}

cleanup_brew() {
    log "Cleaning up Homebrew..."
    show_command "brew cleanup"
}

cleanup_path() {
    log "Cleaning up PATH in shell configuration files..."

    local files=("$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc")

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            log "Checking $file..."
            show_command "sed -i '' '/postgresql/d' $file || true"
        fi
    done
}

verify_uninstall() {
    local version=$1
    log "Verifying PostgreSQL${version} uninstallation..."

    if brew list postgresql${version} &>/dev/null; then
        error "PostgreSQL${version} is still installed via Homebrew!"
    fi

    if [ -d "/usr/local/var/postgresql${version}" ] || \
       [ -d "/usr/local/var/log/postgres${version}" ] || \
       [ -d "/usr/local/share/postgresql${version}" ] || \
       [ -d "/Library/PostgreSQL${version}" ]; then
        error "Some PostgreSQL${version} directories still exist!"
    fi

    success "PostgreSQL${version} uninstallation verified"
}

main() {
    log "Starting PostgreSQL uninstallation process..."

    # Check for sudo privileges
    check_sudo

    # Confirm uninstallation
    read -p "⚠️  This will completely remove PostgreSQL and all its data. Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log "Aborting uninstallation."
        exit 0
    fi

    # Uninstall each version
    for version in "${PG_VERSIONS[@]}"; do
        if brew list postgresql${version} &>/dev/null; then
            uninstall_postgresql "${version}"
            verify_uninstall "${version}"
        else
            log "PostgreSQL${version} is not installed via Homebrew"
        fi
    done

    # Clean up
    cleanup_brew
    cleanup_path

    success "PostgreSQL uninstallation complete!"
    log "To reinstall PostgreSQL, run:"
    echo -e "${YELLOW}$ ./scripts/dev/dev_postgres_install.sh${NC}"
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main


# chmod +x scripts/dev/dev_postgres_uninstall.sh
# ./scripts/dev/dev_postgres_uninstall.sh
# done
