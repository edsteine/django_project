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

verify_postgres_connection() {
    log "Verifying PostgreSQL connection..."

    # Wait for PostgreSQL to be ready
    for i in {1..30}; do
        if psql -U postgres -c "SELECT 1;" >/dev/null 2>&1; then
            success "PostgreSQL is accepting connections"
            return 0
        fi
        echo "Waiting for PostgreSQL to accept connections... ($i/30)"
        sleep 1
    done

    error "PostgreSQL is not accepting connections after 30 seconds"
}

check_and_start_postgres_macos() {
    log "Checking PostgreSQL status on macOS..."

    local service_name="postgresql@${PG_VERSION}"

    show_command "brew services list | grep $service_name || echo 'Service not found'"
    if ! brew services list | grep -q "$service_name"; then
        error "PostgreSQL ${PG_VERSION} is not installed. Please run install script first."
    fi

    if ! brew services list | grep "$service_name" | grep -q "started"; then
        log "Starting PostgreSQL ${PG_VERSION}..."
        show_command "brew services start $service_name"
        verify_postgres_connection
    else
        log "PostgreSQL ${PG_VERSION} is already running"
        verify_postgres_connection
    fi

    # Show database status
    show_command "psql -U postgres -c '\\l' || echo 'Could not list databases'"
}

check_and_start_postgres_linux() {
    log "Checking PostgreSQL status on Linux..."

    show_command "systemctl is-active postgresql || echo 'Service not active'"
    if ! systemctl is-active --quiet postgresql; then
        log "Starting PostgreSQL service..."
        show_command "sudo systemctl start postgresql"
        show_command "sudo systemctl enable postgresql"
    else
        log "PostgreSQL service is already running"
    fi

    show_command "systemctl status postgresql"
    verify_postgres_connection

    # Show database status
    show_command "sudo -u postgres psql -c '\\l' || echo 'Could not list databases'"
}

main() {
    log "Checking and starting PostgreSQL version ${PG_VERSION}..."

    case "$(uname)" in
        "Darwin")
            check_and_start_postgres_macos
            ;;
        "Linux")
            check_and_start_postgres_linux
            ;;
        *)
            error "Unsupported operating system: $(uname)"
            ;;
    esac

    success "PostgreSQL version ${PG_VERSION} is running!"
    log "You can now connect to PostgreSQL using:"
    echo -e "${YELLOW}$ psql -U postgres${NC}"
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main

# chmod +x scripts/dev/dev_postgres_start.sh
# ./scripts/dev/dev_postgres_start.sh
# done
