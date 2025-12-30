"""Shared pytest fixtures for todo-cli tests."""

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    """Provide a Click CliRunner for testing CLI commands.

    Note: Use --no-color flag in tests that check output content
    to avoid ANSI escape codes in assertions.
    """
    return CliRunner()


@pytest.fixture
def temp_storage(tmp_path: Path) -> Path:
    """Provide a temporary storage file path for testing.

    Args:
        tmp_path: pytest's temporary directory fixture

    Returns:
        Path to a temporary todos.json file
    """
    storage_path = tmp_path / "todos.json"
    return storage_path


@pytest.fixture
def sample_todos() -> list[dict[str, Any]]:
    """Provide sample todo data for testing.

    Returns:
        List of sample todo dictionaries
    """
    return [
        {
            "id": 1,
            "title": "Buy groceries",
            "priority": "high",
            "due_date": "2025-12-30",
            "created_at": "2025-12-29T10:00:00",
            "completed": False,
            "completed_at": None
        },
        {
            "id": 2,
            "title": "Write report",
            "priority": "medium",
            "due_date": "2025-12-31",
            "created_at": "2025-12-29T11:00:00",
            "completed": False,
            "completed_at": None
        },
        {
            "id": 3,
            "title": "Call dentist",
            "priority": "low",
            "due_date": None,
            "created_at": "2025-12-29T12:00:00",
            "completed": True,
            "completed_at": "2025-12-29T15:00:00"
        }
    ]


@pytest.fixture
def storage_with_todos(temp_storage: Path, sample_todos: list[dict[str, Any]]) -> Path:
    """Provide a storage file pre-populated with sample todos.

    Args:
        temp_storage: Temporary storage path
        sample_todos: Sample todo data

    Returns:
        Path to storage file with sample data
    """
    temp_storage.parent.mkdir(parents=True, exist_ok=True)
    with temp_storage.open("w") as f:
        json.dump(sample_todos, f, indent=2)
    return temp_storage


@pytest.fixture
def empty_storage(temp_storage: Path) -> Path:
    """Provide an empty storage file for testing.

    Args:
        temp_storage: Temporary storage path

    Returns:
        Path to empty storage file
    """
    temp_storage.parent.mkdir(parents=True, exist_ok=True)
    with temp_storage.open("w") as f:
        json.dump([], f)
    return temp_storage


@pytest.fixture
def corrupted_storage(temp_storage: Path) -> Path:
    """Provide a corrupted storage file for error testing.

    Args:
        temp_storage: Temporary storage path

    Returns:
        Path to corrupted storage file
    """
    temp_storage.parent.mkdir(parents=True, exist_ok=True)
    with temp_storage.open("w") as f:
        f.write("{ invalid json content }")
    return temp_storage
