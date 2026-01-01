# Notes CLI

A markdown-based note-taking CLI for creating, managing, searching, and organizing notes.

## Features

- Create and edit markdown notes with YAML frontmatter
- Search notes by content or title
- Tag-based organization and filtering
- Rich terminal output with colored formatting
- Export to multiple formats (HTML, JSON, TXT)
- Notes stored as plain markdown files (portable and future-proof)

## Installation

```bash
# Install from source
pip install -e .

# With export support
pip install -e ".[export]"

# For development
pip install -e ".[dev]"
```

## Quick Start

```bash
# Create your first note
notes-cli create "My First Note"

# List all notes
notes-cli list

# Search notes
notes-cli search "todo"

# View a note
notes-cli view "My First Note"

# Add tags to a note
notes-cli edit "My First Note" --add-tags personal,ideas

# Export notes to HTML
notes-cli export ./export --format html
```

## Commands

### create

Create a new markdown note:

```bash
notes-cli create "My Note Title"
notes-cli create "Python Tips" --tags python,programming
notes-cli create "Meeting Notes" --editor vim
notes-cli create "Template Note" --template ~/templates/meeting.md
```

### list

List all notes with optional filtering:

```bash
notes-cli list
notes-cli list --tags python,programming
notes-cli list --sort-by created --reverse
notes-cli list --limit 10
```

### view

View/read a note in the terminal:

```bash
notes-cli view "My Note"
notes-cli view 123456
notes-cli view "Long Document" --raw
notes-cli view "Article" --no-pager
```

### search

Search notes by content or title:

```bash
notes-cli search "todo"
notes-cli search "python" --title-only
notes-cli search "meeting" --tags work
notes-cli search "API" --case-sensitive
```

### edit

Edit an existing note:

```bash
notes-cli edit "My Note"
notes-cli edit 123456 --editor vim
notes-cli edit "Meeting Notes" --rename "Team Meeting Notes"
notes-cli edit "Python Tips" --add-tags tutorial,advanced
notes-cli edit "Old Note" --remove-tags outdated
```

### delete

Delete one or more notes:

```bash
notes-cli delete "My Note"
notes-cli delete 123456,789012
notes-cli delete "Old Note" --force
notes-cli delete "Temp" --no-backup
```

### tag

Manage tags across notes:

```bash
# List all tags
notes-cli tag list
notes-cli tag list --count

# Rename a tag
notes-cli tag rename --old-tag python --new-tag python3

# Merge tags
notes-cli tag merge --old-tag todo --new-tag tasks
```

### export

Export notes to different formats:

```bash
notes-cli export ./export/notes.html
notes-cli export ./output --format json
notes-cli export ./docs --format html --tags python
notes-cli export ./all.txt --format txt --single-file
```

## Global Options

- `--verbose, -v` - Enable verbose debug output
- `--quiet, -q` - Suppress non-error output
- `--no-color` - Disable colored output
- `--notes-dir, -d PATH` - Notes directory (default: `~/.notes`)

## Note Format

Notes are stored as markdown files with YAML frontmatter:

```markdown
---
id: 123456
title: My Note Title
tags:
  - python
  - programming
created: '2025-12-30T10:00:00'
modified: '2025-12-30T11:30:00'
---

# Note Content

This is the content of your note in markdown format.

- You can use lists
- **Bold text**
- *Italic text*
- `code blocks`

## Subheadings

And more!
```

## Notes Directory Structure

```
~/.notes/
├── my-first-note.md
├── python-tips.md
├── meeting-notes.md
└── .backups/
    └── 20251230_143000/
        └── deleted-note.md
```

## Exit Codes

- `0` - Success
- `1` - User error (invalid arguments, note not found, etc.)
- `2` - System error (file I/O error, unexpected exception)

## Requirements

- Python 3.11+
- click >= 8.1.0
- rich >= 13.0.0
- pyyaml >= 6.0
- python-frontmatter >= 1.0.0
- markdown >= 3.4.0 (optional, for HTML export)

## License

MIT License
