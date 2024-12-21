#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
DEFAULT_DB_NAME="ed_project_db"
DEFAULT_DB_USER="ed_project_user"
DEFAULT_DB_PASSWORD="ed_project_password"

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

verify_postgres() {
    log "Verifying PostgreSQL connection..."
    if ! psql -U postgres -c "SELECT 1;" >/dev/null 2>&1; then
        error "PostgreSQL is not running or cannot connect as postgres user"
    fi
}

verify_database_exists() {
    local db_name=$1
    if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        error "Database $db_name does not exist!"
    fi
}

verify_user_exists() {
    local db_user=$1
    if ! psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$db_user'" | grep -q 1; then
        error "User $db_user does not exist!"
    fi
}

delete_database() {
    log "Preparing to delete development database..."

    # Check for .env file
    if [ ! -f .env ]; then
        error ".env file not found"
    fi

    # Load environment variables
    show_command "source .env"
    source .env

    # Set variables
    db_name=${DB_NAME:-$DEFAULT_DB_NAME}
    db_user=${DB_USER:-$DEFAULT_DB_USER}

    # Validate inputs
    if [[ ! "$db_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error "Invalid database name: $db_name"
    fi
    if [[ ! "$db_user" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error "Invalid database user: $db_user"
    fi

    # Verify PostgreSQL is running
    verify_postgres

    # Verify database and user exist
    verify_database_exists "$db_name"
    verify_user_exists "$db_user"

    # Show current database size
    log "Current database size:"
    show_command "psql -U postgres -c \"SELECT pg_size_pretty(pg_database_size('$db_name')) as db_size;\""

    # Confirm deletion
    log "About to delete:"
    log "Database: $db_name"
    log "User: $db_user"
    log "Are you sure you want to proceed with deletion? (yes/no): "
    read -p "Are you sure you want to proceed with deletion? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log "Aborting database deletion."
        exit 0
    fi

    log "Starting database deletion process..."

    # Count active connections
    local active_connections=$(psql -U postgres -tAc "SELECT count(*) FROM pg_stat_activity WHERE datname = '$db_name';")
    if [ "$active_connections" -gt "0" ]; then
        log "Terminating $active_connections active connection(s)..."
        show_command "psql -U postgres -c \"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$db_name';\""
    fi

    # Drop the database
    log "Dropping database..."
    show_command "psql -U postgres -c \"DROP DATABASE IF EXISTS $db_name;\"" || error "Failed to drop database"

    # Clean up user permissions and objects
    log "Cleaning up user permissions and objects..."
    show_command "psql -U postgres -c \"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM $db_user;\"" || true
    show_command "psql -U postgres -c \"REASSIGN OWNED BY $db_user TO postgres;\"" || true
    show_command "psql -U postgres -c \"DROP OWNED BY $db_user;\"" || true

    # Drop the user
    log "Dropping user..."
    show_command "psql -U postgres -c \"DROP USER IF EXISTS $db_user;\"" || error "Failed to drop user"

    # Verify deletion
    if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        error "Database deletion verification failed - database still exists!"
    fi
    if psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$db_user'" | grep -q 1; then
        error "User deletion verification failed - user still exists!"
    fi

    success "Database and user deleted successfully!"
    log "If you want to recreate the database, run:"
    echo -e "${YELLOW}$ ./scripts/dev/dev_database_create.sh${NC}"
}

main() {
    log "Starting database deletion process..."
    delete_database
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main

# chmod +x scripts/dev/dev_database_delete.sh
# ./scripts/dev/dev_database_delete.sh
# done
