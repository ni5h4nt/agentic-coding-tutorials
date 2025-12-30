"""Tests for todo-cli utility functions."""

import json
from pathlib import Path
from typing import Any

import pytest
from click import ClickException

from todo_cli.utils import (
    filter_todos,
    find_todo_by_id,
    format_datetime,
    get_next_id,
    get_priority_color,
    get_storage_path,
    load_todos,
    save_todos,
    sort_todos,
    validate_date_format,
)


class TestGetStoragePath:
    """Tests for get_storage_path function."""

    def test_get_default_storage_path(self):
        """Test getting default storage path."""
        path = get_storage_path()
        assert path == Path.home() / ".todo-cli" / "todos.json"

    def test_get_custom_storage_path(self, temp_storage: Path):
        """Test getting custom storage path."""
        custom_path = temp_storage / "custom.json"
        path = get_storage_path(custom_path)
        assert path == custom_path

    def test_default_path_directory_creation(self):
        """Test that default path creates directory if needed."""
        path = get_storage_path()
        # Directory should exist after calling get_storage_path
        assert path.parent.exists()


class TestLoadTodos:
    """Tests for load_todos function."""

    def test_load_from_nonexistent_file(self, temp_storage: Path):
        """Test loading from a file that doesn't exist returns empty list."""
        todos = load_todos(temp_storage)
        assert todos == []

    def test_load_from_empty_file(self, empty_storage: Path):
        """Test loading from an empty storage file."""
        todos = load_todos(empty_storage)
        assert todos == []

    def test_load_existing_todos(self, storage_with_todos: Path):
        """Test loading existing todos from file."""
        todos = load_todos(storage_with_todos)
        assert len(todos) == 3
        assert todos[0]["title"] == "Buy groceries"
        assert todos[1]["title"] == "Write report"
        assert todos[2]["title"] == "Call dentist"

    def test_load_corrupted_file_raises_exception(self, corrupted_storage: Path):
        """Test that loading a corrupted file raises ClickException."""
        with pytest.raises(ClickException, match="Failed to load todos"):
            load_todos(corrupted_storage)


class TestSaveTodos:
    """Tests for save_todos function."""

    def test_save_to_new_file(self, temp_storage: Path, sample_todos: list[dict[str, Any]]):
        """Test saving todos to a new file."""
        save_todos(temp_storage, sample_todos)
        assert temp_storage.exists()

        # Verify content
        with temp_storage.open("r") as f:
            saved_data = json.load(f)
        assert saved_data == sample_todos

    def test_save_empty_list(self, temp_storage: Path):
        """Test saving an empty list of todos."""
        save_todos(temp_storage, [])
        assert temp_storage.exists()

        with temp_storage.open("r") as f:
            saved_data = json.load(f)
        assert saved_data == []

    def test_save_overwrites_existing_file(self, storage_with_todos: Path):
        """Test that saving overwrites existing file."""
        new_todos = [{"id": 99, "title": "New task", "completed": False}]
        save_todos(storage_with_todos, new_todos)

        with storage_with_todos.open("r") as f:
            saved_data = json.load(f)
        assert len(saved_data) == 1
        assert saved_data[0]["id"] == 99

    def test_save_creates_parent_directory(self, tmp_path: Path):
        """Test that save creates parent directory if needed."""
        nested_path = tmp_path / "nested" / "dir" / "todos.json"
        save_todos(nested_path, [])
        assert nested_path.exists()
        assert nested_path.parent.exists()


class TestGetNextId:
    """Tests for get_next_id function."""

    def test_next_id_for_empty_list(self):
        """Test that first ID is 1 for empty list."""
        next_id = get_next_id([])
        assert next_id == 1

    def test_next_id_increments(self, sample_todos: list[dict[str, Any]]):
        """Test that next ID is max ID + 1."""
        next_id = get_next_id(sample_todos)
        assert next_id == 4

    def test_next_id_with_single_todo(self):
        """Test next ID with a single todo."""
        todos = [{"id": 1, "title": "Task"}]
        next_id = get_next_id(todos)
        assert next_id == 2

    def test_next_id_with_gaps(self):
        """Test next ID when there are gaps in IDs."""
        todos = [{"id": 1}, {"id": 5}, {"id": 3}]
        next_id = get_next_id(todos)
        assert next_id == 6  # Should be max + 1


class TestFindTodoById:
    """Tests for find_todo_by_id function."""

    def test_find_existing_todo(self, sample_todos: list[dict[str, Any]]):
        """Test finding an existing todo by ID."""
        todo = find_todo_by_id(sample_todos, 2)
        assert todo is not None
        assert todo["title"] == "Write report"

    def test_find_nonexistent_todo(self, sample_todos: list[dict[str, Any]]):
        """Test finding a non-existent todo returns None."""
        todo = find_todo_by_id(sample_todos, 999)
        assert todo is None

    def test_find_in_empty_list(self):
        """Test finding in an empty list returns None."""
        todo = find_todo_by_id([], 1)
        assert todo is None

    def test_find_first_todo(self, sample_todos: list[dict[str, Any]]):
        """Test finding the first todo."""
        todo = find_todo_by_id(sample_todos, 1)
        assert todo is not None
        assert todo["title"] == "Buy groceries"

    def test_find_last_todo(self, sample_todos: list[dict[str, Any]]):
        """Test finding the last todo."""
        todo = find_todo_by_id(sample_todos, 3)
        assert todo is not None
        assert todo["title"] == "Call dentist"


