# /add-command - Add Command to Existing CLI

## Purpose
Add a new command to an already generated CLI without losing
existing customizations.

## Usage
```
/add-command <cli_path> <description>
/add-command ./generated/img-compress "Add a resize command"
```

## Process

### 1. Load Existing CLI
- Find and parse existing CLISpec
- Load current cli.py to check for customizations
- Identify insertion point for new command

### 2. Design New Command
Generate CommandSpec for the new command:
- Parse description
- Determine arguments and options
- Create examples
- Check for conflicts with existing commands

### 3. Preview Changes
```
Adding command to: <cli_name>

New Command: <command_name>
===========================
Description: <description>
Arguments: <args>
Options: <options>

Existing commands unchanged:
  ✓ <existing_command_1>
  ✓ <existing_command_2>

Proceed? [y/n/edit]
```

### 4. Apply Changes
If approved:
- Update CLISpec
- Regenerate cli.py (preserving customizations if possible)
- Update README.md
