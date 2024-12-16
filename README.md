# ED Project

## Project Overview
This is a Django REST API project with user management and encrypted data handling.
The project uses PostgreSQL for database and includes comprehensive test coverage.

## Prerequisites
- Git
- Python 3.13
- PostgreSQL 14
- Make utility

## Quick Start

### Complete Setup
```bash
# Run complete setup (recommended)
make all
```

### Step-by-Step Setup
```bash
make install-system    # Install system dependencies
make install-pyenv     # Install pyenv for Python version management
make install-postgres  # Install PostgreSQL
make setup-venv        # Create virtual environment
make install          # Install project dependencies
make configure-env    # Set up environment variables
make setup-db         # Configure database and run migrations
```

## Available Make Commands

### Setup Commands
```bash
make install-system   # Install system dependencies
make install-pyenv    # Install pyenv
make install-postgres # Install PostgreSQL
make install-python   # Install Python via pyenv
make setup-venv       # Setup virtual environment
make install         # Install project dependencies
make configure-env    # Setup environment variables
make setup-db        # Setup database and run migrations
```

### Development Commands
```bash
make run             # Start development server
make lint            # Run code linters (flake8, black, isort)
make format          # Format code automatically
make test            # Run test suite
```

### Requirements Management
```bash
make pip-compile-core # Compile core requirements
make pip-compile-dev  # Compile development requirements
make pip-compile-test # Compile test requirements
```

### Python Environment
```bash
make pyenv-activate   # Activate pyenv environment
make pyenv-deactivate # Deactivate pyenv environment
```

## Environment Configuration
The project uses `.env.dev` for development settings. Default database configuration:
```ini
DB_NAME=project_db
DB_USER=postgres
DB_PASSWORD=postgres
```

To configure your environment:
1. Create `.env.dev` file: `make configure-env`
2. Edit the generated file with your settings
3. Run database setup: `make setup-db`

## Project Components

### API (api/)
- `V1/`: API version 1 endpoints and resources
- `config_api/`: API-specific configurations
- `core/`: Core functionality modules
  - `cache/`: Caching implementation
  - `encryption/`: Data encryption handlers
  - `logging/`: Custom logging setup
  - `utils/`: Utility functions
- `graphql/`: GraphQL schema and resolvers
- `middleware/`: Custom middleware implementations

### Configuration (config_project/)
- `settings/`: Environment-specific Django settings
- `project_urls.py`: Project-level URL configuration
- `wsgi.py`: WSGI application entry point

### Testing (tests/)
- `e2e/`: End-to-end tests
- `factories/`: Test data factories
- `integration/`: Integration tests
- `unit/`: Unit tests
- `pytest_conftest.py`: Pytest configuration

## Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Run `make lint` before committing changes
- Use `make format` to automatically format code
- Update documentation as needed

## Testing
```bash
make test  # Runs the complete test suite
```

## Maintenance

### Updating Dependencies
1. Update the appropriate `.in` file in the `requirements` directory
2. Run the corresponding pip-compile command:
```bash
make pip-compile-core  # For core requirements
make pip-compile-dev   # For development requirements
make pip-compile-test  # For test requirements
```

### Code Quality
```bash
make lint    # Run linters
make format  # Format code
```

## Troubleshooting

### Common Issues

1. Database Connection Issues
```bash
# Check database status
sudo service postgresql status

# Reset database
make setup-db
```

2. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
make setup-venv
```

3. Permission Issues
```bash
# For PostgreSQL permission issues
sudo -u postgres psql
# Then grant necessary permissions
```

## Contributing
1. Create a new branch for your feature
2. Follow the development guidelines
3. Run tests and linting before committing
4. Submit a pull request

## Technical Stack
- Django & Django REST Framework
- PostgreSQL 14
- Python 3.13
- GraphQL
- Custom encryption handling
- Comprehensive testing suite
- Automated dependency management

## Security Features
- Custom encryption handlers
- Secure data handling
- Environment-based configurations
- Logging and monitoring setup

## Acknowledgments
- Built with Django REST Framework
- Uses PostgreSQL for data storage
- Managed with Make automation
- Includes GraphQL support
- Features custom encryption handling

For more information, contact the project maintainers or consult the development team.

---
Last updated: November 2024

MIT License

Copyright (c) 2024 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
