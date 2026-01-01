# Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Installation Steps

### 1. Install the CLI

Navigate to the `notes_cli` directory and install:

```bash
cd /home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/notes_cli

# Install in development mode (editable)
pip install -e .

# Or install with export support (adds markdown library)
pip install -e ".[export]"
```

### 2. Verify Installation

Check that the CLI is installed correctly:

```bash
notes-cli --version
notes-cli --help
```

### 3. Create Your First Note

```bash
# This will create ~/.notes directory and open your editor
notes-cli create "My First Note"
```

## Alternative: Use a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install the CLI
pip install -e ".[export,dev]"

# Use the CLI
notes-cli create "Test Note"
```

## Configuration

### Change Notes Directory

By default, notes are stored in `~/.notes`. To use a different location:

```bash
# Set for a single command
notes-cli list --notes-dir ~/Documents/my-notes

# Or set environment variable (add to ~/.bashrc or ~/.zshrc)
export NOTES_DIR="$HOME/Documents/my-notes"
```

### Set Your Preferred Editor

The CLI uses your `$EDITOR` environment variable:

```bash
# Add to ~/.bashrc or ~/.zshrc
export EDITOR="vim"  # or "nano", "code", "emacs", etc.
```

## Troubleshooting

### Command Not Found

If `notes-cli` command is not found after installation:

1. Check that the installation directory is in your PATH:
   ```bash
   python -m pip show notes-cli
   ```

2. Try running directly with Python:
   ```bash
   python -m notes_cli.cli --help
   ```

3. Reinstall with `--force-reinstall`:
   ```bash
   pip install --force-reinstall -e .
   ```

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install click rich pyyaml python-frontmatter markdown
```

### Permission Errors

If you can't create the notes directory:

```bash
# Create it manually
mkdir -p ~/.notes
chmod 755 ~/.notes
```

## Uninstallation

To remove the CLI:

```bash
pip uninstall notes-cli
```

## Next Steps

See [README.md](README.md) for usage examples and command reference.
