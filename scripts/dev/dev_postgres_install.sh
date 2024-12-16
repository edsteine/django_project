#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# PostgreSQL version
PG_VERSION="15"

# Default admin credentials (can be overridden by environment variables)
PG_ADMIN_USER=${PG_ADMIN_USER:-"postgres"}
PG_ADMIN_PASSWORD=${PG_ADMIN_PASSWORD:-"postgres"}

log() {
    echo -e "${BLUE}🐘 $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

show_command() {
    # Show the command in yellow
    echo -e "${YELLOW}$ $1${NC}"
    # Execute the command and show its output
    eval "$1"
}

configure_postgres_admin() {
    log "Configuring PostgreSQL admin user..."

    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS configuration
        show_command "createuser -s postgres || echo 'Postgres user already exists'"

        show_command "psql postgres -c \"ALTER USER postgres WITH PASSWORD '${PG_ADMIN_PASSWORD}'\""

        local SYSTEM_USER=$(whoami)
        show_command "psql postgres -c \"ALTER USER ${SYSTEM_USER} WITH SUPERUSER PASSWORD '${PG_ADMIN_PASSWORD}'\""
    else
        # Linux configuration
        show_command "sudo -u postgres psql -c \"ALTER USER ${PG_ADMIN_USER} WITH PASSWORD '${PG_ADMIN_PASSWORD}'\""
    fi

    success "PostgreSQL admin user configured"
}

configure_postgres_path() {
    log "Configuring PostgreSQL PATH..."

    # Add PostgreSQL binaries to PATH
    POSTGRES_PATH_CONFIG="export PATH=\"/usr/local/opt/postgresql@${PG_VERSION}/bin:\$PATH\""

    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS path configuration
        if ! grep -q "${POSTGRES_PATH_CONFIG}" ~/.zshrc 2>/dev/null; then
            show_command "echo '${POSTGRES_PATH_CONFIG}' >> ~/.zshrc"
        fi
        if ! grep -q "${POSTGRES_PATH_CONFIG}" ~/.bash_profile 2>/dev/null; then
            show_command "echo '${POSTGRES_PATH_CONFIG}' >> ~/.bash_profile"
        fi

        if [ -f ~/.zshrc ]; then
            show_command "source ~/.zshrc"
        elif [ -f ~/.bash_profile ]; then
            show_command "source ~/.bash_profile"
        fi
    else
        # Linux path configuration
        if ! grep -q "${POSTGRES_PATH_CONFIG}" ~/.bashrc 2>/dev/null; then
            show_command "echo '${POSTGRES_PATH_CONFIG}' >> ~/.bashrc"
        fi
        show_command "source ~/.bashrc"
    fi

    success "PostgreSQL PATH configured"
}

install_postgresql_macos() {
    log "Installing PostgreSQL on macOS..."

    show_command "brew list postgresql@${PG_VERSION} &>/dev/null || echo 'PostgreSQL not installed'"
    if brew list postgresql@${PG_VERSION} &>/dev/null; then
        success "PostgreSQL ${PG_VERSION} is already installed"
        return
    fi

    show_command "brew install postgresql@${PG_VERSION}"
    show_command "brew services start postgresql@${PG_VERSION}"
    show_command "brew link postgresql@${PG_VERSION} --force"

    configure_postgres_path
    configure_postgres_admin

    success "PostgreSQL ${PG_VERSION} installed and configured"
}

install_postgresql_linux() {
    log "Installing PostgreSQL on Linux..."

    show_command "dpkg -l | grep postgresql-${PG_VERSION} || echo 'PostgreSQL not installed'"
    if dpkg -l | grep -q postgresql-${PG_VERSION}; then
        success "PostgreSQL ${PG_VERSION} is already installed"
        return
    fi

    log "Adding PostgreSQL repository..."
    show_command "echo 'deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main' | sudo tee /etc/apt/sources.list.d/pgdg.list"

    show_command "wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -"
    show_command "sudo apt-get update"
    show_command "sudo apt-get install -y postgresql-${PG_VERSION} postgresql-contrib"
    show_command "sudo systemctl start postgresql"
    show_command "sudo systemctl enable postgresql"

    configure_postgres_path
    configure_postgres_admin

    success "PostgreSQL ${PG_VERSION} installed and configured"
}

main() {
    log "Installing PostgreSQL version ${PG_VERSION}..."

    case "$(uname)" in
        "Darwin")
            install_postgresql_macos
            ;;
        "Linux")
            if [ -f "/etc/os-release" ]; then
                if grep -qi "ubuntu\|debian" /etc/os-release; then
                    install_postgresql_linux
                else
                    error "Your Linux distribution is not supported automatically."
                fi
            else
                error "Could not determine Linux distribution"
            fi
            ;;
        *)
            error "Unsupported operating system: $(uname)"
            ;;
    esac

    success "PostgreSQL version ${PG_VERSION} installation complete!"
    log "Admin user: ${PG_ADMIN_USER}"
    log "Admin password: ${PG_ADMIN_PASSWORD}"
    log "To change credentials, run the script with:"
    log "PG_ADMIN_USER=your_user PG_ADMIN_PASSWORD=your_password $0"

    # Show final verification commands
    log "Verify installation with these commands:"
    echo -e "${YELLOW}$ psql --version${NC}"
    echo -e "${YELLOW}$ psql -U postgres -c \"SELECT version();\"${NC}"
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main


# chmod +x scripts/dev/dev_postgres_install.sh
# ./scripts/dev/dev_postgres_install.sh
# done
