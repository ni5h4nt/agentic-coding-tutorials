# /implement - Implement Command Logic

## Purpose
Replace TODO stub in generated command with actual implementation.

## Usage
```
/implement <cli_path> <command_name>
/implement ./generated/img-compress compress
/implement ./generated/img-compress all  # Implement all commands
```

## Process

### 1. Analyze Command
- Load the command from cli.py
- Parse arguments and options
- Understand what the command should do

### 2. Design Implementation
```
Implementing: <cli_name> <command_name>

Command Purpose: <description>

Implementation Plan:
  1. <step 1>
  2. <step 2>
  3. <step 3>

Error cases to handle:
  - <error case 1>
  - <error case 2>

Proceed with implementation? [y/n/modify]
```

### 3. Generate Implementation
Write the actual command logic:
- Input validation
- Core functionality
- Error handling with user-friendly messages
- Progress output (respecting --quiet/--verbose)
- Proper exit codes

### 4. Write Tests
For the implementation:
- Happy path test
- Error case tests
- Edge case tests
