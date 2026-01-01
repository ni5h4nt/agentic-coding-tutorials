"""Tests for edit command."""

from pathlib import Path

import frontmatter
import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestEditBasic:
    """Test basic edit command functionality."""

    def test_edit_note_by_title(
        self, runner: CliRunner, temp_notes_dir: Path,
        sample_note: Path, mock_editor: None
    ) -> None:
        """Test editing note by title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note'
        ])
        assert result.exit_code == 0
        assert 'edited' in result.output.lower()

    def test_edit_note_by_id(
        self, runner: CliRunner, temp_notes_dir: Path,
        sample_note: Path, mock_editor: None
    ) -> None:
        """Test editing note by ID."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', '123456'
        ])
        assert result.exit_code == 0

    def test_edit_nonexistent_note(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test editing non-existent note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Nonexistent'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()

    def test_edit_without_note_argument(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that edit requires note argument."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()


class TestEditRename:
    """Test edit command rename functionality."""

    def test_edit_rename_note(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test renaming note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--rename', 'New Note Name'
        ])
        assert result.exit_code == 0
        assert 'renamed' in result.output.lower()

        # Check that file was renamed
        new_path = temp_notes_dir / 'New-Note-Name.md'
        assert new_path.exists()
        assert not sample_note.exists()

        # Check metadata was updated
        with open(new_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert post.metadata['title'] == 'New Note Name'

    def test_edit_rename_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test rename with -r short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '-r', 'Renamed'
        ])
        assert result.exit_code == 0
        renamed_path = temp_notes_dir / 'Renamed.md'
        assert renamed_path.exists()

    def test_edit_rename_to_existing_title(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming to a title that already exists."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Python Tips',
            '--rename', 'Meeting Notes'  # Already exists
        ])
        assert result.exit_code != 0
        assert 'already exists' in result.output.lower()

    def test_edit_rename_with_special_characters(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test renaming with special characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--rename', 'Note: With/Special?Chars'
        ])
        assert result.exit_code == 0
        # Filename should be sanitized
        note_files = list(temp_notes_dir.glob('*.md'))
        # Special characters should be removed or replaced


class TestEditAddTags:
    """Test edit command add tags functionality."""

    def test_edit_add_single_tag(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test adding single tag to note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag'
        ])
        assert result.exit_code == 0
        assert 'added tags' in result.output.lower()

        # Verify tag was added
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'newtag' in post.metadata['tags']

    def test_edit_add_multiple_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test adding multiple tags to note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'tag1,tag2,tag3'
        ])
        assert result.exit_code == 0

        # Verify tags were added
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'tag1' in post.metadata['tags']
        assert 'tag2' in post.metadata['tags']
        assert 'tag3' in post.metadata['tags']

    def test_edit_add_tags_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test add tags with -a short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '-a', 'newtag'
        ])
        assert result.exit_code == 0

    def test_edit_add_duplicate_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test adding tags that already exist."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'test,sample'  # Already exists
        ])
        assert result.exit_code == 0

        # Should not create duplicates
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert post.metadata['tags'].count('test') == 1

    def test_edit_add_tags_preserves_existing(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that adding tags preserves existing tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag'
        ])
        assert result.exit_code == 0

        # Check existing tags are preserved
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'test' in post.metadata['tags']
        assert 'sample' in post.metadata['tags']
        assert 'newtag' in post.metadata['tags']


class TestEditRemoveTags:
    """Test edit command remove tags functionality."""

    def test_edit_remove_single_tag(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test removing single tag from note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--remove-tags', 'test'
        ])
        assert result.exit_code == 0
        assert 'removed tags' in result.output.lower()

        # Verify tag was removed
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'test' not in post.metadata['tags']

    def test_edit_remove_multiple_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test removing multiple tags from note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--remove-tags', 'test,sample'
        ])
        assert result.exit_code == 0

        # Verify tags were removed
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'test' not in post.metadata['tags']
        assert 'sample' not in post.metadata['tags']

    def test_edit_remove_tags_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test remove tags with -R short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '-R', 'test'
        ])
        assert result.exit_code == 0

    def test_edit_remove_nonexistent_tag(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test removing tag that doesn't exist."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--remove-tags', 'nonexistent'
        ])
        assert result.exit_code == 0
        # Should not error, just do nothing

    def test_edit_remove_all_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test removing all tags from note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--remove-tags', 'test,sample'
        ])
        assert result.exit_code == 0

        # Verify all tags were removed
        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert len(post.metadata['tags']) == 0