class TestValidateDateFormat:
    """Tests for validate_date_format function."""

    def test_valid_date_formats(self):
        """Test various valid date formats."""
        assert validate_date_format("2025-12-30") is True
        assert validate_date_format("2025-01-01") is True
        assert validate_date_format("2024-02-29") is True  # Leap year

    def test_invalid_date_formats(self):
        """Test various invalid date formats."""
        assert validate_date_format("12-30-2025") is False  # Wrong format
        assert validate_date_format("2025/12/30") is False  # Wrong separator
        assert validate_date_format("2025-13-01") is False  # Invalid month
        assert validate_date_format("2025-12-32") is False  # Invalid day
        assert validate_date_format("2025-02-30") is False  # Invalid day for month
        assert validate_date_format("not-a-date") is False
        assert validate_date_format("") is False

    def test_edge_case_dates(self):
        """Test edge case dates."""
        assert validate_date_format("2023-02-29") is False  # Not a leap year
        assert validate_date_format("2024-02-29") is True   # Leap year
        assert validate_date_format("2025-12-31") is True   # Last day of year
        assert validate_date_format("2025-01-01") is True   # First day of year


class TestFormatDatetime:
    """Tests for format_datetime function."""

    def test_format_returns_iso_string(self):
        """Test that format_datetime returns ISO format string."""
        result = format_datetime()
        assert isinstance(result, str)
        # Check it contains basic ISO format elements
        assert "T" in result
        assert "-" in result
        assert ":" in result

    def test_format_is_parseable(self):
        """Test that formatted datetime can be parsed."""
        from datetime import datetime
        result = format_datetime()
        # Should not raise exception
        parsed = datetime.fromisoformat(result)
        assert isinstance(parsed, datetime)


class TestSortTodos:
    """Tests for sort_todos function."""

    def test_sort_by_created_date(self, sample_todos: list[dict[str, Any]]):
        """Test sorting todos by created date (newest first)."""
        sorted_todos = sort_todos(sample_todos, "created")
        assert sorted_todos[0]["id"] == 3  # Most recent
        assert sorted_todos[1]["id"] == 2
        assert sorted_todos[2]["id"] == 1  # Oldest

    def test_sort_by_due_date(self):
        """Test sorting todos by due date."""
        todos = [
            {"id": 1, "due_date": "2025-12-31"},
            {"id": 2, "due_date": None},
            {"id": 3, "due_date": "2025-12-25"},
        ]
        sorted_todos = sort_todos(todos, "due")
        # None should be at the end
        assert sorted_todos[0]["id"] == 3  # 2025-12-25
        assert sorted_todos[1]["id"] == 1  # 2025-12-31
        assert sorted_todos[2]["id"] == 2  # None

    def test_sort_by_priority(self):
        """Test sorting todos by priority (high to low)."""
        todos = [
            {"id": 1, "priority": "low"},
            {"id": 2, "priority": "high"},
            {"id": 3, "priority": "medium"},
        ]
        sorted_todos = sort_todos(todos, "priority")
        assert sorted_todos[0]["priority"] == "high"
        assert sorted_todos[1]["priority"] == "medium"
        assert sorted_todos[2]["priority"] == "low"

    def test_sort_empty_list(self):
        """Test sorting an empty list."""
        sorted_todos = sort_todos([], "created")
        assert sorted_todos == []

    def test_sort_with_invalid_field(self, sample_todos: list[dict[str, Any]]):
        """Test sorting with invalid field returns original list."""
        sorted_todos = sort_todos(sample_todos, "invalid")
        assert sorted_todos == sample_todos


class TestFilterTodos:
    """Tests for filter_todos function."""

    def test_filter_all(self, sample_todos: list[dict[str, Any]]):
        """Test filtering with 'all' returns all todos."""
        filtered = filter_todos(sample_todos, "all")
        assert len(filtered) == 3

    def test_filter_pending(self, sample_todos: list[dict[str, Any]]):
        """Test filtering pending todos."""
        filtered = filter_todos(sample_todos, "pending")
        assert len(filtered) == 2
        assert all(not todo["completed"] for todo in filtered)

    def test_filter_completed(self, sample_todos: list[dict[str, Any]]):
        """Test filtering completed todos."""
        filtered = filter_todos(sample_todos, "completed")
        assert len(filtered) == 1
        assert all(todo["completed"] for todo in filtered)

    def test_filter_empty_list(self):
        """Test filtering an empty list."""
        filtered = filter_todos([], "pending")
        assert filtered == []

    def test_filter_no_pending_tasks(self):
        """Test filtering when there are no pending tasks."""
        todos = [
            {"id": 1, "completed": True},
            {"id": 2, "completed": True}
        ]
        filtered = filter_todos(todos, "pending")
        assert filtered == []

    def test_filter_no_completed_tasks(self):
        """Test filtering when there are no completed tasks."""
        todos = [
            {"id": 1, "completed": False},
            {"id": 2, "completed": False}
        ]
        filtered = filter_todos(todos, "completed")
        assert filtered == []


class TestGetPriorityColor:
    """Tests for get_priority_color function."""

    def test_high_priority_color(self):
        """Test color for high priority."""
        color = get_priority_color("high")
        assert color == "red"

    def test_medium_priority_color(self):
        """Test color for medium priority."""
        color = get_priority_color("medium")
        assert color == "yellow"

    def test_low_priority_color(self):
        """Test color for low priority."""
        color = get_priority_color("low")
        assert color == "green"

    def test_invalid_priority_returns_default(self):
        """Test that invalid priority returns default color."""
        color = get_priority_color("invalid")
        assert color == "white"

    def test_case_sensitivity(self):
        """Test priority colors with different cases."""
        # Function should handle lowercase (as per implementation)
        assert get_priority_color("high") == "red"
        assert get_priority_color("HIGH") == "white"  # Not in dict, returns default
