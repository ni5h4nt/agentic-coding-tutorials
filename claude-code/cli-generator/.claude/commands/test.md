# /test - Smart Test Runner for Generated CLIs

## Purpose
Run tests for generated CLIs with intelligent output and suggestions.

## Usage
```
/test <cli_path>                  # Run all tests
/test <cli_path> <command_name>   # Test specific command
/test <cli_path> --coverage       # With coverage report
/test <cli_path> --fix            # Auto-fix simple issues
```

## Process

### 1. Discover Tests
- Find test files in <cli_path>/tests/
- Parse test functions
- Check test dependencies

### 2. Run Tests
Execute: `pytest <cli_path>/tests -v --tb=short`

### 3. Present Results
```
Test Results: <cli_name>
========================

Summary: 12 passed, 2 failed, 1 skipped

✓ test_cli_help
✓ test_cli_version
✓ test_compress_basic
✗ test_compress_invalid_quality
  Line 45: AssertionError
  Expected: Exit code 1
  Got: Exit code 0 (no validation on quality range)

  Suggested fix: Add validation in compress command

Coverage: 78% (target: 80%)

Next steps:
  /implement <cli_path> compress  # Fix validation
  /test <cli_path> --fix          # Auto-fix if possible
```
