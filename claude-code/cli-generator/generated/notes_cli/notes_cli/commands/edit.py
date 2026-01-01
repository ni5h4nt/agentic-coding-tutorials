"""Edit command for notes CLI."""

import click

from ..utils import (
    get_notes_dir,
    find_note,
    sanitize_filename,
    open_in_editor,
    parse_tags,
    print_success,
    print_error,
    print_verbose,
)


@click.command()
@click.argument('note', type=str, required=True)
@click.option(
    '--editor', '-e',
    type=str,
    default=None,
    help='Editor to use (overrides $EDITOR)'
)
@click.option(
    '--rename', '-r',
    type=str,
    default=None,
    help='Rename the note'
)
@click.option(
    '--add-tags', '-a',
    type=str,
    default=None,
    help='Add tags (comma-separated)'
)
@click.option(
    '--remove-tags', '-R',
    type=str,
    default=None,
    help='Remove tags (comma-separated)'
)
@click.pass_context
def edit(ctx: click.Context, note: str, editor: str | None, rename: str | None,
         add_tags: str | None, remove_tags: str | None) -> None:
    """Edit an existing note.

    Opens the specified note in your editor. Can also rename notes and
    modify tags without opening the editor.

    Examples:
        notes-cli edit "My First Note"
        notes-cli edit 123456 --editor vim
        notes-cli edit "Meeting Notes" --rename "Team Meeting Notes"
        notes-cli edit "Python Tips" --add-tags tutorial,advanced
        notes-cli edit "Old Note" --remove-tags outdated
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        print_verbose(f"Searching for note: {note}")

        # Find the note
        note_obj = find_note(notes_dir, note)
        if not note_obj:
            raise click.ClickException(f"Note not found: {note}")

        print_verbose(f"Found note: {note_obj.title} (ID: {note_obj.id})")

        original_filepath = note_obj.filepath
        modified = False

        # Handle rename
        if rename:
            print_verbose(f"Renaming note to: {rename}")
            note_obj.metadata['title'] = rename

            # Create new filename
            new_filename = sanitize_filename(rename) + '.md'
            new_filepath = notes_dir / new_filename

            if new_filepath.exists() and new_filepath != original_filepath:
                raise click.ClickException(f"A note with title '{rename}' already exists")

            modified = True

        # Handle tag additions
        if add_tags:
            new_tags = parse_tags(add_tags)
            print_verbose(f"Adding tags: {new_tags}")

            current_tags = set(note_obj.tags)
            current_tags.update(new_tags)
            note_obj.metadata['tags'] = sorted(list(current_tags))
            modified = True

        # Handle tag removals
        if remove_tags:
            remove_tag_list = parse_tags(remove_tags)
            print_verbose(f"Removing tags: {remove_tag_list}")

            current_tags = set(note_obj.tags)
            current_tags.difference_update(remove_tag_list)
            note_obj.metadata['tags'] = sorted(list(current_tags))
            modified = True

        # Save metadata changes if any
        if modified:
            note_obj.save()
            print_verbose("Saved metadata changes")

            # Handle file rename if title changed
            if rename:
                new_filename = sanitize_filename(rename) + '.md'
                new_filepath = notes_dir / new_filename

                if new_filepath != original_filepath:
                    import shutil
                    shutil.move(str(original_filepath), str(new_filepath))
                    note_obj.filepath = new_filepath
                    print_verbose(f"Renamed file: {original_filepath.name} -> {new_filepath.name}")

            # Print success message for metadata-only changes
            if not (editor or (not rename and not add_tags and not remove_tags)):
                changes = []
                if rename:
                    changes.append(f"renamed to '{rename}'")
                if add_tags:
                    changes.append(f"added tags: {', '.join(parse_tags(add_tags))}")
                if remove_tags:
                    changes.append(f"removed tags: {', '.join(parse_tags(remove_tags))}")

                print_success(f"Note updated: {', '.join(changes)}")

        # Open in editor if no metadata-only options or explicitly requested
        if not (rename or add_tags or remove_tags) or editor:
            print_verbose(f"Opening note in editor: {note_obj.filepath}")
            try:
                open_in_editor(note_obj.filepath, editor)
                print_success(f"Note edited: {note_obj.title}")
            except click.ClickException:
                print_error("Failed to open editor")
                raise click.Abort()

    except click.ClickException:
        raise
    except click.Abort:
        raise
    except Exception as e:
        print_error(f"Failed to edit note: {e}")
        raise click.Abort()
