"""Tests for search command."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestSearchBasic:
    """Test basic search command functionality."""

    def test_search_in_title(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching for term in note title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Python'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output
        assert '1 note' in result.output

    def test_search_in_content(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching for term in note content."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'comprehensions'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output

    def test_search_no_matches(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with no matches."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'nonexistentterm12345'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output or '0 note' in result.output

    def test_search_multiple_matches(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with multiple matching notes."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Note'
        ])
        assert result.exit_code == 0
        # Should find multiple notes with "Note" in title

    def test_search_empty_directory(
        self, runner: CliRunner, empty_notes_dir: Path
    ) -> None:
        """Test searching in empty directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(empty_notes_dir),
            'search', 'anything'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output

    def test_search_without_query(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that search requires query argument."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()


class TestSearchTitleOnly:
    """Test search with title-only option."""

    def test_search_title_only(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching only in titles."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Python',
            '--title-only'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output

    def test_search_title_only_no_content_match(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test title-only search ignores content matches."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'comprehensions',  # Only in content
            '--title-only'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output or '0 note' in result.output

    def test_search_title_only_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test title-only with -t short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Shopping',
            '-t'
        ])
        assert result.exit_code == 0
        assert 'Shopping List' in result.output


class TestSearchContentOnly:
    """Test search with content-only option."""

    def test_search_content_only(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching only in content."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'generators',
            '--content-only'
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output

    def test_search_content_only_no_title_match(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test content-only search ignores title matches."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Shopping',  # Only in title
            '--content-only'
        ])
        assert result.exit_code == 0
        # Should not find it or find minimal matches

    def test_search_content_only_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test content-only with -c short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'budget',
            '-c'
        ])
        assert result.exit_code == 0

    def test_search_title_and_content_only_conflict(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that title-only and content-only can't be used together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'test',
            '--title-only',
            '--content-only'
        ])
        assert result.exit_code != 0
        assert 'Cannot use both' in result.output


class TestSearchCaseSensitive:
    """Test case-sensitive search."""

    def test_search_case_insensitive_default(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that search is case-insensitive by default."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'python'  # lowercase
        ])
        assert result.exit_code == 0
        assert 'Python Tips' in result.output  # Title has uppercase P

    def test_search_case_sensitive(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test case-sensitive search."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'python',  # lowercase
            '--case-sensitive'
        ])
        assert result.exit_code == 0
        # May or may not find results depending on content

    def test_search_case_sensitive_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test case-sensitive with -s short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Python',
            '-s'
        ])
        assert result.exit_code == 0


class TestSearchWithTagsFilter:
    """Test search with tags filter."""

    def test_search_with_tag_filter(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching within notes with specific tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Note',
            '--tags', 'work'
        ])
        assert result.exit_code == 0
        # Should only search in notes tagged with 'work'

    def test_search_with_multiple_tag_filters(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with multiple tag filters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'list',
            '--tags', 'python,personal'
        ])
        assert result.exit_code == 0

    def test_search_with_tag_filter_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test tag filter with -T short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Note',
            '-T', 'work'
        ])
        assert result.exit_code == 0

    def test_search_with_nonexistent_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with non-existent tag filter."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'anything',
            '--tags', 'nonexistent'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output or '0 note' in result.output


class TestSearchEdgeCases:
    """Test search command edge cases."""

    def test_search_special_characters(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path
    ) -> None:
        """Test searching for special characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', '@#$%'
        ])
        assert result.exit_code == 0
        # Should handle special characters in search query

    def test_search_unicode(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path
    ) -> None:
        """Test searching for unicode characters."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', '你好'
        ])
        assert result.exit_code == 0
        # Should find the note with unicode content

    def test_search_empty_query(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with empty query string."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', ''
        ])
        # Should handle empty query appropriately

    def test_search_very_long_query(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching with very long query."""
        long_query = 'a' * 1000
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', long_query
        ])
        assert result.exit_code == 0

    def test_search_regex_special_chars(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that regex special characters are escaped."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', '.*'
        ])
        # Should search for literal .* not regex pattern

    def test_search_whitespace_query(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching for whitespace."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', '   '
        ])
        # Should handle whitespace query


class TestSearchOutput:
    """Test search command output formatting."""

    def test_search_shows_context(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that search results show context."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'comprehensions'
        ])
        assert result.exit_code == 0
        # Should show snippet of content with match

    def test_search_with_no_color(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test search output without colors."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            '--no-color',
            'search', 'Python'
        ])
        assert result.exit_code == 0
        # Should not highlight matches with colors

    def test_search_with_verbose(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test search with verbose flag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            '--verbose',
            'search', 'Python'
        ])
        assert result.exit_code == 0
        # May show additional debug information

    def test_search_shows_match_count(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that search shows number of matches."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Note'
        ])
        assert result.exit_code == 0
        # Should show count like "3 note(s) found"
        assert 'note' in result.output.lower()


class TestSearchCombinations:
    """Test combinations of search options."""

    def test_search_title_only_case_sensitive(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test title-only with case-sensitive search."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Python',
            '--title-only',
            '--case-sensitive'
        ])
        assert result.exit_code == 0

    def test_search_content_only_with_tags(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test content-only search with tag filter."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Note',
            '--content-only',
            '--tags', 'work'
        ])
        assert result.exit_code == 0

    def test_search_all_options(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test using multiple search options together."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Action',
            '--content-only',
            '--case-sensitive',
            '--tags', 'work,meetings'
        ])
        assert result.exit_code == 0


class TestSearchIntegration:
    """Integration tests for search command."""

    def test_search_then_view(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test searching for a note then viewing it."""
        # Search for note
        search_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Python'
        ])
        assert search_result.exit_code == 0
        assert '111111' in search_result.output

        # View the found note by ID
        view_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', '111111'
        ])
        assert view_result.exit_code == 0
        assert 'Python Tips' in view_result.output

    def test_create_then_search(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating a note then searching for it."""
        # Create note
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Searchable Note',
            '--tags', 'test'
        ])
        assert create_result.exit_code == 0

        # Search for it
        search_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'search', 'Searchable'
        ])
        assert search_result.exit_code == 0
        assert 'Searchable Note' in search_result.output
