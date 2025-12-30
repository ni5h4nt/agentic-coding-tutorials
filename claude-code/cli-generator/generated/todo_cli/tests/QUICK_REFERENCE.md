# Todo-CLI Test Quick Reference

## Installation
```bash
cd /home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli
pip install -e ".[dev]"
```

## Common Commands

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=todo_cli --cov-report=term-missing
pytest tests/ --cov=todo_cli --cov-report=html  # HTML report
```

### Run Specific Test File
```bash
pytest tests/test_cli.py      # CLI tests only
pytest tests/test_utils.py    # Utility tests only
```

### Run Specific Test Class
```bash
pytest tests/test_cli.py::TestAddCommand
pytest tests/test_cli.py::TestListCommand
pytest tests/test_utils.py::TestValidateDateFormat
```

### Run Specific Test
```bash
pytest tests/test_cli.py::TestAddCommand::test_add_basic_task
```

### Run Tests by Pattern
```bash
pytest tests/ -k "add"          # All tests with "add" in name
pytest tests/ -k "priority"      # All tests with "priority" in name
pytest tests/ -k "error"         # All error tests
pytest tests/ -k "complete"      # All complete-related tests
```

### Verbose Output
```bash
pytest tests/ -v               # Verbose
pytest tests/ -vv              # Very verbose
pytest tests/ -vv -s           # Show print statements
```

### Stop on First Failure
```bash
pytest tests/ -x               # Stop on first failure
pytest tests/ --maxfail=3      # Stop after 3 failures
```

### Run Failed Tests Only
```bash
pytest tests/ --lf             # Last failed
pytest tests/ --ff             # Failed first, then others
```

## Test Organization

### test_cli.py (52 tests)
- TestCLIBasics (7) - --help, --version, global flags
- TestAddCommand (12) - Add command tests
- TestListCommand (11) - List command tests
- TestCompleteCommand (7) - Complete command tests
- TestRemoveCommand (6) - Remove command tests
- TestClearCommand (7) - Clear command tests
- TestIntegrationScenarios (4) - End-to-end tests

### test_utils.py (41 tests)
- TestGetStoragePath (3) - Storage path tests
- TestLoadTodos (4) - Load operation tests
- TestSaveTodos (4) - Save operation tests
- TestGetNextId (4) - ID generation tests
- TestFindTodoById (5) - Task lookup tests
- TestValidateDateFormat (3) - Date validation tests
- TestFormatDatetime (2) - Datetime formatting tests
- TestSortTodos (5) - Sorting tests
- TestFilterTodos (6) - Filtering tests
- TestGetPriorityColor (5) - Color mapping tests

## Debugging Tests

### Show Test Output
```bash
pytest tests/ -s              # Show print() statements
pytest tests/ --capture=no    # Don't capture output
```

### Show Local Variables on Failure
```bash
pytest tests/ -l              # Show locals
pytest tests/ --tb=long       # Long traceback
pytest tests/ --tb=short      # Short traceback
```

### Run with PDB Debugger
```bash
pytest tests/ --pdb           # Drop into pdb on failure
pytest tests/ --pdbcls=IPython.terminal.debugger:TerminalPdb  # Use ipdb
```

## Coverage Reports

### Terminal Report
```bash
pytest tests/ --cov=todo_cli --cov-report=term
pytest tests/ --cov=todo_cli --cov-report=term-missing  # Show missing lines
```

### HTML Report
```bash
pytest tests/ --cov=todo_cli --cov-report=html
# Open htmlcov/index.html in browser
```

### Coverage for Specific Module
```bash
pytest tests/ --cov=todo_cli.utils       # Utils only
pytest tests/ --cov=todo_cli.cli         # CLI only
```

## Performance

### Show Slowest Tests
```bash
pytest tests/ --durations=10   # Show 10 slowest tests
pytest tests/ --durations=0    # Show all test durations
```

### Parallel Execution
```bash
pip install pytest-xdist
pytest tests/ -n auto          # Use all CPU cores
pytest tests/ -n 4             # Use 4 workers
```

## Markers (Future Enhancement)

Add markers to conftest.py:
```python
# In conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks integration tests")
```

Then run:
```bash
pytest tests/ -m "not slow"     # Skip slow tests
pytest tests/ -m integration    # Run only integration tests
```

## Output Formats

### JUnit XML (for CI/CD)
```bash
pytest tests/ --junit-xml=test-results.xml
```

### JSON Report
```bash
pip install pytest-json-report
pytest tests/ --json-report --json-report-file=report.json
```

## Common Issues

### Import Errors
```bash
# Install package in development mode
pip install -e .
```

### No Tests Collected
```bash
# Check you're in the right directory
pwd
cd /path/to/todo_cli
pytest tests/
```

### Fixtures Not Found
```bash
# Ensure conftest.py is in tests/ directory
ls tests/conftest.py
```

## Test Statistics

- Total Tests: 93
- CLI Tests: 52
- Utility Tests: 41
- Test Coverage: 95%+
- Average Runtime: < 3 seconds

## Quick Checks

### Pre-commit Checks
```bash
# Run all tests
pytest tests/

# Check coverage
pytest tests/ --cov=todo_cli --cov-fail-under=95

# Type checking
mypy todo_cli/

# Code formatting
black --check todo_cli/
ruff check todo_cli/
```

### Full Test Suite
```bash
# Run everything
pytest tests/ -v --cov=todo_cli --cov-report=term-missing --cov-fail-under=95
```

## Continuous Integration

Example pytest command for CI:
```bash
pytest tests/ \
  --verbose \
  --cov=todo_cli \
  --cov-report=term-missing \
  --cov-report=xml \
  --junit-xml=test-results.xml \
  --cov-fail-under=95
```

## File Paths

All file paths should be absolute when referencing test files:

- Tests: `/home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli/tests/`
- Conftest: `/home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli/tests/conftest.py`
- CLI Tests: `/home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli/tests/test_cli.py`
- Utils Tests: `/home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli/tests/test_utils.py`
