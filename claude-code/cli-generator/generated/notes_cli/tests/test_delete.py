"""Tests for delete command."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestDeleteBasic:
    """Test basic delete command functionality."""

    def test_delete_note_by_title(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting note by title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force'  # Skip confirmation
        ])
        assert result.exit_code == 0
        assert 'deleted' in result.output.lower()
        assert not sample_note.exists()

    def test_delete_note_by_id(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting note by ID."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '123456',
            '--force'
        ])
        assert result.exit_code == 0
        assert not sample_note.exists()

    def test_delete_nonexistent_note(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test deleting non-existent note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Nonexistent',
            '--force'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()

    def test_delete_without_note_argument(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test that delete requires note argument."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()


class TestDeleteMultiple:
    """Test deleting multiple notes."""

    def test_delete_multiple_notes_by_comma(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test deleting multiple notes with comma-separated identifiers."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Python Tips,Shopping List',
            '--force'
        ])
        assert result.exit_code == 0
        assert '2 note' in result.output

    def test_delete_multiple_by_ids(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test deleting multiple notes by IDs."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '111111,222222',
            '--force'
        ])
        assert result.exit_code == 0

    def test_delete_mixed_valid_invalid(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test deleting with mix of valid and invalid identifiers."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Python Tips,Nonexistent,Shopping List',
            '--force'
        ])
        # Should delete valid ones and report invalid ones
        assert 'not found' in result.output.lower()


class TestDeleteConfirmation:
    """Test delete confirmation prompt."""

    def test_delete_with_confirmation_yes(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting with user confirmation (yes)."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note'
        ], input='y\n')
        assert result.exit_code == 0
        assert not sample_note.exists()

    def test_delete_with_confirmation_no(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting with user confirmation (no)."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note'
        ], input='n\n')
        # Deletion should be cancelled
        assert 'cancel' in result.output.lower()
        assert sample_note.exists()

    def test_delete_with_force_flag(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting with --force flag skips confirmation."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force'
        ])
        assert result.exit_code == 0
        assert not sample_note.exists()

    def test_delete_force_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting with -f short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '-f'
        ])
        assert result.exit_code == 0
        assert not sample_note.exists()


class TestDeleteBackup:
    """Test delete backup functionality."""

    def test_delete_with_backup_default(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that backup is created by default."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force'
        ])
        assert result.exit_code == 0
        assert 'backup' in result.output.lower()

        # Check backup directory exists
        backup_dir = temp_notes_dir / '.backups'
        assert backup_dir.exists()

    def test_delete_without_backup(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test deleting without creating backup."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force',
            '--no-backup'
        ])
        assert result.exit_code == 0
        assert not sample_note.exists()

    def test_delete_backup_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test backup with -b short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force',
            '-b'
        ])
        assert result.exit_code == 0

    def test_delete_backup_contains_note(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test that backup directory contains the deleted note."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force',
            '--backup'
        ])
        assert result.exit_code == 0

        # Check backup file exists
        backup_dir = temp_notes_dir / '.backups'
        backup_files = list(backup_dir.glob('**/*.md'))
        assert len(backup_files) > 0


class TestDeleteEdgeCases:
    """Test delete command edge cases."""

    def test_delete_empty_string(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test deleting with empty string identifier."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '',
            '--force'
        ])
        assert result.exit_code != 0

    def test_delete_whitespace_identifier(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test deleting with whitespace identifier."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '   ',
            '--force'
        ])
        assert result.exit_code != 0

    def test_delete_with_special_characters(
        self, runner: CliRunner, temp_notes_dir: Path,
        note_with_special_chars: Path
    ) -> None:
        """Test deleting note with special characters in title."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '666666',  # Use ID to avoid matching issues
            '--force'
        ])
        assert result.exit_code == 0

    def test_delete_from_empty_directory(
        self, runner: CliRunner, empty_notes_dir: Path
    ) -> None:
        """Test deleting from empty directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(empty_notes_dir),
            'delete', 'anything',
            '--force'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()

    def test_delete_all_notes_in_directory(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test deleting all notes in directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', '111111,222222,333333,444444,555555',
            '--force'
        ])
        assert result.exit_code == 0
        # All notes should be deleted
        remaining_notes = list(temp_notes_dir.glob('*.md'))
        assert len(remaining_notes) == 0


class TestDeleteOutput:
    """Test delete command output."""

    def test_delete_with_verbose(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test delete with verbose flag."""
        result = runner.invoke(cli, [
            '--verbose',
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Sample Note',
            '--force'
        ])
        assert result.exit_code == 0
        # May show additional debug information

    def test_delete_shows_summary(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that delete shows summary before confirmation."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Python Tips,Shopping List'
        ], input='n\n')
        # Should show list of notes to be deleted
        assert 'Python Tips' in result.output
        assert 'Shopping List' in result.output


class TestDeleteIntegration:
    """Integration tests for delete command."""

    def test_create_then_delete(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test creating a note then deleting it."""
        # Create note
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Delete Test'
        ])
        assert create_result.exit_code == 0

        # Delete note
        delete_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Delete Test',
            '--force'
        ])
        assert delete_result.exit_code == 0

        # Verify it's gone
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert 'Delete Test' not in list_result.output

    def test_delete_then_list(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test deleting notes then listing remaining ones."""
        # Delete some notes
        delete_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'delete', 'Python Tips,Shopping List',
            '--force'
        ])
        assert delete_result.exit_code == 0

        # List remaining notes
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list'
        ])
        assert list_result.exit_code == 0
        assert 'Python Tips' not in list_result.output
        assert 'Shopping List' not in list_result.output
        assert 'Meeting Notes' in list_result.output  # Should still exist
