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

create_database() {
    log "Ensuring database and user exist..."

    if [ ! -f .env ]; then
        error ".env file not found"
    fi

    # Source environment variables
    show_command "source .env"
    source .env

    db_name=${DB_NAME:-$DEFAULT_DB_NAME}
    db_user=${DB_USER:-$DEFAULT_DB_USER}
    db_password=${DB_PASSWORD:-$DEFAULT_DB_PASSWORD}

    # Validate database name and user
    if [[ ! "$db_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error "Invalid database name: $db_name"
    fi
    if [[ ! "$db_user" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error "Invalid database user: $db_user"
    fi

    # Verify PostgreSQL is running
    verify_postgres

    log "Setting up database with:"
    log "Database: $db_name"
    log "User: $db_user"

    # Create user if doesn't exist
    show_command "psql -U postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='$db_user'\" || echo 'User not found'"
    if ! psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$db_user'" | grep -q 1; then
        show_command "psql -U postgres -c \"CREATE USER $db_user WITH PASSWORD '$db_password';\""
        show_command "psql -U postgres -c \"ALTER USER $db_user WITH SUPERUSER;\""
    else
        log "User $db_user already exists, updating permissions..."
        show_command "psql -U postgres -c \"ALTER USER $db_user WITH SUPERUSER PASSWORD '$db_password';\""
    fi

    # Create database if doesn't exist
    show_command "psql -U postgres -tAc \"SELECT 1 FROM pg_database WHERE datname='$db_name'\" || echo 'Database not found'"
    if ! psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db_name'" | grep -q 1; then
        show_command "psql -U postgres -c \"CREATE DATABASE $db_name OWNER $db_user;\""
        show_command "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;\""

        # Create extensions
        show_command "psql -U postgres -d $db_name -c \"CREATE EXTENSION IF NOT EXISTS \\\"uuid-ossp\\\";\""
        show_command "psql -U postgres -d $db_name -c \"CREATE EXTENSION IF NOT EXISTS \\\"pgcrypto\\\";\""
    else
        log "Database $db_name already exists, updating permissions..."
        show_command "psql -U postgres -c \"ALTER DATABASE $db_name OWNER TO $db_user;\""
        show_command "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;\""
    fi

    # Verify setup
    show_command "psql -U postgres -c \"\\du\" | grep $db_user"
    show_command "psql -U postgres -c \"\\l\" | grep $db_name"

    success "Database setup complete!"
    log "Connection string: postgresql://${db_user}:${db_password}@localhost:5432/${db_name}"
}

main() {
    log "Setting up PostgreSQL database..."
    create_database
    success "Database creation completed successfully!"
    log "You can now connect using:"
    echo -e "${YELLOW}$ psql -U $db_user -d $db_name${NC}"
}

trap 'error "Operation cancelled by user"' INT
trap 'error "An error occurred"' ERR

main

#  chmod +x scripts/dev/dev_database_create.sh
# ./scripts/dev/dev_database_create.sh

# done
