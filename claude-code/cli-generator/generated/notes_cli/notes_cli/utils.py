"""Shared utilities for notes CLI."""

import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

import click
import frontmatter
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


class Note:
    """Represents a markdown note with frontmatter metadata."""

    def __init__(self, filepath: Path):
        """Initialize a note from a file path.

        Args:
            filepath: Path to the markdown file
        """
        self.filepath = filepath
        self._load()

    def _load(self) -> None:
        """Load note content and metadata from file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            self.content = post.content
            self.metadata = post.metadata

        # Ensure required metadata fields exist
        if 'id' not in self.metadata:
            self.metadata['id'] = self._generate_id()
        if 'title' not in self.metadata:
            self.metadata['title'] = self.filepath.stem
        if 'tags' not in self.metadata:
            self.metadata['tags'] = []
        if 'created' not in self.metadata:
            self.metadata['created'] = datetime.now().isoformat()
        if 'modified' not in self.metadata:
            self.metadata['modified'] = datetime.now().isoformat()

    def _generate_id(self) -> int:
        """Generate a unique integer ID based on filepath.

        Returns:
            Integer ID
        """
        hash_obj = hashlib.md5(str(self.filepath).encode())
        return int(hash_obj.hexdigest()[:8], 16) % 1000000

    def save(self) -> None:
        """Save note content and metadata to file."""
        self.metadata['modified'] = datetime.now().isoformat()
        post = frontmatter.Post(self.content, **self.metadata)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

    @property
    def id(self) -> int:
        """Get note ID."""
        return self.metadata['id']

    @property
    def title(self) -> str:
        """Get note title."""
        return self.metadata['title']

    @property
    def tags(self) -> list[str]:
        """Get note tags."""
        return self.metadata.get('tags', [])

    @property
    def created(self) -> str:
        """Get creation timestamp."""
        return self.metadata.get('created', '')

    @property
    def modified(self) -> str:
        """Get modification timestamp."""
        return self.metadata.get('modified', '')

    def __repr__(self) -> str:
        return f"Note(id={self.id}, title='{self.title}')"


def get_notes_dir(notes_dir: str | None) -> Path:
    """Get and ensure notes directory exists.

    Args:
        notes_dir: Path to notes directory or None for default

    Returns:
        Path object for notes directory

    Raises:
        click.ClickException: If directory cannot be created
    """
    if notes_dir:
        path = Path(notes_dir).expanduser().resolve()
    else:
        path = Path.home() / '.notes'

    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise click.ClickException(f"Failed to create notes directory: {e}")

    return path


def load_all_notes(notes_dir: Path) -> list[Note]:
    """Load all notes from the notes directory.

    Args:
        notes_dir: Path to notes directory

    Returns:
        List of Note objects
    """
    notes = []
    for filepath in notes_dir.glob('*.md'):
        try:
            note = Note(filepath)
            notes.append(note)
        except Exception as e:
            if not is_quiet():
                console.print(f"[yellow]Warning: Failed to load {filepath.name}: {e}[/yellow]")
    return notes


def find_note(notes_dir: Path, identifier: str) -> Note | None:
    """Find a note by title or ID.

    Args:
        notes_dir: Path to notes directory
        identifier: Note title or ID

    Returns:
        Note object or None if not found
    """
    notes = load_all_notes(notes_dir)

    # Try to match by ID first
    try:
        note_id = int(identifier)
        for note in notes:
            if note.id == note_id:
                return note
    except ValueError:
        pass

    # Try exact title match
    for note in notes:
        if note.title.lower() == identifier.lower():
            return note

    # Try partial title match
    for note in notes:
        if identifier.lower() in note.title.lower():
            return note

    return None


def sanitize_filename(title: str) -> str:
    """Convert title to safe filename.

    Args:
        title: Note title

    Returns:
        Sanitized filename (without extension)
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces with hyphens
    filename = re.sub(r'\s+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    # Limit length
    filename = filename[:100]
    return filename or 'untitled'


def get_editor() -> str:
    """Get the preferred text editor.

    Returns:
        Editor command
    """
    return os.environ.get('EDITOR', 'nano')


def open_in_editor(filepath: Path, editor: str | None = None) -> None:
    """Open a file in the user's preferred editor.

    Args:
        filepath: Path to file to edit
        editor: Editor command (overrides default)

    Raises:
        click.ClickException: If editor fails
    """
    editor_cmd = editor or get_editor()
    try:
        click.edit(filename=str(filepath), editor=editor_cmd)
    except Exception as e:
        raise click.ClickException(f"Failed to open editor: {e}")


def parse_tags(tags_str: str | None) -> list[str]:
    """Parse comma-separated tags string.

    Args:
        tags_str: Comma-separated tags

    Returns:
        List of tag strings
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]


def format_datetime(dt_str: str) -> str:
    """Format ISO datetime string for display.

    Args:
        dt_str: ISO format datetime string

    Returns:
        Formatted datetime string
    """
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return dt_str


def format_filesize(filepath: Path) -> str:
    """Format file size for display.

    Args:
        filepath: Path to file

    Returns:
        Formatted file size string
    """
    try:
        size = filepath.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except OSError:
        return "Unknown"


def is_verbose() -> bool:
    """Check if verbose mode is enabled.

    Returns:
        True if verbose mode is enabled
    """
    ctx = click.get_current_context()
    return ctx.obj.get('verbose', False) if ctx.obj else False


def is_quiet() -> bool:
    """Check if quiet mode is enabled.

    Returns:
        True if quiet mode is enabled
    """
    ctx = click.get_current_context()
    return ctx.obj.get('quiet', False) if ctx.obj else False


def use_color() -> bool:
    """Check if colored output is enabled.

    Returns:
        True if colors should be used
    """
    ctx = click.get_current_context()
    return not ctx.obj.get('no_color', False) if ctx.obj else True


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: Message to print
    """
    if not is_quiet():
        if use_color():
            console.print(f"[green]✓[/green] {message}")
        else:
            console.print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: Error message to print
    """
    if use_color():
        error_console.print(f"[red]✗[/red] {message}")
    else:
        error_console.print(f"✗ {message}")


def print_info(message: str) -> None:
    """Print an info message.

    Args:
        message: Info message to print
    """
    if not is_quiet():
        if use_color():
            console.print(f"[blue]ℹ[/blue] {message}")
        else:
            console.print(f"ℹ {message}")


def print_verbose(message: str) -> None:
    """Print a verbose debug message.

    Args:
        message: Debug message to print
    """
    if is_verbose():
        if use_color():
            console.print(f"[dim]{message}[/dim]")
        else:
            console.print(message)


def confirm_action(message: str, default: bool = False) -> bool:
    """Prompt user for confirmation.

    Args:
        message: Confirmation message
        default: Default value if user just presses Enter

    Returns:
        True if user confirms
    """
    return click.confirm(message, default=default)
