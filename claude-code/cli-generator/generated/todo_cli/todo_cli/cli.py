"""todo-cli: A simple command-line task manager for tracking todos with priorities and due dates."""

from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .utils import (
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


# Global state for options
class GlobalState:
    """Global state container for CLI options."""

    def __init__(self) -> None:
        self.verbose: bool = False
        self.quiet: bool = False
        self.no_color: bool = False
        self.config: Path | None = None
        self.console: Console | None = None


pass_state = click.make_pass_decorator(GlobalState, ensure=True)


@click.group()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output for debugging"
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all non-essential output"
)
@click.option(
    "--no-color",
    is_flag=True,
    help="Disable colored output"
)
@click.option(
    "--config",
    "-c",
    type=click.Path(path_type=Path),
    help="Path to custom JSON storage file"
)
@click.version_option(version=__version__)
@click.pass_context
def cli(
    ctx: click.Context,
    verbose: bool,
    quiet: bool,
    no_color: bool,
    config: Path | None
) -> None:
    """todo-cli: A simple command-line task manager for tracking todos with priorities and due dates.

    Store and manage your tasks with priorities, due dates, and completion tracking.
    All data is stored locally in JSON format.

    Examples:

        # Add a task
        $ todo-cli add "Buy groceries" --priority high --due 2025-12-30

        # List pending tasks
        $ todo-cli list --filter pending --sort priority

        # Complete a task
        $ todo-cli complete 1

        # Remove all completed tasks
        $ todo-cli clear --force
    """
    state = ctx.ensure_object(GlobalState)
    state.verbose = verbose
    state.quiet = quiet
    state.no_color = no_color
    state.config = config
    state.console = Console(force_terminal=not no_color, no_color=no_color)


@cli.command()
@click.argument("title", type=str, required=True)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    default="medium",
    help="Task priority level"
)
@click.option(
    "--due",
    "-d",
    type=str,
    help="Due date in YYYY-MM-DD format"
)
@pass_state
def add(state: GlobalState, title: str, priority: str, due: str | None) -> None:
    """Add a new task to your todo list.

    TITLE: The task description

    Examples:

        $ todo-cli add "Finish report"
        $ todo-cli add "Call dentist" --priority high --due 2025-12-30
    """
    # Validate due date format if provided
    if due and not validate_date_format(due):
        raise click.ClickException(
            f"Invalid date format: {due}. Use YYYY-MM-DD format (e.g., 2025-12-30)"
        )

    storage_path = get_storage_path(state.config)
    todos = load_todos(storage_path)

    # Create new todo
    new_todo: dict[str, Any] = {
        "id": get_next_id(todos),
        "title": title,
        "priority": priority.lower(),
        "due_date": due,
        "created_at": format_datetime(),
        "completed": False,
        "completed_at": None
    }

    todos.append(new_todo)
    save_todos(storage_path, todos)

    if not state.quiet:
        console = state.console or Console()
        priority_color = get_priority_color(new_todo["priority"])
        console.print(
            f"[green]✓[/green] Added task #{new_todo['id']}: "
            f"[bold]{title}[/bold] "
            f"[{priority_color}]({priority})[/{priority_color}]"
        )
        if due:
            console.print(f"  Due: {due}")


