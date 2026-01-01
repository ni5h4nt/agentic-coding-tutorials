# Notes CLI Test Suite

Comprehensive pytest test suite for the notes-cli application.

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures and test configuration
├── test_cli.py          # Main CLI and global options tests
├── test_create.py       # Create command tests
├── test_list.py         # List command tests
├── test_view.py         # View command tests
├── test_search.py       # Search command tests
├── test_delete.py       # Delete command tests
├── test_edit.py         # Edit command tests
├── test_tag.py          # Tag management tests
└── test_export.py       # Export command tests
```

## Test Coverage

### 1. CLI Basics (`test_cli.py`)
- Help and version flags
- Global options (--verbose, --quiet, --no-color, --notes-dir)
- Command discovery
- Error handling
- Exit codes

### 2. Create Command (`test_create.py`)
- Basic note creation
- Title sanitization
- Tag handling (single, multiple, with spaces)
- Template support
- Editor integration
- Duplicate detection
- Special characters and unicode
- Integration with other commands

### 3. List Command (`test_list.py`)
- Empty directory handling
- Single and multiple notes
- Tag filtering (single, multiple, nonexistent)
- Sorting (by title, created, modified, size)
- Reverse sorting
- Limiting results
- Option combinations
- Edge cases (corrupt notes, non-markdown files)

### 4. View Command (`test_view.py`)
- View by title, ID, partial match
- Raw mode
- Pager support
- Metadata display
- Empty notes
- Special characters
- Case-insensitive matching

### 5. Search Command (`test_search.py`)
- Search in title and content
- Title-only and content-only modes
- Case sensitivity
- Tag filtering
- Multiple matches
- Context display
- Special characters and unicode
- Regex character escaping

### 6. Delete Command (`test_delete.py`)
- Delete by title and ID
- Multiple deletion
- Confirmation prompts
- Force flag
- Backup creation
- Mixed valid/invalid identifiers
- Integration tests

### 7. Edit Command (`test_edit.py`)
- Edit by title and ID
- Rename notes
- Add tags (single, multiple, duplicates)
- Remove tags (single, multiple, all)
- Combined operations
- Editor integration
- Metadata-only edits
- Timestamp updates

### 8. Tag Command (`test_tag.py`)
- List tags (with and without counts)
- Rename tags across notes
- Merge tags
- Confirmation prompts
- Nonexistent tags
- Empty directory handling

### 9. Export Command (`test_export.py`)
- JSON export (single file, multiple files)
- Text export (single file, multiple files)
- HTML export (with markdown rendering)
- PDF export (not implemented)
- Tag filtering
- Single-file option
- Parent directory creation
- Special characters preservation

## Fixtures

### Core Fixtures (`conftest.py`)

- **runner**: Click test runner for CLI invocation
- **temp_notes_dir**: Temporary directory for test notes
- **empty_notes_dir**: Empty notes directory
- **sample_note**: Single note with standard metadata
- **multiple_notes**: Five notes with various tags and content
- **note_with_special_chars**: Note with special characters and unicode
- **notes_with_long_content**: Note with 100+ lines for pager testing
- **template_file**: Template file for create command testing
- **mock_editor**: Mock editor to prevent actual editor from opening

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_create.py
```

### Run Specific Test Class
```bash
pytest tests/test_create.py::TestCreateBasic
```

### Run Specific Test
```bash
pytest tests/test_create.py::TestCreateBasic::test_create_note_basic
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=notes_cli --cov-report=html
```

### Run Only Fast Tests (exclude integration)
```bash
pytest tests/ -m "not integration"
```

## Test Categories

### Happy Path Tests
Standard usage with valid inputs:
- Creating notes with valid titles
- Listing notes with proper filters
- Searching with simple queries
- Editing with valid changes

### Error Case Tests
Invalid inputs and error conditions:
- Missing required arguments
- Nonexistent notes
- Invalid option combinations
- Permission errors
- Duplicate titles

### Edge Case Tests
Boundary conditions and special cases:
- Empty notes directory
- Empty note content
- Very long titles (200+ chars)
- Special characters in titles
- Unicode content
- Corrupt note files
- Hidden files
- Subdirectories

### Integration Tests
Full workflows across multiple commands:
- Create → List → View
- Create → Edit → View
- Create → Search → Delete
- Edit → Tag → Export
- List → Filter → Export

## Writing New Tests

### Test Class Structure
```python
class TestFeatureName:
    """Test description."""

    def test_specific_behavior(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test what this does."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'command', 'args'
        ])
        assert result.exit_code == 0
        assert 'expected' in result.output
```

### Best Practices

1. **Descriptive Names**: Test names should clearly describe what they test
2. **One Assertion Per Concept**: Focus each test on one behavior
3. **Use Fixtures**: Leverage shared fixtures from conftest.py
4. **Test Exit Codes**: Always check result.exit_code
5. **Verify Output**: Check command output contains expected messages
6. **Clean Up**: Use temp_notes_dir for isolation, no manual cleanup needed
7. **Mock External Dependencies**: Use mock_editor for editor interactions

### Fixture Usage
```python
def test_with_multiple_fixtures(
    self,
    runner: CliRunner,           # CLI test runner
    temp_notes_dir: Path,        # Temp directory
    multiple_notes: list[Path],  # Pre-created notes
    mock_editor: None            # Mocked editor
) -> None:
    """Example showing multiple fixtures."""
    # Test code here
```

## Dependencies

- pytest >= 7.0.0
- click >= 8.0.0
- python-frontmatter >= 1.0.0
- rich >= 13.0.0

Optional for HTML export tests:
- markdown >= 3.0.0

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- No interactive prompts (use `input=` parameter)
- Isolated temporary directories
- No external dependencies (files, databases)
- Fast execution (< 30 seconds for full suite)
- Platform independent (Windows, macOS, Linux)

## Known Limitations

1. **Editor Tests**: Real editor interactions cannot be tested, only mocked
2. **Pager Tests**: Pager behavior is difficult to test comprehensively
3. **Color Output**: ANSI color codes testing is limited
4. **Timing Tests**: Modified timestamps may vary slightly
5. **PDF Export**: Not implemented, tests verify error message only

## Contributing

When adding new features:
1. Add corresponding test fixtures in conftest.py
2. Create test class for the feature
3. Cover happy path, error cases, and edge cases
4. Add integration tests for workflows
5. Update this README with new test categories

## Test Metrics

Expected test counts:
- test_cli.py: ~20 tests
- test_create.py: ~25 tests
- test_list.py: ~40 tests
- test_view.py: ~20 tests
- test_search.py: ~35 tests
- test_delete.py: ~25 tests
- test_edit.py: ~35 tests
- test_tag.py: ~25 tests
- test_export.py: ~35 tests

**Total: ~260 tests**

Expected coverage: >90% of CLI code
