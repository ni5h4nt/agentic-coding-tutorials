"""Tests for create command."""

from pathlib import Path

import frontmatter
import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestCreateBasic:
    """Test basic create command functionality."""

    def test_create_note_basic(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating a basic note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Test Note'
        ])
        assert result.exit_code == 0
        assert 'created' in result.output.lower()

        # Check that file was created
        note_files = list(temp_notes_dir.glob('*.md'))
        assert len(note_files) == 1
        assert note_files[0].name == 'Test-Note.md'

    def test_create_note_with_spaces(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with spaces in title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'My First Note'
        ])
        assert result.exit_code == 0

        # Check filename is sanitized
        note_files = list(temp_notes_dir.glob('*.md'))
        assert len(note_files) == 1
        assert note_files[0].name == 'My-First-Note.md'

    def test_create_note_metadata(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test that created note has correct metadata."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Metadata Test'
        ])
        assert result.exit_code == 0

        # Load the created note
        note_path = temp_notes_dir / 'Metadata-Test.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        assert post.metadata['title'] == 'Metadata Test'
        assert 'id' in post.metadata
        assert 'created' in post.metadata
        assert 'modified' in post.metadata
        assert isinstance(post.metadata['tags'], list)


class TestCreateWithTags:
    """Test create command with tags."""

    def test_create_with_single_tag(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with single tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Tagged Note',
            '--tags', 'python'
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Tagged-Note.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        assert 'python' in post.metadata['tags']

    def test_create_with_multiple_tags(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with multiple tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Multi Tag Note',
            '--tags', 'python,programming,tutorial'
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Multi-Tag-Note.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        assert 'python' in post.metadata['tags']
        assert 'programming' in post.metadata['tags']
        assert 'tutorial' in post.metadata['tags']

    def test_create_with_tags_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with -t short option for tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Short Option',
            '-t', 'test'
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Short-Option.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        assert 'test' in post.metadata['tags']

    def test_create_with_tags_with_spaces(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with tags that have spaces."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Spaced Tags',
            '--tags', 'tag one, tag two, tag three'
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Spaced-Tags.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        assert 'tag one' in post.metadata['tags']
        assert 'tag two' in post.metadata['tags']
        assert 'tag three' in post.metadata['tags']


class TestCreateWithTemplate:
    """Test create command with templates."""

    def test_create_with_template(
        self, runner: CliRunner, temp_notes_dir: Path,
        template_file: Path, mock_editor: None
    ) -> None:
        """Test creating note from template."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Templated Note',
            '--template', str(template_file)
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Templated-Note.md'
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Template content should be in the note
        assert 'Template' in post.content

    def test_create_with_nonexistent_template(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with non-existent template fails."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Bad Template',
            '--template', '/nonexistent/template.md'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()

    def test_create_with_template_short_option(
        self, runner: CliRunner, temp_notes_dir: Path,
        template_file: Path, mock_editor: None
    ) -> None:
        """Test creating note with -T short option for template."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Short Template',
            '-T', str(template_file)
        ])
        assert result.exit_code == 0

        note_path = temp_notes_dir / 'Short-Template.md'
        assert note_path.exists()


class TestCreateEdgeCases:
    """Test create command edge cases."""

    def test_create_duplicate_note(
        self, runner: CliRunner, temp_notes_dir: Path,
        sample_note: Path, mock_editor: None
    ) -> None:
        """Test creating note with existing title fails."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Sample Note'
        ])
        assert result.exit_code != 0
        assert 'already exists' in result.output.lower()

    def test_create_note_with_special_characters(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with special characters in title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Note: With Special/Chars?'
        ])
        assert result.exit_code == 0

        # Check that filename is sanitized (special chars removed)
        note_files = list(temp_notes_dir.glob('*.md'))
        assert len(note_files) == 1
        # Special characters should be removed or replaced
        assert ':' not in note_files[0].name
        assert '/' not in note_files[0].name
        assert '?' not in note_files[0].name

    def test_create_note_with_unicode(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with unicode characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', '你好 World 🌍'
        ])
        # Should handle unicode gracefully

    def test_create_empty_title(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with empty title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', ''
        ])
        # Should either fail or create with default title

    def test_create_very_long_title(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with very long title."""
        long_title = 'A' * 200  # 200 character title
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', long_title
        ])
        assert result.exit_code == 0

        # Filename should be truncated
        note_files = list(temp_notes_dir.glob('*.md'))
        assert len(note_files) == 1
        # Should be limited to reasonable length (100 chars in implementation)
        assert len(note_files[0].stem) <= 100

    def test_create_note_without_title(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that create command requires title argument."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()


class TestCreateWithEditor:
    """Test create command with editor options."""

    def test_create_with_custom_editor(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with custom editor."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Custom Editor',
            '--editor', 'vim'
        ])
        # Should work with mock editor

    def test_create_with_editor_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note with -e short option for editor."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Short Editor',
            '-e', 'nano'
        ])
        # Should work with mock editor


class TestCreateIntegration:
    """Integration tests for create command."""

    def test_create_then_list(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating note then listing it."""
        # Create note
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Integration Test'
        ])
        assert create_result.exit_code == 0

        # List notes
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert list_result.exit_code == 0
        assert 'Integration Test' in list_result.output

    def test_create_multiple_notes(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating multiple notes."""
        titles = ['Note One', 'Note Two', 'Note Three']

        for title in titles:
            result = runner.invoke(cli, [
                '--notes-dir', str(temp_notes_dir),
                'create', title
            ])
            assert result.exit_code == 0

        # Verify all notes exist
        note_files = list(temp_notes_dir.glob('*.md'))
        assert len(note_files) == 3
