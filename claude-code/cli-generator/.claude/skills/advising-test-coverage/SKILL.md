---
name: advising-test-coverage
description: Suggests comprehensive test cases for CLI commands including edge cases and error scenarios. Use when generating tests, discussing test coverage, or after implementing CLI commands.
---

# Test Coverage Advisor

## Test Categories to Suggest

For each CLI command, ensure tests cover:

### 1. Happy Path
- Basic usage with required arguments only
- Usage with all options specified
- Common option combinations

### 2. Edge Cases
- Empty input
- Very large input
- Special characters in arguments
- Paths with spaces
- Unicode content

### 3. Error Handling
- Missing required arguments
- Invalid option values
- File not found
- Permission denied
- Invalid format/type

### 4. Exit Codes
- 0 for success
- 1 for user error (bad input)
- 2 for system error (file not found)

## Suggestion Format

When reviewing or generating tests:

```
Test coverage for `{command}`:

✅ Covered:
- Basic usage
- Output formatting

⚠️ Missing:
- Edge case: empty input
- Error: invalid format option
- Exit code verification

Suggested test:
def test_{command}_empty_input():
    result = runner.invoke(cli, ['{command}', ''])
    assert result.exit_code == 1
    assert 'error' in result.output.lower()
```
