# /refine - Refine CLI Design

## Purpose
Modify the current CLI design based on feedback without regenerating
everything from scratch.

## Usage
```
/refine <feedback>
/refine "Add a --dry-run flag to all commands"
/refine "Rename the 'process' command to 'convert'"
/refine "Remove the 'config' command, not needed"
```

## Process

### 1. Load Current Design
- Get CLISpec from current session
- If no design: Error - "No design found. Run /design first."

### 2. Parse Feedback
Identify the type of change:
- Add: New command, option, argument
- Modify: Change name, description, type
- Remove: Delete command, option
- Global: Apply to all commands

### 3. Apply Changes
Update the CLISpec:
- Validate changes don't break anything
- Maintain consistency (no duplicate names, etc.)

### 4. Show Diff
```
Design Refinement
=================

Changes applied:
+ Added --dry-run flag to all commands
  ~ Modified 'compress' command options

Before:
  compress --quality --output

After:
  compress --quality --output --dry-run

Next steps:
  /refine "<more changes>"
  /generate
```

## Maintains Session State
The refined design stays in session for:
- Further /refine commands
- /generate to create code
- /save-spec to export
