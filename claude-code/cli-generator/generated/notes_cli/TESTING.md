# Notes CLI - Testing Documentation

## Test Suite Overview

Comprehensive pytest test suite for the notes-cli application with **242 test cases** covering all commands and functionality.

## Quick Start

```bash
# Install dependencies (if not already installed)
pip install -e .
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_create.py

# Run with coverage (requires pytest-cov)
pip install pytest-cov
pytest tests/ --cov=notes_cli --cov-report=html
```

## Test Statistics

### Test Count by File

| File | Tests | Size | Coverage Area |
|------|-------|------|---------------|
| test_cli.py | 22 | 7.5K | Main CLI, global options, help, version |
| test_create.py | 20 | 12K | Note creation, tags, templates, editor |
| test_delete.py | 24 | 12K | Deletion, backups, confirmation prompts |
| test_edit.py | 30 | 18K | Editing, renaming, tag management |
| test_export.py | 28 | 20K | JSON/HTML/TXT export, filtering |
| test_list.py | 34 | 16K | Listing, filtering, sorting, limiting |
| test_search.py | 35 | 16K | Searching, highlighting, case sensitivity |
| test_tag.py | 28 | 16K | Tag listing, renaming, merging |
| test_view.py | 21 | 9.8K | Viewing notes, raw mode, pager |
| **Total** | **242** | **137K** | **All commands + utilities** |

### Test Categories

- **Happy Path**: ~100 tests - Standard usage with valid inputs
- **Error Cases**: ~80 tests - Invalid inputs and error conditions
- **Edge Cases**: ~50 tests - Boundary conditions and special scenarios
- **Integration**: ~12 tests - Multi-command workflows

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures and test configuration (6.3K)
├── test_cli.py          # CLI basics and global options (22 tests)
├── test_create.py       # Create command (20 tests)
├── test_list.py         # List command (34 tests)
├── test_view.py         # View command (21 tests)
├── test_search.py       # Search command (35 tests)
├── test_delete.py       # Delete command (24 tests)
├── test_edit.py         # Edit command (30 tests)
├── test_tag.py          # Tag management (28 tests)
├── test_export.py       # Export functionality (28 tests)
├── README.md            # Detailed test documentation
└── TEST_SUMMARY.md      # Comprehensive test summary
```

## Fixtures (conftest.py)

### Core Fixtures

- **runner**: Click CliRunner for invoking commands
- **temp_notes_dir**: Isolated temporary directory for tests
- **empty_notes_dir**: Empty directory for edge case testing
- **sample_note**: Single note with standard metadata
- **multiple_notes**: Five diverse notes for filtering/searching
- **note_with_special_chars**: Unicode and special character testing
- **notes_with_long_content**: 100-line note for pager testing
- **template_file**: Template file for create command
- **mock_editor**: Mocked editor to prevent interactive prompts

## Test Coverage Areas

### 1. Create Command (test_create.py)
✓ Basic note creation with title sanitization
✓ Single and multiple tags
✓ Tag parsing with spaces
✓ Template support from file
✓ Custom editor specification
✓ Duplicate title detection
✓ Special characters in titles
✓ Unicode content handling
✓ Empty and very long titles
✓ Integration: create → list, create → view

### 2. List Command (test_list.py)
✓ Empty directory handling
✓ Single and multiple note display
✓ Tag filtering (single, multiple, nonexistent)
✓ Sorting by: title, created, modified, size
✓ Reverse sorting
✓ Result limiting with --limit
✓ Combining filters, sorting, and limiting
✓ Edge cases: corrupt notes, non-markdown files
✓ Output formatting with/without colors

### 3. View Command (test_view.py)
✓ View by title, ID, partial match
✓ Raw mode showing frontmatter
✓ Pager support (--pager/--no-pager)
✓ Metadata display
✓ Empty note handling
✓ Special characters in content
✓ Case-insensitive title matching
✓ Unicode rendering

### 4. Search Command (test_search.py)
✓ Search in title and content
✓ Title-only search mode
✓ Content-only search mode
✓ Case-sensitive vs case-insensitive
✓ Tag filtering within search results
✓ Multiple match handling
✓ Context snippet display
✓ Special characters and unicode
✓ Regex character escaping
✓ Match highlighting (with colors)

### 5. Delete Command (test_delete.py)
✓ Delete by title and ID
✓ Multiple deletion (comma-separated)
✓ Confirmation prompts
✓ Force flag to skip confirmation
✓ Backup creation (default on)
✓ No-backup option
✓ Backup directory structure
✓ Mixed valid/invalid identifiers
✓ Delete all notes scenario

### 6. Edit Command (test_edit.py)
✓ Edit by title and ID
✓ Rename notes (--rename)
✓ Add tags (--add-tags)
✓ Remove tags (--remove-tags)
✓ Combined operations
✓ Duplicate tag prevention
✓ Editor integration (mocked)
✓ Metadata-only edits
✓ Content preservation
✓ Modified timestamp updates
✓ Duplicate title prevention

### 7. Tag Command (test_tag.py)
✓ List all tags
✓ List tags with counts
✓ Rename tags across all notes
✓ Merge tags
✓ Confirmation prompts
✓ Nonexistent tag handling
✓ Empty directory cases
✓ Multiple note updates
✓ Tag deduplication

### 8. Export Command (test_export.py)
✓ JSON export (single file)
✓ JSON export (multiple files)
✓ Text export (single file)
✓ Text export (multiple files)
✓ HTML export with markdown rendering
✓ PDF export (not implemented error)
✓ Tag filtering during export
✓ Single-file flag
✓ Format validation
✓ Parent directory creation
✓ Special character preservation
✓ Metadata inclusion

### 9. CLI Basics (test_cli.py)
✓ Help flag (--help)
✓ Version flag (--version)
✓ Invalid command handling
✓ Global options: --verbose, --quiet
✓ Global options: --no-color, --notes-dir
✓ Combined global flags
✓ Command help text
✓ Exit codes (0 for success, 1/2 for errors)

## Running Tests

### Basic Usage

```bash
# All tests
pytest tests/

