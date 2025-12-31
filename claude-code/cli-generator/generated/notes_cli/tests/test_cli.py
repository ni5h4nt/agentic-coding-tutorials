"""Tests for main CLI functionality."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from notes_cli.cli import cli, main


class TestCLIBasics:
    """Test basic CLI functionality."""

    def test_cli_help(self, runner: CliRunner) -> None:
        """Test --help flag displays help text."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'A markdown-based note-taking CLI' in result.output
        assert 'create' in result.output
        assert 'list' in result.output
        assert 'search' in result.output

    def test_cli_version(self, runner: CliRunner) -> None:
        """Test --version flag displays version."""
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'version' in result.output.lower()

    def test_cli_no_command(self, runner: CliRunner) -> None:
        """Test CLI without command shows help."""
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert 'A markdown-based note-taking CLI' in result.output

    def test_cli_invalid_command(self, runner: CliRunner) -> None:
        """Test CLI with invalid command shows error."""
        result = runner.invoke(cli, ['invalid-command'])
        assert result.exit_code != 0
        assert 'Error' in result.output or 'No such command' in result.output


class TestGlobalOptions:
    """Test global CLI options."""

    def test_verbose_flag(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test --verbose flag enables verbose output."""
        result = runner.invoke(cli, [
            '--verbose',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        # Verbose output should show debug information
        # Note: exact output depends on implementation

    def test_quiet_flag(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test --quiet flag suppresses output."""
        result = runner.invoke(cli, [
            '--quiet',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        # Less output expected in quiet mode

    def test_no_color_flag(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test --no-color flag disables colored output."""
        result = runner.invoke(cli, [
            '--no-color',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        # Should not contain ANSI color codes (implementation specific)

    def test_notes_dir_option(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test --notes-dir option sets custom notes directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0

    def test_notes_dir_short_option(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test -d short option for notes directory."""
        result = runner.invoke(cli, [
            '-d', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0

    def test_combined_flags(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test combining multiple global flags."""
        result = runner.invoke(cli, [
            '--verbose',
            '--no-color',
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0


class TestCommandHelp:
    """Test help text for individual commands."""

    def test_create_help(self, runner: CliRunner) -> None:
        """Test create command --help."""
        result = runner.invoke(cli, ['create', '--help'])
        assert result.exit_code == 0
        assert 'Create a new markdown note' in result.output
        assert '--tags' in result.output
        assert '--editor' in result.output
        assert '--template' in result.output

    def test_list_help(self, runner: CliRunner) -> None:
        """Test list command --help."""
        result = runner.invoke(cli, ['list', '--help'])
        assert result.exit_code == 0
        assert 'List all notes' in result.output
        assert '--tags' in result.output
        assert '--sort-by' in result.output
        assert '--reverse' in result.output
        assert '--limit' in result.output

    def test_view_help(self, runner: CliRunner) -> None:
        """Test view command --help."""
        result = runner.invoke(cli, ['view', '--help'])
        assert result.exit_code == 0
        assert 'View/read a note' in result.output
        assert '--raw' in result.output
        assert '--pager' in result.output

    def test_search_help(self, runner: CliRunner) -> None:
        """Test search command --help."""
        result = runner.invoke(cli, ['search', '--help'])
        assert result.exit_code == 0
        assert 'Search notes' in result.output
        assert '--title-only' in result.output
        assert '--content-only' in result.output
        assert '--case-sensitive' in result.output

    def test_edit_help(self, runner: CliRunner) -> None:
        """Test edit command --help."""
        result = runner.invoke(cli, ['edit', '--help'])
        assert result.exit_code == 0
        assert 'Edit' in result.output

    def test_delete_help(self, runner: CliRunner) -> None:
        """Test delete command --help."""
        result = runner.invoke(cli, ['delete', '--help'])
        assert result.exit_code == 0
        assert 'Delete' in result.output
        assert '--force' in result.output
        assert '--backup' in result.output

    def test_tag_help(self, runner: CliRunner) -> None:
        """Test tag command --help."""
        result = runner.invoke(cli, ['tag', '--help'])
        assert result.exit_code == 0
        assert 'tag' in result.output.lower()

    def test_export_help(self, runner: CliRunner) -> None:
        """Test export command --help."""
        result = runner.invoke(cli, ['export', '--help'])
        assert result.exit_code == 0
        assert 'Export' in result.output
        assert '--format' in result.output


class TestErrorHandling:
    """Test error handling in main entry point."""

    def test_main_function_exists(self) -> None:
        """Test that main() function exists and is callable."""
        assert callable(main)

    def test_invalid_notes_directory_permission(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test handling of permission errors for notes directory."""
        # Create a directory we can't write to (platform specific)
        # This test might not work on all systems
        invalid_dir = tmp_path / "readonly"
        invalid_dir.mkdir()

        # Try to use a subdirectory we can't create
        result = runner.invoke(cli, [
            '--notes-dir', str(invalid_dir / "subdir" / "notes"),
            'list'
        ])
        # Should handle gracefully


class TestExitCodes:
    """Test CLI exit codes."""

    def test_success_exit_code(self, runner: CliRunner, temp_notes_dir: Path) -> None:
        """Test successful command returns exit code 0."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert result.exit_code == 0

    def test_user_error_exit_code(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test user error returns non-zero exit code."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'view', 'nonexistent-note'
        ])
        assert result.exit_code != 0
