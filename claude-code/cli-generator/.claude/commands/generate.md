# /generate - Generate CLI Code

## Purpose
Generate complete CLI code from the current or specified design.

## Usage
```
/generate                    # From current design in session
/generate <spec_file>        # From saved spec file
/generate --output ./my-cli  # Custom output directory
/generate --with-tests       # Include test files
```

## Process

### 1. Get Specification
- If spec_file provided: Load from file
- If design in current session: Use that
- If neither: Error - "No design found. Run /design first."

### 2. Validate Specification
Run validators:
- [ ] CLI name is valid
- [ ] No duplicate commands
- [ ] No duplicate options
- [ ] All required fields present

### 3. Generate Code
Using CodeGenerator, create:
- `<name>/cli.py` - Main CLI with all commands
- `<name>/__init__.py` - Package init
- `pyproject.toml` - Project configuration
- `README.md` - Documentation

If --with-tests:
- `tests/test_cli.py` - CLI tests
- `tests/conftest.py` - Test fixtures

### 4. Report Results
```
Generated CLI: <name>
====================

Files created:
  ✓ <name>/cli.py (XX lines)
  ✓ <name>/__init__.py
  ✓ pyproject.toml
  ✓ README.md

Quick start:
  cd <output_path>
  uv pip install -e .
  <name> --help
```
