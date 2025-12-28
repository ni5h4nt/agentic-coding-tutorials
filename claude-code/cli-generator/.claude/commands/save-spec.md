# /save-spec - Save CLI Specification

## Purpose
Save the current CLI design to a JSON file for later use or sharing.

## Usage
```
/save-spec                    # Save as <cli-name>.json
/save-spec my-design.json     # Custom filename
/save-spec --format yaml      # Save as YAML
```

## Process

### 1. Get Current Design
- Load CLISpec from session
- Error if no design exists

### 2. Serialize
Convert to JSON (default) or YAML:
- Pretty print with indentation
- Include all fields
- Add metadata (generator version, timestamp)

### 3. Save File
Write to specified location:
- Default: ./specs/<cli-name>.json
- Custom: user-provided path

### 4. Confirm
```
Specification saved
===================

File: ./specs/img-compress.json
Size: 2.3 KB
Commands: 3
Options: 12

Use with:
  /generate ./specs/img-compress.json
  cli-gen build ./specs/img-compress.json
```
