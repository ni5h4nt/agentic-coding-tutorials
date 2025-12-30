# todo-cli

A simple command-line task manager for tracking todos with priorities and due dates.

## Installation

```bash
pip install -e .
```

## Usage

### Add a new task

```bash
# Basic task
todo-cli add "Buy groceries"

# Task with high priority
todo-cli add "Submit report" --priority high

# Task with due date
todo-cli add "Doctor appointment" --due 2025-12-30

# Task with both priority and due date
todo-cli add "Project deadline" --priority high --due 2025-12-31
```

### List tasks

```bash
# List all tasks
todo-cli list

# List only pending tasks
todo-cli list --filter pending

# List completed tasks
todo-cli list --filter completed

# Sort by priority
todo-cli list --sort priority

# Sort by due date
todo-cli list --sort due

# Combine filtering and sorting
todo-cli list --filter pending --sort priority
```

### Complete a task

```bash
todo-cli complete 1
```

### Remove a task

```bash
# Remove with confirmation prompt
todo-cli remove 1

# Remove without confirmation
todo-cli remove 1 --force
```

### Clear completed tasks

```bash
# Clear with confirmation prompt
todo-cli clear

# Clear without confirmation
todo-cli clear --force
```

### Global Options

All commands support these global options:

- `--verbose` / `-v`: Enable verbose output for debugging
- `--quiet` / `-q`: Suppress all non-essential output
- `--no-color`: Disable colored output
- `--config` / `-c`: Use a custom JSON storage file
- `--version`: Show version information
- `--help`: Show help message

### Examples

```bash
# Use custom storage location
todo-cli --config ~/my-todos.json add "Custom task"

# Quiet mode (no output except errors)
todo-cli --quiet add "Silent task"

# Verbose mode (extra debug information)
todo-cli --verbose list

# Disable colors (useful for scripts)
todo-cli --no-color list
```

## Data Storage

By default, tasks are stored in `~/.todo-cli/todos.json`. You can specify a custom location using the `--config` option.

## Task Data Model

Each task is stored with the following fields:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "priority": "medium",
  "due_date": "2025-12-30",
  "created_at": "2025-12-29T10:30:00.000000",
  "completed": false,
  "completed_at": null
}
```

## Requirements

- Python 3.11+
- click >= 8.1.0
- rich >= 13.0.0

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
```

Type checking:

```bash
mypy todo_cli
```

Linting:

```bash
ruff check .
```

## License

MIT
