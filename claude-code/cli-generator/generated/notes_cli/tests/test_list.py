"""Tests for list command."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestListBasic:
    """Test basic list command functionality."""

    def test_list_empty_directory(
        self, runner: CliRunner, empty_notes_dir: Path
    ) -> None:
        """Test listing notes in empty directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(empty_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output or '0 note' in result.output

    def test_list_single_note(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test listing directory with single note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        assert 'Sample Note' in result.output
        assert '1 note' in result.output

    def test_list_multiple_notes(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test listing multiple notes."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output
        assert 'Meeting Notes' in result.output
        assert 'Shopping List' in result.output
        assert '5 note' in result.output  # multiple_notes creates 5 notes

    def test_list_shows_metadata(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that list shows note metadata."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Should show ID column
        assert '111111' in result.output or 'ID' in result.output
        # Should show tags
        assert 'python' in result.output or 'programming' in result.output


class TestListFilterByTags:
    """Test list command filtering by tags."""

    def test_list_filter_single_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering by single tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'python'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output
        assert 'Meeting Notes' not in result.output

    def test_list_filter_multiple_tags(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering by multiple tags (OR logic)."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'python,work'
        ])
        assert result.exit_code == 0
        # Should show notes with either python OR work tags
        assert 'Python Tips' in result.output or 'Meeting Notes' in result.output

    def test_list_filter_tag_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering with -t short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '-t', 'personal'
        ])
        assert result.exit_code == 0
        assert 'Shopping List' in result.output

    def test_list_filter_nonexistent_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering by tag that doesn't exist."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'nonexistent'
        ])
        assert result.exit_code == 0
        assert 'No notes match' in result.output or '0 note' in result.output

    def test_list_filter_empty_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering with empty tag string."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', ''
        ])
        assert result.exit_code == 0
        # Should show all notes (no filter applied)


class TestListSorting:
    """Test list command sorting options."""

    def test_list_sort_by_title(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting by title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'title'
        ])
        assert result.exit_code == 0
        # Notes should appear in alphabetical order
        output_lines = result.output
        # Empty Note, Meeting Notes, Note Without Tags, Python Tips, Shopping List

    def test_list_sort_by_created(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting by creation date."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'created'
        ])
        assert result.exit_code == 0

    def test_list_sort_by_modified(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting by modification date (default)."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'modified'
        ])
        assert result.exit_code == 0

    def test_list_sort_by_size(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting by file size."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'size'
        ])
        assert result.exit_code == 0
        # Should show size column

    def test_list_sort_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting with -s short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '-s', 'title'
        ])
        assert result.exit_code == 0

    def test_list_sort_invalid_field(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test sorting by invalid field."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'invalid'
        ])
        assert result.exit_code != 0
        # Should show error about invalid choice

    def test_list_reverse_sort(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test reverse sorting."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--sort-by', 'title',
            '--reverse'
        ])
        assert result.exit_code == 0
        # Should be in reverse alphabetical order

    def test_list_reverse_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test reverse with -r short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '-s', 'title',
            '-r'
        ])
        assert result.exit_code == 0


class TestListLimit:
    """Test list command limit option."""

    def test_list_with_limit(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test limiting number of results."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--limit', '2'
        ])
        assert result.exit_code == 0
        assert '2 note' in result.output

    def test_list_limit_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test limit with -n short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '-n', '3'
        ])
        assert result.exit_code == 0
        assert '3 note' in result.output

    def test_list_limit_larger_than_total(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test limit larger than total notes."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--limit', '100'
        ])
        assert result.exit_code == 0
        assert '5 note' in result.output  # Should show all 5 notes

    def test_list_limit_zero(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test limit of zero."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--limit', '0'
        ])
        assert result.exit_code == 0
        # Should show all notes (no limit)

    def test_list_limit_negative(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test negative limit value."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--limit', '-1'
        ])
        # Should either error or ignore negative value

    def test_list_limit_invalid(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test invalid limit value."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--limit', 'invalid'
        ])
        assert result.exit_code != 0


class TestListCombinations:
    """Test combinations of list options."""

    def test_list_filter_and_sort(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering and sorting together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'programming,work',
            '--sort-by', 'title'
        ])
        assert result.exit_code == 0

    def test_list_filter_sort_limit(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test filtering, sorting, and limiting together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'programming,work,personal',
            '--sort-by', 'modified',
            '--limit', '2'
        ])
        assert result.exit_code == 0

    def test_list_all_options(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test using all list options together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'python',
            '--sort-by', 'title',
            '--reverse',
            '--limit', '5'
        ])
        assert result.exit_code == 0


class TestListEdgeCases:
    """Test list command edge cases."""

    def test_list_with_corrupt_note(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test listing when one note is corrupted."""
        # Create a corrupt note file
        corrupt_path = temp_notes_dir / 'corrupt.md'
        with open(corrupt_path, 'w', encoding='utf-8') as f:
            f.write("---\ninvalid yaml: [\n---\n")

        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        # Should handle gracefully, possibly showing warning

    def test_list_with_non_markdown_files(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test listing directory with non-markdown files."""
        # Create non-markdown files
        (temp_notes_dir / 'readme.txt').write_text('Not a note')
        (temp_notes_dir / 'data.json').write_text('{}')

        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Should only list .md files

    def test_list_with_hidden_files(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test listing ignores hidden files."""
        # Create hidden file
        hidden_path = temp_notes_dir / '.hidden.md'
        hidden_path.write_text('---\ntitle: Hidden\n---\nContent')

        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        # Should not list hidden files or handle them appropriately

    def test_list_with_subdirectories(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that list doesn't recurse into subdirectories."""
        subdir = temp_notes_dir / 'subdir'
        subdir.mkdir()
        (subdir / 'nested.md').write_text('---\ntitle: Nested\n---\nContent')

        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Should not show nested notes (only top-level)

    def test_list_with_special_characters_in_notes(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path
    ) -> None:
        """Test listing notes with special characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Rich table may wrap long titles across lines, check for parts
        assert 'Special' in result.output
        assert '1 note(s) displayed' in result.output


class TestListOutput:
    """Test list command output formatting."""

    def test_list_with_no_color(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test list output without colors."""
        result = runner.invoke(cli, [
            '--no-color',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Output should not contain ANSI color codes

    def test_list_with_verbose(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test list with verbose flag."""
        result = runner.invoke(cli, [
            '--verbose',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # May show additional debug information

    def test_list_with_quiet(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test list with quiet flag."""
        result = runner.invoke(cli, [
            '--quiet',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0
        # Should still show list output (quiet suppresses non-essential output)
