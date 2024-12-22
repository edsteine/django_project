import logging
import os
import re

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Configure logging based on environment
log_level = logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


def generate_todo_id() -> str:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        todos_path = os.path.join(script_dir, "TODOS.md")

        # Open and read the file
        with open(todos_path, encoding="utf-8") as file:
            for line in file:
                if "Latest TODO ID:" in line:
                    current_id = int(line.split("T")[1].strip())
                    new_id = f"T{str(current_id + 1).zfill(3)}"
                    return new_id
        raise ValueError("TODO ID format not found in TODOS.md")
    except (FileNotFoundError, IndexError, ValueError) as e:
        logger.info("Error: Make sure TODOS.md exists and has 'Latest TODO ID: T000' format: %e", e)
        return "T001"  # Default starting ID


def find_todos() -> list[dict[str, Any]]:
    todos = []
    # Scan all Python files in project
    for file_path in Path(".").rglob("*.py"):
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                # Match TODO comments with various formats
                todo_match = re.search(r"#\s*TODO\(([\w\-/]+)\):\s*(.+)", line)
                if todo_match:
                    author = todo_match.group(1)
                    description = todo_match.group(2).strip()
                    todos.append(
                        {
                            "file": str(file_path),
                            "line": line_num,
                            "author": author,
                            "description": description,
                            "date": datetime.now(tz=UTC).strftime("%Y-%m-%d"),
                        }
                    )
    return todos


def generate_todos_md(todos: list[dict[str, Any]]) -> str:
    content = """# Project TODOs

Latest TODO ID: T000

## Active TODOs\n\n"""

    for i, todo in enumerate(todos, 1):
        todo_id = f"T{str(i).zfill(3)}"
        content += f"""- [{todo_id}] {todo['description']}
  - File: {todo['file']}:{todo['line']}
  - Author: {todo['author']}
  - Added: {todo['date']}

"""

    content += "\n## Completed\n"
    Path("TODOS.md").write_text(content, encoding="utf-8")
    return content


if __name__ == "__main__":
    todos = find_todos()
    generate_todos_md(todos)
