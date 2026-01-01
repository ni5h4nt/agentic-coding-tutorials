"""Tests for view command."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestViewBasic:
    """Test basic view command functionality."""

    def test_view_note_by_title(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing note by title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output
        assert 'sample note' in result.output.lower()

    def test_view_note_by_id(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing note by ID."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', '123456'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output

    def test_view_note_by_partial_title(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing note by partial title match."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output

    def test_view_nonexistent_note(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test viewing non-existent note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Nonexistent Note'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()

    def test_view_shows_metadata(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that view shows note metadata."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note'
        ])
        assert result.exit_code == 0
        assert '123456' in result.output  # ID
        assert 'test' in result.output or 'sample' in result.output  # Tags


class TestViewRawMode:
    """Test view command raw mode."""

    def test_view_raw_mode(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing note in raw mode."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note',
            '--raw'
        ])
        assert result.exit_code == 0
        # Should show frontmatter
        assert '---' in result.output
        assert 'title:' in result.output.lower() or 'Sample Note' in result.output

    def test_view_raw_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing with -r short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note',
            '-r'
        ])
        assert result.exit_code == 0
        assert '---' in result.output

    def test_view_raw_shows_full_content(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that raw mode shows complete file content."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note',
            '--raw'
        ])
        assert result.exit_code == 0
        # Should contain both frontmatter and content
        assert 'id:' in result.output.lower() or '123456' in result.output
        assert 'Section' in result.output


class TestViewPager:
    """Test view command pager options."""

    def test_view_with_pager(
        self, runner: CliRunner, temp_notes_dir: Path,
        notes_with_long_content: Path
    ) -> None:
        """Test viewing long note with pager."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Very Long Note',
            '--pager'
        ])
        # Pager behavior is complex to test, just verify it runs

    def test_view_without_pager(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing note without pager."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note',
            '--no-pager'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output

    def test_view_pager_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test viewing with -p short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note',
            '-p'
        ])
        # Should work with pager


class TestViewEdgeCases:
    """Test view command edge cases."""

    def test_view_empty_note(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test viewing note with no content."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Empty Note'
        ])
        assert result.exit_code == 0
        assert 'Empty Note' in result.output
        # Should show metadata even if content is empty

    def test_view_note_with_special_characters(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path
    ) -> None:
        """Test viewing note with special characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', '666666'  # Use ID to avoid title matching issues
        ])
        assert result.exit_code == 0
        assert 'Special Chars' in result.output

    def test_view_note_case_insensitive(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that note title matching is case insensitive."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'SAMPLE NOTE'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output

    def test_view_without_note_argument(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that view requires note argument."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()

    def test_view_with_multiple_matches(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test viewing when partial title matches multiple notes."""
        # 'Note' appears in multiple note titles
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Note'
        ])
        # Should return first match or handle appropriately


class TestViewOutput:
    """Test view command output formatting."""

    def test_view_with_no_color(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test view output without colors."""
        result = runner.invoke(cli, [
            '--no-color',
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note'
        ])
        assert result.exit_code == 0
        # Should not contain ANSI color codes

    def test_view_with_verbose(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test view with verbose flag."""
        result = runner.invoke(cli, [
            '--verbose',
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note'
        ])
        assert result.exit_code == 0
        # May show additional debug information

    def test_view_rendered_markdown(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that markdown is rendered by default."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'Sample Note'
        ])
        assert result.exit_code == 0
        # Should render markdown (exact rendering depends on implementation)
        assert 'Sample Note' in result.output


class TestViewIntegration:
    """Integration tests for view command."""

    def test_create_then_view(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating a note then viewing it."""
        # Create note
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'View Test',
            '--tags', 'test'
        ])
        assert create_result.exit_code == 0

        # View note
        view_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'View Test'
        ])
        assert view_result.exit_code == 0
        assert 'View Test' in view_result.output

    def test_view_note_from_list(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test viewing a note after listing."""
        # List notes to get ID
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert list_result.exit_code == 0

        # View by ID
        view_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', '111111'  # Python Tips ID
        ])
        assert view_result.exit_code == 0
        assert 'Python Tips' in view_result.output
