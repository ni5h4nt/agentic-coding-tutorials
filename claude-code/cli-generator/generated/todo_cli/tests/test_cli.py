"""Tests for todo-cli commands."""

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from todo_cli.cli import cli


class TestCLIBasics:
    """Tests for basic CLI functionality."""

    def test_cli_help(self, runner: CliRunner):
        """Test that --help flag works."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "todo-cli" in result.output
        assert "A simple command-line task manager" in result.output
        assert "Commands:" in result.output

    def test_cli_version(self, runner: CliRunner):
        """Test that --version flag works."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_cli_no_command(self, runner: CliRunner):
        """Test running CLI without a command shows help."""
        result = runner.invoke(cli, [])
        # Click returns exit code 0 or 2 depending on version when no command given
        assert result.exit_code in (0, 2)

    def test_cli_invalid_command(self, runner: CliRunner):
        """Test running CLI with invalid command."""
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "Error" in result.output or "No such command" in result.output

    def test_global_verbose_flag(self, runner: CliRunner, temp_storage: Path):
        """Test global --verbose flag."""
        result = runner.invoke(cli, ["--verbose", "--config", str(temp_storage), "list"])
        assert result.exit_code == 0

    def test_global_quiet_flag(self, runner: CliRunner, temp_storage: Path):
        """Test global --quiet flag."""
        result = runner.invoke(cli, ["--quiet", "--config", str(temp_storage), "list"])
        assert result.exit_code == 0
        # Output should be minimal or empty
        assert len(result.output) < 100

    def test_global_no_color_flag(self, runner: CliRunner, temp_storage: Path):
        """Test global --no-color flag."""
        result = runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "list"])
        assert result.exit_code == 0


