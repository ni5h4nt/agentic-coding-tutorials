"""Shared pytest fixtures for notes CLI tests."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import frontmatter
import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Click test runner.

    Returns:
        CliRunner instance for testing CLI commands
    """
    return CliRunner()


@pytest.fixture
def temp_notes_dir(tmp_path: Path) -> Path:
    """Create a temporary notes directory.

    Args:
        tmp_path: pytest built-in temporary directory fixture

    Returns:
        Path to temporary notes directory
    """
    notes_dir = tmp_path / "test_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    return notes_dir


@pytest.fixture
def sample_note(temp_notes_dir: Path) -> Path:
    """Create a sample note file.

    Args:
        temp_notes_dir: Temporary notes directory

    Returns:
        Path to created note file
    """
    note_path = temp_notes_dir / "Sample-Note.md"
    metadata = {
        'id': 123456,
        'title': 'Sample Note',
        'tags': ['test', 'sample'],
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat()
    }
    content = "This is a sample note.\n\n## Section\n\nSome content here."
    post = frontmatter.Post(content, **metadata)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    return note_path


@pytest.fixture
def multiple_notes(temp_notes_dir: Path) -> list[Path]:
    """Create multiple sample notes for testing.

    Args:
        temp_notes_dir: Temporary notes directory

    Returns:
        List of paths to created note files
    """
    notes_data = [
        {
            'filename': 'Python-Tips.md',
            'id': 111111,
            'title': 'Python Tips',
            'tags': ['python', 'programming'],
            'content': 'Python list comprehensions are powerful.\n\n## Advanced Tips\n\nUse generators for memory efficiency.'
        },
        {
            'filename': 'Meeting-Notes.md',
            'id': 222222,
            'title': 'Meeting Notes',
            'tags': ['work', 'meetings'],
            'content': 'Discussed Q4 planning.\n\n## Action Items\n\n- Review budget\n- Update timeline'
        },
        {
            'filename': 'Shopping-List.md',
            'id': 333333,
            'title': 'Shopping List',
            'tags': ['personal', 'todo'],
            'content': '- Milk\n- Eggs\n- Bread\n- Coffee'
        },
        {
            'filename': 'Note-Without-Tags.md',
            'id': 444444,
            'title': 'Note Without Tags',
            'tags': [],
            'content': 'This note has no tags.'
        },
        {
            'filename': 'Empty-Note.md',
            'id': 555555,
            'title': 'Empty Note',
            'tags': ['empty'],
            'content': ''
        }
    ]

    created_notes = []
    for note_data in notes_data:
        note_path = temp_notes_dir / note_data['filename']
        metadata = {
            'id': note_data['id'],
            'title': note_data['title'],
            'tags': note_data['tags'],
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        post = frontmatter.Post(note_data['content'], **metadata)

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        created_notes.append(note_path)

    return created_notes


@pytest.fixture
def note_with_special_chars(temp_notes_dir: Path) -> Path:
    """Create a note with special characters in title and content.

    Args:
        temp_notes_dir: Temporary notes directory

    Returns:
        Path to created note file
    """
    note_path = temp_notes_dir / "special-chars.md"
    metadata = {
        'id': 666666,
        'title': 'Note with Special Chars: @#$%',
        'tags': ['special', 'test'],
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat()
    }
    content = "Content with special characters: !@#$%^&*()\n\nUnicode: 你好 мир 🚀"
    post = frontmatter.Post(content, **metadata)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    return note_path


@pytest.fixture
def template_file(tmp_path: Path) -> Path:
    """Create a template file for testing.

    Args:
        tmp_path: pytest built-in temporary directory fixture

    Returns:
        Path to template file
    """
    template_path = tmp_path / "template.md"
    content = "# Template\n\n## Section 1\n\nYour content here.\n\n## Section 2\n\nMore content."

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return template_path


@pytest.fixture
def mock_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the editor to prevent actual editor from opening.

    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    def mock_edit(*args: Any, **kwargs: Any) -> str:
        """Mock click.edit function."""
        return "Edited content"

    import click
    monkeypatch.setattr(click, 'edit', mock_edit)


@pytest.fixture
def empty_notes_dir(tmp_path: Path) -> Path:
    """Create an empty notes directory for testing edge cases.

    Args:
        tmp_path: pytest built-in temporary directory fixture

    Returns:
        Path to empty notes directory
    """
    empty_dir = tmp_path / "empty_notes"
    empty_dir.mkdir(parents=True, exist_ok=True)
    return empty_dir


@pytest.fixture
def notes_with_long_content(temp_notes_dir: Path) -> Path:
    """Create a note with long content for pager testing.

    Args:
        temp_notes_dir: Temporary notes directory

    Returns:
        Path to created note file
    """
    note_path = temp_notes_dir / "long-note.md"
    metadata = {
        'id': 777777,
        'title': 'Very Long Note',
        'tags': ['long'],
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat()
    }
    # Create long content (many lines)
    content = "\n".join([f"Line {i}: This is a long line of text." for i in range(100)])
    post = frontmatter.Post(content, **metadata)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    return note_path
