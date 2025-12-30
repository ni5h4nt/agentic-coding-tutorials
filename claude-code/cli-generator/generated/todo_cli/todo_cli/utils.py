"""Utility functions for todo-cli storage and helpers."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import click


def get_storage_path(config_path: Path | None = None) -> Path:
    """Get the path to the todos storage file.

    Args:
        config_path: Optional custom config path

    Returns:
        Path to the todos.json file
    """
    if config_path:
        return config_path

    storage_dir = Path.home() / ".todo-cli"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir / "todos.json"


def load_todos(storage_path: Path) -> list[dict[str, Any]]:
    """Load todos from storage file.

    Args:
        storage_path: Path to the storage file

    Returns:
        List of todo dictionaries
    """
    if not storage_path.exists():
        return []

    try:
        with storage_path.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise click.ClickException(f"Failed to load todos: {e}")


def save_todos(storage_path: Path, todos: list[dict[str, Any]]) -> None:
    """Save todos to storage file.

    Args:
        storage_path: Path to the storage file
        todos: List of todo dictionaries to save
    """
    try:
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        with storage_path.open("w") as f:
            json.dump(todos, f, indent=2)
    except (IOError, TypeError) as e:
        raise click.ClickException(f"Failed to save todos: {e}")


def get_next_id(todos: list[dict[str, Any]]) -> int:
    """Get the next available task ID.

    Args:
        todos: List of existing todos

    Returns:
        Next available ID
    """
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1


def find_todo_by_id(todos: list[dict[str, Any]], task_id: int) -> dict[str, Any] | None:
    """Find a todo by its ID.

    Args:
        todos: List of todos
        task_id: ID to search for

    Returns:
        Todo dictionary or None if not found
    """
    for todo in todos:
        if todo["id"] == task_id:
            return todo
    return None


def validate_date_format(date_str: str) -> bool:
    """Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_datetime() -> str:
    """Get current datetime as ISO format string.

    Returns:
        Current datetime in ISO format
    """
    return datetime.now().isoformat()


def sort_todos(
    todos: list[dict[str, Any]],
    sort_by: str
) -> list[dict[str, Any]]:
    """Sort todos by the specified field.

    Args:
        todos: List of todos to sort
        sort_by: Field to sort by (created/due/priority)

    Returns:
        Sorted list of todos
    """
    if sort_by == "created":
        return sorted(todos, key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "due":
        # Sort by due date, putting None at the end
        return sorted(
            todos,
            key=lambda x: (x["due_date"] is None, x["due_date"] or "")
        )
    elif sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(todos, key=lambda x: priority_order.get(x["priority"], 3))

    return todos


def filter_todos(
    todos: list[dict[str, Any]],
    filter_by: str
) -> list[dict[str, Any]]:
    """Filter todos by status.

    Args:
        todos: List of todos to filter
        filter_by: Filter type (all/pending/completed)

    Returns:
        Filtered list of todos
    """
    if filter_by == "pending":
        return [t for t in todos if not t["completed"]]
    elif filter_by == "completed":
        return [t for t in todos if t["completed"]]

    return todos


def get_priority_color(priority: str) -> str:
    """Get the color for a priority level.

    Args:
        priority: Priority level (low/medium/high)

    Returns:
        Color name for rich formatting
    """
    colors = {
        "high": "red",
        "medium": "yellow",
        "low": "green"
    }
    return colors.get(priority, "white")
