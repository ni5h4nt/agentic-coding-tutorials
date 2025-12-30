# Installation Guide

## Quick Start

1. Navigate to the todo-cli directory:
```bash
cd /home/nishant/documents/repositories/github/personal/agentic-coding-tutorials/claude-code/cli-generator/generated/todo_cli
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Verify installation:
```bash
todo-cli --version
```

4. Try it out:
```bash
todo-cli add "My first task"
todo-cli list
```

## Alternative Installation Methods

### Install from source (production mode)
```bash
pip install .
```

### Install with development dependencies
```bash
pip install -e ".[dev]"
```

## Uninstall

```bash
pip uninstall todo-cli
```

## Troubleshooting

### Command not found after installation

Make sure your Python scripts directory is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### Module import errors

Ensure all dependencies are installed:
```bash
pip install click>=8.1.0 rich>=13.0.0
```

### Permission errors on storage directory

The CLI will try to create `~/.todo-cli/` directory. If you encounter permission issues, you can use a custom location:
```bash
todo-cli --config ~/custom-location/todos.json add "Test task"
```