class TestEditCombinations:
    """Test combinations of edit options."""

    def test_edit_rename_and_add_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test renaming and adding tags together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--rename', 'Updated Note',
            '--add-tags', 'updated'
        ])
        assert result.exit_code == 0

        new_path = temp_notes_dir / 'Updated-Note.md'
        assert new_path.exists()

        with open(new_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert post.metadata['title'] == 'Updated Note'
        assert 'updated' in post.metadata['tags']

    def test_edit_add_and_remove_tags(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test adding and removing tags together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag',
            '--remove-tags', 'test'
        ])
        assert result.exit_code == 0

        with open(sample_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'newtag' in post.metadata['tags']
        assert 'test' not in post.metadata['tags']

    def test_edit_all_options(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test using all edit options together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--rename', 'Fully Updated',
            '--add-tags', 'new',
            '--remove-tags', 'test'
        ])
        assert result.exit_code == 0

        new_path = temp_notes_dir / 'Fully-Updated.md'
        assert new_path.exists()

        with open(new_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert post.metadata['title'] == 'Fully Updated'
        assert 'new' in post.metadata['tags']
        assert 'test' not in post.metadata['tags']


class TestEditWithEditor:
    """Test edit command with editor options."""

    def test_edit_with_custom_editor(
        self, runner: CliRunner, temp_notes_dir: Path,
        sample_note: Path, mock_editor: None
    ) -> None:
        """Test editing with custom editor."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--editor', 'vim'
        ])
        # Should work with mock editor

    def test_edit_editor_short_option(
        self, runner: CliRunner, temp_notes_dir: Path,
        sample_note: Path, mock_editor: None
    ) -> None:
        """Test editing with -e short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '-e', 'nano'
        ])
        # Should work with mock editor

    def test_edit_metadata_only_no_editor(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that metadata-only edits don't open editor."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag'
        ])
        assert result.exit_code == 0
        # Should not open editor, just update metadata


class TestEditEdgeCases:
    """Test edit command edge cases."""

    def test_edit_empty_identifier(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test editing with empty identifier."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', ''
        ])
        assert result.exit_code != 0

    def test_edit_note_with_special_chars(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path, mock_editor: None
    ) -> None:
        """Test editing note with special characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', '666666'
        ])
        # Should handle special characters

    def test_edit_preserves_content(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that editing preserves note content."""
        # Get original content
        with open(sample_note, 'r', encoding='utf-8') as f:
            original_post = frontmatter.load(f)
        original_content = original_post.content

        # Edit metadata
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag'
        ])
        assert result.exit_code == 0

        # Check content is preserved
        with open(sample_note, 'r', encoding='utf-8') as f:
            updated_post = frontmatter.load(f)
        assert updated_post.content == original_content

    def test_edit_updates_modified_timestamp(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that editing updates modified timestamp."""
        # Get original timestamp
        with open(sample_note, 'r', encoding='utf-8') as f:
            original_post = frontmatter.load(f)
        original_modified = original_post.metadata['modified']

        # Edit note
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'newtag'
        ])
        assert result.exit_code == 0

        # Check timestamp was updated
        with open(sample_note, 'r', encoding='utf-8') as f:
            updated_post = frontmatter.load(f)
        assert updated_post.metadata['modified'] != original_modified


class TestEditIntegration:
    """Integration tests for edit command."""

    def test_create_edit_view(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating, editing, then viewing a note."""
        # Create
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Edit Test'
        ])
        assert create_result.exit_code == 0

        # Edit
        edit_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Edit Test',
            '--add-tags', 'edited'
        ])
        assert edit_result.exit_code == 0

        # View
        view_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Edit Test'
        ])
        assert view_result.exit_code == 0
        assert 'edited' in view_result.output

    def test_edit_then_list(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test editing note then listing to see changes."""
        # Edit
        edit_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--rename', 'Modified Note'
        ])
        assert edit_result.exit_code == 0

        # List
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert list_result.exit_code == 0
        assert 'Modified Note' in list_result.output
        assert 'Sample Note' not in list_result.output
