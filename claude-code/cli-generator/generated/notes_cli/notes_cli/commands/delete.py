"""Delete command for notes CLI."""

import shutil
from datetime import datetime
from pathlib import Path

import click

from ..utils import (
    get_notes_dir,
    find_note,
    confirm_action,
    print_success,
    print_error,
    print_verbose,
    print_info,
)


@click.command()
@click.argument('notes', type=str, required=True)
@click.option(
    '--force', '-f',
    is_flag=True,
    help='Skip confirmation prompt'
)
@click.option(
    '--backup/--no-backup', '-b/',
    default=True,
    help='Create backup before deletion'
)
@click.pass_context
def delete(ctx: click.Context, notes: str, force: bool, backup: bool) -> None:
    """Delete one or more notes.

    Delete notes by specifying their titles or IDs. Multiple notes can be
    deleted by separating them with commas. By default, creates backups
    and asks for confirmation.

    Examples:
        notes-cli delete "My First Note"
        notes-cli delete 123456,789012
        notes-cli delete "Old Note" --force
        notes-cli delete "Temp" --no-backup
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])

        # Parse note identifiers
        note_identifiers = [n.strip() for n in notes.split(',') if n.strip()]

        if not note_identifiers:
            raise click.ClickException("No notes specified")

        print_verbose(f"Processing {len(note_identifiers)} note(s) for deletion")

        # Find all notes to delete
        notes_to_delete = []
        not_found = []

        for identifier in note_identifiers:
            note_obj = find_note(notes_dir, identifier)
            if note_obj:
                notes_to_delete.append(note_obj)
                print_verbose(f"Found note: {note_obj.title} (ID: {note_obj.id})")
            else:
                not_found.append(identifier)
                print_verbose(f"Note not found: {identifier}")

        # Report not found notes
        if not_found:
            print_error(f"Notes not found: {', '.join(not_found)}")

        if not notes_to_delete:
            raise click.ClickException("No valid notes to delete")

        # Show summary
        print_info(f"Notes to delete: {len(notes_to_delete)}")
        for note in notes_to_delete:
            print_info(f"  - {note.title} (ID: {note.id})")

        # Confirm deletion
        if not force:
            if not confirm_action(
                f"Delete {len(notes_to_delete)} note(s)?",
                default=False
            ):
                print_info("Deletion cancelled")
                return

        # Create backup directory if needed
        backup_dir = None
        if backup:
            backup_dir = notes_dir / '.backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            print_verbose(f"Backup directory: {backup_dir}")

        # Delete notes
        deleted_count = 0
        for note in notes_to_delete:
            try:
                # Create backup
                if backup and backup_dir:
                    backup_path = backup_dir / note.filepath.name
                    shutil.copy2(note.filepath, backup_path)
                    print_verbose(f"Backed up: {note.filepath.name}")

                # Delete the note
                note.filepath.unlink()
                deleted_count += 1
                print_verbose(f"Deleted: {note.title}")

            except Exception as e:
                print_error(f"Failed to delete {note.title}: {e}")

        # Report results
        if deleted_count > 0:
            print_success(f"Deleted {deleted_count} note(s)")
            if backup and backup_dir:
                print_info(f"Backups saved to: {backup_dir}")
        else:
            print_error("No notes were deleted")
            raise click.Abort()

    except click.ClickException:
        raise
    except click.Abort:
        raise
    except Exception as e:
        print_error(f"Failed to delete notes: {e}")
        raise click.Abort()