class TestAddCommand:
    """Tests for the 'add' command."""

    def test_add_basic_task(self, runner: CliRunner, temp_storage: Path):
        """Test adding a basic task."""
        result = runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Buy groceries"])
        assert result.exit_code == 0
        assert "Added task #1" in result.output
        assert "Buy groceries" in result.output

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 1
        assert todos[0]["title"] == "Buy groceries"
        assert todos[0]["priority"] == "medium"  # Default priority

    def test_add_task_with_priority(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with priority."""
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "add", "Urgent task",
            "--priority", "high"
        ])
        assert result.exit_code == 0
        assert "high" in result.output

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert todos[0]["priority"] == "high"

    def test_add_task_with_due_date(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with due date."""
        result = runner.invoke(cli, [
            "--no-color", "--config", str(temp_storage),
            "add", "Submit report",
            "--due", "2025-12-31"
        ])
        assert result.exit_code == 0
        assert "2025-12-31" in result.output

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert todos[0]["due_date"] == "2025-12-31"

    def test_add_task_with_all_options(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with all options."""
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "add", "Complete project",
            "--priority", "high",
            "--due", "2025-12-25"
        ])
        assert result.exit_code == 0

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 1
        assert todos[0]["title"] == "Complete project"
        assert todos[0]["priority"] == "high"
        assert todos[0]["due_date"] == "2025-12-25"
        assert todos[0]["completed"] is False

    def test_add_task_invalid_date_format(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with invalid date format."""
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "add", "Task",
            "--due", "12-31-2025"  # Wrong format
        ])
        assert result.exit_code != 0
        assert "Invalid date format" in result.output

    def test_add_task_invalid_priority(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with invalid priority."""
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "add", "Task",
            "--priority", "urgent"  # Not a valid choice
        ])
        assert result.exit_code != 0
        assert "Invalid value" in result.output or "invalid choice" in result.output.lower()

    def test_add_multiple_tasks(self, runner: CliRunner, temp_storage: Path):
        """Test adding multiple tasks."""
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Task 1"])
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Task 2"])
        result = runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Task 3"])

        assert result.exit_code == 0
        assert "Added task #3" in result.output

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 3

    def test_add_task_with_quiet_flag(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task with --quiet flag."""
        result = runner.invoke(cli, [
            "--quiet", "--config", str(temp_storage),
            "add", "Silent task"
        ])
        assert result.exit_code == 0
        # Output should be minimal
        assert result.output == "" or len(result.output) < 10

    def test_add_task_with_short_flags(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task using short flags."""
        result = runner.invoke(cli, [
            "-c", str(temp_storage),
            "add", "Task",
            "-p", "low",
            "-d", "2025-12-30"
        ])
        assert result.exit_code == 0

        # Verify storage
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert todos[0]["priority"] == "low"
        assert todos[0]["due_date"] == "2025-12-30"

    def test_add_task_missing_title(self, runner: CliRunner, temp_storage: Path):
        """Test adding a task without title."""
        result = runner.invoke(cli, ["--config", str(temp_storage), "add"])
        assert result.exit_code != 0


class TestListCommand:
    """Tests for the 'list' command."""

    def test_list_empty_todos(self, runner: CliRunner, empty_storage: Path):
        """Test listing when there are no todos."""
        result = runner.invoke(cli, ["--config", str(empty_storage), "list"])
        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_list_all_todos(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing all todos."""
        result = runner.invoke(cli, ["--config", str(storage_with_todos), "list"])
        assert result.exit_code == 0
        assert "Buy groceries" in result.output
        assert "Write report" in result.output
        assert "Call dentist" in result.output

    def test_list_pending_todos(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing only pending todos."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "list", "--filter", "pending"
        ])
        assert result.exit_code == 0
        assert "Buy groceries" in result.output
        assert "Write report" in result.output
        assert "Call dentist" not in result.output  # Completed task

    def test_list_completed_todos(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing only completed todos."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "list", "--filter", "completed"
        ])
        assert result.exit_code == 0
        assert "Call dentist" in result.output
        assert "Buy groceries" not in result.output  # Pending task

    def test_list_sort_by_created(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing sorted by created date."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "list", "--sort", "created"
        ])
        assert result.exit_code == 0
        # Should show newest first (Call dentist is newest)
        dentist_pos = result.output.find("Call dentist")
        groceries_pos = result.output.find("Buy groceries")
        assert dentist_pos < groceries_pos

    def test_list_sort_by_priority(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing sorted by priority."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "list", "--sort", "priority"
        ])
        assert result.exit_code == 0
        # Should show high priority first
        groceries_pos = result.output.find("Buy groceries")  # high
        report_pos = result.output.find("Write report")      # medium
        assert groceries_pos < report_pos

    def test_list_sort_by_due(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing sorted by due date."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "list", "--sort", "due"
        ])
        assert result.exit_code == 0
        # Should show earlier due dates first

    def test_list_with_verbose_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing with --verbose flag."""
        result = runner.invoke(cli, [
            "--verbose", "--config", str(storage_with_todos),
            "list"
        ])
        assert result.exit_code == 0
        assert "Total:" in result.output  # Verbose shows total count

    def test_list_with_quiet_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing with --quiet flag doesn't suppress list output."""
        result = runner.invoke(cli, [
            "--quiet", "--config", str(storage_with_todos),
            "list"
        ])
        assert result.exit_code == 0
        # List should still show (quiet only suppresses certain messages)

    def test_list_short_flags(self, runner: CliRunner, storage_with_todos: Path):
        """Test listing using short flags."""
        result = runner.invoke(cli, [
            "-c", str(storage_with_todos),
            "list", "-f", "pending", "-s", "priority"
        ])
        assert result.exit_code == 0

    def test_list_no_matches_for_filter(self, runner: CliRunner, temp_storage: Path):
        """Test listing when filter matches no todos."""
        # Add only pending tasks
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Task 1"])

        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "list", "--filter", "completed"
        ])
        assert result.exit_code == 0
        assert "No completed tasks found" in result.output


