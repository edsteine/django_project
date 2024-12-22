#!/bin/bash

# Base directory for your code and tests
API_DIR="api"
TESTS_DIR="tests"

# Loop through the API directory and mimic the structure in tests/
create_test_files() {
    # Find all Python files in the api folder, including '__init__.py' but skipping them in test naming
    find "$API_DIR" -type f -name "*.py" | while read -r api_file; do
        # Get the relative path from the API root to the current file
        relative_path="${api_file#"$API_DIR"/}"
        # Extract the base name of the file (without the directory)
        file_base_name=$(basename "$relative_path" .py)

        # Get the directory path relative to the 'api' root directory
        dir_name=$(dirname "$relative_path")

        # Mimic the same directory structure in the tests folder for unit, integration, e2e, factories
        mkdir -p "$TESTS_DIR/unit/$dir_name"
        mkdir -p "$TESTS_DIR/integration/$dir_name"
        mkdir -p "$TESTS_DIR/e2e/$dir_name"
        mkdir -p "$TESTS_DIR/factories/$dir_name"

        # Create test files for unit, integration, e2e, and factories with appropriate naming, except for __init__.py
        if [[ "$file_base_name" != "__init__" ]]; then
            touch "$TESTS_DIR/unit/$dir_name/test_${file_base_name}_unit.py"
            touch "$TESTS_DIR/integration/$dir_name/test_${file_base_name}_integration.py"
            touch "$TESTS_DIR/e2e/$dir_name/test_${file_base_name}_e2e.py"
            touch "$TESTS_DIR/factories/$dir_name/${file_base_name}_factory.py"
        else
            # Create __init__.py files in the test folders to match the structure
            touch "$TESTS_DIR/unit/$dir_name/__init__.py"
            touch "$TESTS_DIR/integration/$dir_name/__init__.py"
            touch "$TESTS_DIR/e2e/$dir_name/__init__.py"
            touch "$TESTS_DIR/factories/$dir_name/__init__.py"
        fi

        echo "Created test structure for: $relative_path"
    done

    echo "Test files and directories created."
}

# Run the function to create test files
create_test_files