@cli.command()
@click.option(
    "--filter",
    "-f",
    "filter_by",
    type=click.Choice(["all", "pending", "completed"], case_sensitive=False),
    default="all",
    help="Filter tasks by status"
)
@click.option(
    "--sort",
    "-s",
    "sort_by",
    type=click.Choice(["created", "due", "priority"], case_sensitive=False),
    default="created",
    help="Sort tasks by field"
)
@pass_state
def list(state: GlobalState, filter_by: str, sort_by: str) -> None:
    """Display tasks with filtering and sorting options.

    Examples:

        $ todo-cli list
        $ todo-cli list --filter pending --sort priority
        $ todo-cli list --filter completed --sort due
    """
    storage_path = get_storage_path(state.config)
    todos = load_todos(storage_path)

    if not todos:
        if not state.quiet:
            console = state.console or Console()
            console.print("[yellow]No tasks found. Add some tasks to get started![/yellow]")
        return

    # Apply filtering and sorting
    filtered_todos = filter_todos(todos, filter_by.lower())
    sorted_todos = sort_todos(filtered_todos, sort_by.lower())

    if not sorted_todos:
        if not state.quiet:
            console = state.console or Console()
            console.print(f"[yellow]No {filter_by} tasks found.[/yellow]")
        return

    # Create table
    console = state.console or Console()
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Priority", width=10)
    table.add_column("Due Date", width=12)
    table.add_column("Status", width=12)

    for todo in sorted_todos:
        priority_color = get_priority_color(todo["priority"])
        status = "[green]✓ Done[/green]" if todo["completed"] else "[yellow]Pending[/yellow]"

        table.add_row(
            str(todo["id"]),
            todo["title"],
            f"[{priority_color}]{todo['priority']}[/{priority_color}]",
            todo["due_date"] or "-",
            status
        )

    console.print(table)

    if state.verbose:
        console.print(f"\n[dim]Total: {len(sorted_todos)} tasks[/dim]")


@cli.command()
@click.argument("task_id", type=int, required=True)
@pass_state
def complete(state: GlobalState, task_id: int) -> None:
    """Mark a task as completed.

    TASK_ID: The ID of the task to complete

    Examples:

        $ todo-cli complete 1
        $ todo-cli complete 5
    """
    storage_path = get_storage_path(state.config)
    todos = load_todos(storage_path)

    todo = find_todo_by_id(todos, task_id)
    if not todo:
        raise click.ClickException(f"Task #{task_id} not found")

    if todo["completed"]:
        if not state.quiet:
            console = state.console or Console()
            console.print(f"[yellow]Task #{task_id} is already completed[/yellow]")
        return

    # Mark as completed
    todo["completed"] = True
    todo["completed_at"] = format_datetime()

    save_todos(storage_path, todos)

    if not state.quiet:
        console = state.console or Console()
        console.print(f"[green]✓[/green] Completed task #{task_id}: [bold]{todo['title']}[/bold]")


@cli.command()
@click.argument("task_id", type=int, required=True)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Skip confirmation prompt"
)
@pass_state
def remove(state: GlobalState, task_id: int, force: bool) -> None:
    """Delete a task from your todo list.

    TASK_ID: The ID of the task to remove

    Examples:

        $ todo-cli remove 1
        $ todo-cli remove 5 --force
    """
    storage_path = get_storage_path(state.config)
    todos = load_todos(storage_path)

    todo = find_todo_by_id(todos, task_id)
    if not todo:
        raise click.ClickException(f"Task #{task_id} not found")

    # Confirm deletion unless forced
    if not force:
        console = state.console or Console()
        console.print(f"About to delete: [bold]{todo['title']}[/bold]")
        if not click.confirm("Are you sure?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Remove the todo
    todos = [t for t in todos if t["id"] != task_id]
    save_todos(storage_path, todos)

    if not state.quiet:
        console = state.console or Console()
        console.print(f"[red]✓[/red] Removed task #{task_id}")


@cli.command()
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Skip confirmation prompt"
)
@pass_state
def clear(state: GlobalState, force: bool) -> None:
    """Remove all completed tasks from your todo list.

    Examples:

        $ todo-cli clear
        $ todo-cli clear --force
    """
    storage_path = get_storage_path(state.config)
    todos = load_todos(storage_path)

    completed_todos = [t for t in todos if t["completed"]]

    if not completed_todos:
        if not state.quiet:
            console = state.console or Console()
            console.print("[yellow]No completed tasks to clear[/yellow]")
        return

    # Confirm deletion unless forced
    if not force:
        console = state.console or Console()
        console.print(f"About to delete {len(completed_todos)} completed task(s)")
        if not click.confirm("Are you sure?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Keep only pending tasks
    remaining_todos = [t for t in todos if not t["completed"]]
    save_todos(storage_path, remaining_todos)

    if not state.quiet:
        console = state.console or Console()
        console.print(f"[green]✓[/green] Removed {len(completed_todos)} completed task(s)")


if __name__ == "__main__":
    cli()