class TestCompleteCommand:
    """Tests for the 'complete' command."""

    def test_complete_existing_task(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing an existing task."""
        result = runner.invoke(cli, ["--no-color", "--config", str(storage_with_todos), "complete", "1"])
        assert result.exit_code == 0
        assert "Completed task #1" in result.output

        # Verify storage
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        task = next(t for t in todos if t["id"] == 1)
        assert task["completed"] is True
        assert task["completed_at"] is not None

    def test_complete_already_completed_task(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing an already completed task."""
        result = runner.invoke(cli, ["--config", str(storage_with_todos), "complete", "3"])
        assert result.exit_code == 0
        assert "already completed" in result.output

    def test_complete_nonexistent_task(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing a non-existent task."""
        result = runner.invoke(cli, ["--config", str(storage_with_todos), "complete", "999"])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_complete_with_quiet_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing with --quiet flag."""
        result = runner.invoke(cli, [
            "--quiet", "--config", str(storage_with_todos),
            "complete", "1"
        ])
        assert result.exit_code == 0
        assert result.output == "" or len(result.output) < 10

    def test_complete_invalid_id_format(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing with invalid ID format."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "complete", "not-a-number"
        ])
        assert result.exit_code != 0

    def test_complete_negative_id(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing with negative ID."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "complete", "-1"
        ])
        assert result.exit_code != 0

    def test_complete_missing_id(self, runner: CliRunner, storage_with_todos: Path):
        """Test completing without providing ID."""
        result = runner.invoke(cli, ["--config", str(storage_with_todos), "complete"])
        assert result.exit_code != 0


class TestRemoveCommand:
    """Tests for the 'remove' command."""

    def test_remove_task_with_force(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing a task with --force flag."""
        result = runner.invoke(cli, [
            "--no-color", "--config", str(storage_with_todos),
            "remove", "1", "--force"
        ])
        assert result.exit_code == 0
        assert "Removed task #1" in result.output

        # Verify storage
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 2
        assert not any(t["id"] == 1 for t in todos)

    def test_remove_task_with_confirmation_yes(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing a task with confirmation (yes)."""
        result = runner.invoke(cli, [
            "--no-color", "--config", str(storage_with_todos),
            "remove", "1"
        ], input="y\n")
        assert result.exit_code == 0
        assert "Removed task #1" in result.output

        # Verify storage
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 2

    def test_remove_task_with_confirmation_no(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing a task with confirmation (no)."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "remove", "1"
        ], input="n\n")
        assert result.exit_code == 0
        assert "Cancelled" in result.output

        # Verify storage - task should still exist
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 3
        assert any(t["id"] == 1 for t in todos)

    def test_remove_nonexistent_task(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing a non-existent task."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "remove", "999", "--force"
        ])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_remove_with_short_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing using short -f flag."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "remove", "2", "-f"
        ])
        assert result.exit_code == 0

    def test_remove_missing_id(self, runner: CliRunner, storage_with_todos: Path):
        """Test removing without providing ID."""
        result = runner.invoke(cli, ["--config", str(storage_with_todos), "remove"])
        assert result.exit_code != 0


