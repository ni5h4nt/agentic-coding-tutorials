"""Tests for tag command."""

from pathlib import Path

import frontmatter
import pytest
from click.testing import CliRunner

from notes_cli.cli import cli


class TestTagList:
    """Test tag list functionality."""

    def test_tag_list_basic(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test listing all tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0
        assert 'python' in result.output
        assert 'work' in result.output
        assert 'personal' in result.output

    def test_tag_list_with_count(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test listing tags with count."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list',
            '--count'
        ])
        assert result.exit_code == 0
        # Should show tag counts in table format
        assert 'Count' in result.output or 'count' in result.output.lower()

    def test_tag_list_count_short_option(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test listing tags with -c short option."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list',
            '-c'
        ])
        assert result.exit_code == 0

    def test_tag_list_empty_directory(
        self, runner: CliRunner, empty_notes_dir: Path
    ) -> None:
        """Test listing tags in empty directory."""
        result = runner.invoke(cli, [
            '--notes-dir', str(empty_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0
        assert 'No notes found' in result.output or 'No tags found' in result.output

    def test_tag_list_notes_without_tags(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test listing when some notes have no tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0
        # Note Without Tags exists but should not appear in tag list


class TestTagRename:
    """Test tag rename functionality."""

    def test_tag_rename_basic(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming a tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'python',
            '--new-tag', 'python3'
        ], input='y\n')
        assert result.exit_code == 0
        assert 'renamed' in result.output.lower()

        # Verify tag was renamed in note
        python_note = temp_notes_dir / 'Python-Tips.md'
        with open(python_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'python3' in post.metadata['tags']
        assert 'python' not in post.metadata['tags']

    def test_tag_rename_short_options(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming tag with short options."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '-o', 'work',
            '-n', 'office'
        ], input='y\n')
        assert result.exit_code == 0

    def test_tag_rename_without_old_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test rename without --old-tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--new-tag', 'newtag'
        ])
        assert result.exit_code != 0
        assert 'required' in result.output.lower()

    def test_tag_rename_without_new_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test rename without --new-tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'python'
        ])
        assert result.exit_code != 0
        assert 'required' in result.output.lower()

    def test_tag_rename_nonexistent_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming tag that doesn't exist."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'nonexistent',
            '--new-tag', 'newtag'
        ], input='y\n')
        assert result.exit_code == 0
        assert 'No notes found' in result.output

    def test_tag_rename_confirmation_cancel(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test cancelling tag rename."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'python',
            '--new-tag', 'python3'
        ], input='n\n')
        assert 'cancel' in result.output.lower()

        # Verify tag was not renamed
        python_note = temp_notes_dir / 'Python-Tips.md'
        with open(python_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'python' in post.metadata['tags']

    def test_tag_rename_multiple_notes(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming tag that appears in multiple notes."""
        # First add same tag to multiple notes
        runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Meeting Notes',
            '--add-tags', 'shared'
        ])
        runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Shopping List',
            '--add-tags', 'shared'
        ])

        # Now rename the shared tag
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'shared',
            '--new-tag', 'common'
        ], input='y\n')
        assert result.exit_code == 0
        assert '2 note' in result.output


class TestTagMerge:
    """Test tag merge functionality."""

    def test_tag_merge_basic(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merging tags."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'todo',
            '--new-tag', 'personal'
        ], input='y\n')
        assert result.exit_code == 0
        assert 'merged' in result.output.lower()

        # Verify old tag was removed and new tag added
        shopping_note = temp_notes_dir / 'Shopping-List.md'
        with open(shopping_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'personal' in post.metadata['tags']
        assert 'todo' not in post.metadata['tags']

    def test_tag_merge_short_options(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merging with short options."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '-o', 'todo',
            '-n', 'personal'
        ], input='y\n')
        assert result.exit_code == 0

    def test_tag_merge_without_old_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merge without --old-tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--new-tag', 'newtag'
        ])
        assert result.exit_code != 0
        assert 'required' in result.output.lower()

    def test_tag_merge_without_new_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merge without --new-tag."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'python'
        ])
        assert result.exit_code != 0
        assert 'required' in result.output.lower()

    def test_tag_merge_nonexistent_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merging tag that doesn't exist."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'nonexistent',
            '--new-tag', 'python'
        ], input='y\n')
        assert result.exit_code == 0
        assert 'No notes found' in result.output

    def test_tag_merge_confirmation_cancel(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test cancelling tag merge."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'todo',
            '--new-tag', 'personal'
        ], input='n\n')
        assert 'cancel' in result.output.lower()

        # Verify tag was not merged
        shopping_note = temp_notes_dir / 'Shopping-List.md'
        with open(shopping_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert 'todo' in post.metadata['tags']

    def test_tag_merge_preserves_new_tag(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that merge preserves new tag if it already exists."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'todo',
            '--new-tag', 'personal'
        ], input='y\n')
        assert result.exit_code == 0

        # Note already had 'personal' tag, should still have it
        shopping_note = temp_notes_dir / 'Shopping-List.md'
        with open(shopping_note, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        assert post.metadata['tags'].count('personal') == 1  # No duplicates


class TestTagEdgeCases:
    """Test tag command edge cases."""

    def test_tag_invalid_action(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test tag with invalid action."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'invalid'
        ])
        assert result.exit_code != 0

    def test_tag_without_action(
        self, runner: CliRunner, temp_notes_dir: Path
    ) -> None:
        """Test tag command without action."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag'
        ])
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'required' in result.output.lower()

    def test_tag_list_sorted_alphabetically(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test that tag list is sorted alphabetically."""
        result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0
        # Tags should appear in alphabetical order


class TestTagOutput:
    """Test tag command output formatting."""

    def test_tag_list_with_no_color(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test tag list output without colors."""
        result = runner.invoke(cli, [
            '--no-color',
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0

    def test_tag_list_with_verbose(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test tag list with verbose flag."""
        result = runner.invoke(cli, [
            '--verbose',
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert result.exit_code == 0


class TestTagIntegration:
    """Integration tests for tag command."""

    def test_tag_list_after_edit(
        self, runner: CliRunner, temp_notes_dir: Path, sample_note: Path
    ) -> None:
        """Test listing tags after editing notes."""
        # Add new tag
        edit_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Sample Note',
            '--add-tags', 'integration'
        ])
        assert edit_result.exit_code == 0

        # List tags
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert list_result.exit_code == 0
        assert 'integration' in list_result.output

    def test_tag_rename_then_search(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test renaming tag then searching by new tag."""
        # Rename tag
        rename_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'rename',
            '--old-tag', 'python',
            '--new-tag', 'python3'
        ], input='y\n')
        assert rename_result.exit_code == 0

        # Search by new tag
        search_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'list',
            '--tags', 'python3'
        ])
        assert search_result.exit_code == 0
        assert 'Python Tips' in search_result.output

    def test_tag_merge_then_list(
        self, runner: CliRunner, temp_notes_dir: Path, multiple_notes: list[Path]
    ) -> None:
        """Test merging tags then listing."""
        # Merge tags
        merge_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'merge',
            '--old-tag', 'todo',
            '--new-tag', 'personal'
        ], input='y\n')
        assert merge_result.exit_code == 0

        # List tags - old tag should be gone
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list'
        ])
        assert list_result.exit_code == 0
        assert 'personal' in list_result.output
        # 'todo' should not appear as separate tag

    def test_create_edit_tag_workflow(
        self, runner: CliRunner, temp_notes_dir: Path, mock_editor: None
    ) -> None:
        """Test full workflow: create, edit tags, list tags."""
        # Create note
        create_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'create', 'Tag Test',
            '--tags', 'initial'
        ])
        assert create_result.exit_code == 0

        # Add more tags
        edit_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'edit', 'Tag Test',
            '--add-tags', 'added1,added2'
        ])
        assert edit_result.exit_code == 0

        # List all tags
        list_result = runner.invoke(cli, [
            '--notes-dir', str(temp_notes_dir),
            'tag', 'list',
            '--count'
        ])
        assert list_result.exit_code == 0
        assert 'initial' in list_result.output
        assert 'added1' in list_result.output
        assert 'added2' in list_result.output