# Specific file
pytest tests/test_create.py

# Specific test class
pytest tests/test_create.py::TestCreateBasic

# Specific test
pytest tests/test_create.py::TestCreateBasic::test_create_note_basic

# With verbose output
pytest tests/ -v

# Show print statements
pytest tests/ -s

# Stop on first failure
pytest tests/ -x
```

### Advanced Usage

```bash
# Run only fast tests
pytest tests/ -k "not slow"

# Run with coverage
pytest tests/ --cov=notes_cli --cov-report=term-missing
pytest tests/ --cov=notes_cli --cov-report=html

# Run in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest tests/ -n auto

# Generate JUnit XML report (for CI)
pytest tests/ --junitxml=test-results.xml

# Show slowest tests
pytest tests/ --durations=10
```

## Writing New Tests

### Example Test Structure

```python
class TestNewFeature:
    """Test new feature description."""

    def test_basic_functionality(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test basic use case."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'command', 'args'
        ])
        assert result.exit_code == 0
        assert 'expected output' in result.output

    def test_error_case(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test error handling."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'command', 'invalid-args'
        ])
        assert result.exit_code != 0
        assert 'error message' in result.output.lower()
```

### Best Practices

1. **Descriptive Names**: Use clear, descriptive test method names
2. **Single Assertion**: Focus each test on one behavior
3. **Use Fixtures**: Leverage shared fixtures from conftest.py
4. **Test Exit Codes**: Always verify result.exit_code
5. **Verify Output**: Check that output contains expected messages
6. **Isolation**: Use temp_notes_dir for test isolation
7. **Mock External**: Mock editor and other external dependencies

## Continuous Integration

Tests are CI/CD ready:
- No interactive prompts (input parameter or mocks)
- Fast execution (< 30 seconds full suite)
- Isolated temporary directories
- No external dependencies
- Platform independent (Windows, macOS, Linux)
- Clear pass/fail signals

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ -v --cov=notes_cli
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Expected Coverage

- **Overall**: >90% code coverage
- **Commands**: 100% (all commands have dedicated tests)
- **Utils**: >85% (helper functions well-covered)
- **CLI**: 100% (main entry point fully tested)

## Test Execution Time

- **Full suite**: ~5-10 seconds
- **Single file**: <1 second
- **Per test**: <0.1 seconds average

Fast enough for:
- Pre-commit hooks
- Continuous integration
- Frequent local testing
- TDD workflows

## Dependencies

### Required for Testing
```bash
pip install pytest>=7.0.0
pip install click>=8.0.0
pip install python-frontmatter>=1.0.0
pip install rich>=13.0.0
```

### Optional for Testing
```bash
pip install pytest-cov      # Coverage reports
pip install pytest-xdist    # Parallel execution
pip install markdown        # HTML export tests
```

## Known Limitations

1. **Editor Tests**: Real editor interactions cannot be fully tested (mocked instead)
2. **Pager Tests**: Pager behavior is complex to test (basic coverage only)
3. **Color Output**: ANSI color code testing is limited
4. **Timing Tests**: Modified timestamps may vary slightly in fast execution
5. **PDF Export**: Not implemented, only error message tested

## Troubleshooting

### Tests Fail with "No module named 'notes_cli'"
```bash
# Install package in development mode
pip install -e .
```

### Tests Fail with "markdown module not found"
```bash
# Install markdown for HTML export tests
pip install markdown
# Or skip those tests
pytest tests/ -k "not html"
```

### Tests Are Slow
```bash
# Run in parallel
pip install pytest-xdist
pytest tests/ -n auto
```

### Need to Debug a Test
```bash
# Run single test with print statements
pytest tests/test_create.py::TestCreateBasic::test_create_note_basic -s -v
```

## Documentation Files

- **tests/README.md**: Detailed test documentation with examples
- **tests/TEST_SUMMARY.md**: Comprehensive test metrics and summary
- **tests/conftest.py**: Fixture definitions and configuration
- **pytest.ini**: Pytest configuration (in project root)
- **TESTING.md**: This file - quick reference guide

## Contributing

When adding new features to notes-cli:

1. **Write tests first** (TDD approach)
2. **Follow existing patterns** in test files
3. **Add fixtures** if new test data needed
4. **Cover all paths**: happy, error, edge cases
5. **Update documentation** (this file and README)
6. **Verify coverage** remains >90%
7. **Run full suite** before committing

```bash
# Pre-commit checklist
pytest tests/ -v                    # All tests pass
pytest tests/ --cov=notes_cli       # Coverage >90%
python3 -m py_compile tests/*.py    # No syntax errors
```

## Support

For test-related questions:
- See detailed examples in individual test files
- Check fixture definitions in conftest.py
- Review test categories in README.md
- Examine integration tests for workflows

---

**Test Suite Version**: 1.0
**Last Updated**: 2025-12-30
**Total Tests**: 242
**Total Coverage**: >90% expected
**Execution Time**: <30 seconds