class TestClearCommand:
    """Tests for the 'clear' command."""

    def test_clear_with_force(self, runner: CliRunner, storage_with_todos: Path):
        """Test clearing completed tasks with --force flag."""
        result = runner.invoke(cli, [
            "--no-color", "--config", str(storage_with_todos),
            "clear", "--force"
        ])
        assert result.exit_code == 0
        assert "Removed 1 completed task(s)" in result.output

        # Verify storage - only pending tasks remain
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 2
        assert all(not t["completed"] for t in todos)

    def test_clear_with_confirmation_yes(self, runner: CliRunner, storage_with_todos: Path):
        """Test clearing with confirmation (yes)."""
        result = runner.invoke(cli, [
            "--no-color", "--config", str(storage_with_todos),
            "clear"
        ], input="y\n")
        assert result.exit_code == 0
        assert "Removed 1 completed task(s)" in result.output

    def test_clear_with_confirmation_no(self, runner: CliRunner, storage_with_todos: Path):
        """Test clearing with confirmation (no)."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "clear"
        ], input="n\n")
        assert result.exit_code == 0
        assert "Cancelled" in result.output

        # Verify storage - all tasks should still exist
        with storage_with_todos.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 3

    def test_clear_no_completed_tasks(self, runner: CliRunner, temp_storage: Path):
        """Test clearing when there are no completed tasks."""
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Task 1"])

        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "clear", "--force"
        ])
        assert result.exit_code == 0
        assert "No completed tasks to clear" in result.output

    def test_clear_all_tasks_completed(self, runner: CliRunner, temp_storage: Path):
        """Test clearing when all tasks are completed."""
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Task 1"])
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "add", "Task 2"])
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "complete", "1"])
        runner.invoke(cli, ["--no-color", "--config", str(temp_storage), "complete", "2"])

        result = runner.invoke(cli, [
            "--no-color", "--config", str(temp_storage),
            "clear", "--force"
        ])
        assert result.exit_code == 0
        assert "Removed 2 completed task(s)" in result.output

        # Verify storage is empty
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 0

    def test_clear_with_quiet_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test clearing with --quiet flag."""
        result = runner.invoke(cli, [
            "--quiet", "--config", str(storage_with_todos),
            "clear", "--force"
        ])
        assert result.exit_code == 0

    def test_clear_with_short_flag(self, runner: CliRunner, storage_with_todos: Path):
        """Test clearing using short -f flag."""
        result = runner.invoke(cli, [
            "--config", str(storage_with_todos),
            "clear", "-f"
        ])
        assert result.exit_code == 0


class TestIntegrationScenarios:
    """Integration tests for common workflows."""

    def test_complete_workflow(self, runner: CliRunner, temp_storage: Path):
        """Test a complete workflow: add, list, complete, clear."""
        # Add tasks
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Task 1", "-p", "high"])
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Task 2", "-p", "low"])
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Task 3"])

        # List all
        result = runner.invoke(cli, ["--config", str(temp_storage), "list"])
        assert "Task 1" in result.output
        assert "Task 2" in result.output
        assert "Task 3" in result.output

        # Complete one task
        runner.invoke(cli, ["--config", str(temp_storage), "complete", "1"])

        # List pending
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "list", "--filter", "pending"
        ])
        assert "Task 1" not in result.output
        assert "Task 2" in result.output

        # Clear completed
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "clear", "--force"
        ])
        assert result.exit_code == 0

        # Verify final state
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 2
        assert all(not t["completed"] for t in todos)

    def test_add_complete_remove_workflow(self, runner: CliRunner, temp_storage: Path):
        """Test add, complete, and remove workflow."""
        # Add task
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Important task"])

        # Complete it
        runner.invoke(cli, ["--config", str(temp_storage), "complete", "1"])

        # Remove it
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "remove", "1", "--force"
        ])
        assert result.exit_code == 0

        # Verify empty
        with temp_storage.open("r") as f:
            todos = json.load(f)
        assert len(todos) == 0

    def test_multiple_priorities_and_sorting(self, runner: CliRunner, temp_storage: Path):
        """Test adding tasks with different priorities and sorting."""
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Low task", "-p", "low"])
        runner.invoke(cli, ["--config", str(temp_storage), "add", "High task", "-p", "high"])
        runner.invoke(cli, ["--config", str(temp_storage), "add", "Med task", "-p", "medium"])

        # Sort by priority
        result = runner.invoke(cli, [
            "--config", str(temp_storage),
            "list", "--sort", "priority"
        ])
        assert result.exit_code == 0

        # Verify order: high should come before medium, medium before low
        high_pos = result.output.find("High task")
        med_pos = result.output.find("Med task")
        low_pos = result.output.find("Low task")
        assert high_pos < med_pos < low_pos

    def test_corrupted_storage_handling(self, runner: CliRunner, corrupted_storage: Path):
        """Test handling of corrupted storage file."""
        result = runner.invoke(cli, ["--config", str(corrupted_storage), "list"])
        assert result.exit_code != 0
        assert "Failed to load todos" in result.output
