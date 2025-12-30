# Todo-CLI Test Suite

Comprehensive pytest test suite for the todo-cli application.

## Test Structure

```
tests/
├── __init__.py         # Package marker
├── conftest.py         # Shared pytest fixtures
├── test_cli.py         # CLI command tests (180+ test cases)
├── test_utils.py       # Utility function tests (50+ test cases)
└── README.md           # This file
```

## Installation

Install test dependencies:

```bash
# From the todo_cli directory
pip install -e ".[dev]"
```

Or install manually:

```bash
pip install pytest pytest-cov click rich
```

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with coverage
```bash
pytest tests/ --cov=todo_cli --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_cli.py
pytest tests/test_utils.py
```

### Run specific test class
```bash
pytest tests/test_cli.py::TestAddCommand
pytest tests/test_utils.py::TestValidateDateFormat
```

### Run specific test
```bash
pytest tests/test_cli.py::TestAddCommand::test_add_basic_task
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run tests matching a pattern
```bash
pytest tests/ -k "add"           # All tests with "add" in name
pytest tests/ -k "priority"       # All tests with "priority" in name
```

## Test Coverage

### CLI Commands (test_cli.py)
- **TestCLIBasics**: Core CLI functionality (--help, --version, global flags)
- **TestAddCommand**: Add command with all options and edge cases
- **TestListCommand**: List command with filtering and sorting
- **TestCompleteCommand**: Complete command with validation
- **TestRemoveCommand**: Remove command with confirmation
- **TestClearCommand**: Clear command with confirmation
- **TestIntegrationScenarios**: End-to-end workflows

### Utility Functions (test_utils.py)
- **TestGetStoragePath**: Storage path resolution
- **TestLoadTodos**: Loading todos from storage
- **TestSaveTodos**: Saving todos to storage
- **TestGetNextId**: ID generation
- **TestFindTodoById**: Task lookup
- **TestValidateDateFormat**: Date validation
- **TestFormatDatetime**: Datetime formatting
- **TestSortTodos**: Task sorting by various fields
- **TestFilterTodos**: Task filtering by status
- **TestGetPriorityColor**: Priority color mapping

## Test Categories

### Happy Path Tests
- Valid inputs with expected outputs
- All command options work correctly
- Storage operations succeed

### Error Cases
- Invalid task IDs (non-existent, negative, malformed)
- Invalid date formats
- Invalid priority values
- Missing required arguments
- Corrupted storage files

### Edge Cases
- Empty task lists
- All tasks completed/pending
- Tasks without due dates
- Confirmation prompts (yes/no)
- Quiet and verbose modes
- No-color mode

### Integration Tests
- Complete workflows (add -> list -> complete -> clear)
- Multiple operations in sequence
- Storage persistence across commands

## Fixtures

### runner
Click's CliRunner for testing CLI commands

### temp_storage
Temporary storage file path for isolated tests

### sample_todos
Sample todo data with 3 tasks (2 pending, 1 completed)

### storage_with_todos
Pre-populated storage file with sample todos

### empty_storage
Empty storage file

### corrupted_storage
Corrupted JSON file for error testing

## Test Statistics

- **Total test files**: 2
- **Total test classes**: 21
- **Total test cases**: 230+
- **Commands tested**: 5 (add, list, complete, remove, clear)
- **Options tested**: 8 (--priority, --due, --filter, --sort, --force, --verbose, --quiet, --no-color)

## Code Coverage Goals

- **Utility functions**: 100% coverage
- **CLI commands**: 95%+ coverage
- **Error handling**: All error paths tested
- **Edge cases**: All edge cases covered

## Testing Best Practices

1. **Isolation**: Each test uses temp_storage to avoid conflicts
2. **Fixtures**: Reusable fixtures in conftest.py
3. **Descriptive names**: Test names clearly describe what they test
4. **Arrange-Act-Assert**: Tests follow AAA pattern
5. **Both positive and negative**: Test success and failure cases
6. **Mock storage**: Use temporary directories, never real user data

## Common Test Patterns

### Testing a CLI command
```python
def test_example(runner: CliRunner, temp_storage: Path):
    result = runner.invoke(cli, [
        "--config", str(temp_storage),
        "command", "args"
    ])
    assert result.exit_code == 0
    assert "expected output" in result.output
```

### Testing with confirmation
```python
def test_with_confirmation(runner: CliRunner, storage_with_todos: Path):
    result = runner.invoke(cli, [
        "--config", str(storage_with_todos),
        "remove", "1"
    ], input="y\n")  # Simulate user typing 'y'
    assert result.exit_code == 0
```

### Verifying storage
```python
def test_storage_update(runner: CliRunner, temp_storage: Path):
    runner.invoke(cli, ["--config", str(temp_storage), "add", "Task"])

    # Verify storage was updated
    with temp_storage.open("r") as f:
        todos = json.load(f)
    assert len(todos) == 1
    assert todos[0]["title"] == "Task"
```

## Troubleshooting

### Import errors
Make sure todo_cli is installed:
```bash
pip install -e .
```

### No tests collected
Check you're in the correct directory:
```bash
cd /path/to/todo_cli
pytest tests/
```

### Coverage not working
Install pytest-cov:
```bash
pip install pytest-cov
```

## Contributing

When adding new features:
1. Add tests for happy path
2. Add tests for error cases
3. Add tests for edge cases
4. Update this README if needed
5. Ensure coverage remains above 95%
