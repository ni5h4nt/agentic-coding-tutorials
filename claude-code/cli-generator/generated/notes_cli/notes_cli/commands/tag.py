"""Tag command for notes CLI."""

from collections import Counter

import click
from rich.console import Console
from rich.table import Table

from ..utils import (
    get_notes_dir,
    load_all_notes,
    print_success,
    print_error,
    print_verbose,
    print_info,
    confirm_action,
    use_color,
)

console = Console()


@click.command()
@click.argument('action', type=click.Choice(['list', 'rename', 'merge']), required=True)
@click.option(
    '--old-tag', '-o',
    type=str,
    default=None,
    help='Old tag name (for rename/merge)'
)
@click.option(
    '--new-tag', '-n',
    type=str,
    default=None,
    help='New tag name (for rename/merge)'
)
@click.option(
    '--count', '-c',
    is_flag=True,
    help='Show note count for each tag'
)
@click.pass_context
def tag(ctx: click.Context, action: str, old_tag: str | None, new_tag: str | None, count: bool) -> None:
    """Manage tags across notes.

    List all tags, rename tags across all notes, or merge tags together.

    Examples:
        notes-cli tag list
        notes-cli tag list --count
        notes-cli tag rename --old-tag python --new-tag python3
        notes-cli tag merge --old-tag todo --new-tag tasks
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])

        if action == 'list':
            _list_tags(notes_dir, count)
        elif action == 'rename':
            _rename_tag(notes_dir, old_tag, new_tag)
        elif action == 'merge':
            _merge_tag(notes_dir, old_tag, new_tag)

    except click.ClickException:
        raise
    except Exception as e:
        print_error(f"Tag operation failed: {e}")
        raise click.Abort()


def _list_tags(notes_dir, show_count: bool) -> None:
    """List all tags with optional counts.

    Args:
        notes_dir: Path to notes directory
        show_count: Whether to show note counts
    """
    print_verbose("Loading all notes")
    notes = load_all_notes(notes_dir)

    if not notes:
        console.print("No notes found.")
        return

    # Collect all tags
    tag_counter = Counter()
    for note in notes:
        for tag in note.tags:
            tag_counter[tag] += 1

    if not tag_counter:
        console.print("No tags found.")
        return

    print_verbose(f"Found {len(tag_counter)} unique tags")

    # Display tags
    if show_count:
        table = Table(show_header=True, header_style="bold cyan" if use_color() else "bold")
        table.add_column("Tag", style="yellow" if use_color() else None)
        table.add_column("Count", justify="right", style="blue" if use_color() else None)

        for tag, tag_count in sorted(tag_counter.items()):
            table.add_row(tag, str(tag_count))

        console.print(table)
        console.print(f"\n{len(tag_counter)} tag(s), {sum(tag_counter.values())} total uses")
    else:
        # Simple list
        for tag in sorted(tag_counter.keys()):
            console.print(f"  {tag}")
        console.print(f"\n{len(tag_counter)} tag(s)")


def _rename_tag(notes_dir, old_tag: str | None, new_tag: str | None) -> None:
    """Rename a tag across all notes.

    Args:
        notes_dir: Path to notes directory
        old_tag: Tag to rename
        new_tag: New tag name

    Raises:
        click.ClickException: If required options are missing
    """
    if not old_tag:
        raise click.ClickException("--old-tag is required for rename action")
    if not new_tag:
        raise click.ClickException("--new-tag is required for rename action")

    print_verbose(f"Renaming tag: {old_tag} -> {new_tag}")

    notes = load_all_notes(notes_dir)
    affected_notes = []

    # Find notes with the old tag
    for note in notes:
        if old_tag in note.tags:
            affected_notes.append(note)

    if not affected_notes:
        print_info(f"No notes found with tag '{old_tag}'")
        return

    print_info(f"Found {len(affected_notes)} note(s) with tag '{old_tag}'")

    # Confirm action
    if not confirm_action(f"Rename tag '{old_tag}' to '{new_tag}' in {len(affected_notes)} note(s)?", default=True):
        print_info("Rename cancelled")
        return

    # Rename tag in each note
    updated_count = 0
    for note in affected_notes:
        try:
            tags = note.tags
            # Remove old tag and add new tag
            tags = [new_tag if t == old_tag else t for t in tags]
            # Remove duplicates while preserving order
            seen = set()
            unique_tags = []
            for t in tags:
                if t not in seen:
                    seen.add(t)
                    unique_tags.append(t)

            note.metadata['tags'] = unique_tags
            note.save()
            updated_count += 1
            print_verbose(f"Updated: {note.title}")
        except Exception as e:
            print_error(f"Failed to update {note.title}: {e}")

    if updated_count > 0:
        print_success(f"Renamed tag in {updated_count} note(s)")
    else:
        print_error("No notes were updated")


def _merge_tag(notes_dir, old_tag: str | None, new_tag: str | None) -> None:
    """Merge one tag into another.

    Args:
        notes_dir: Path to notes directory
        old_tag: Tag to merge (will be removed)
        new_tag: Tag to merge into (will be kept)

    Raises:
        click.ClickException: If required options are missing
    """
    if not old_tag:
        raise click.ClickException("--old-tag is required for merge action")
    if not new_tag:
        raise click.ClickException("--new-tag is required for merge action")

    print_verbose(f"Merging tag: {old_tag} -> {new_tag}")

    notes = load_all_notes(notes_dir)
    affected_notes = []

    # Find notes with the old tag
    for note in notes:
        if old_tag in note.tags:
            affected_notes.append(note)

    if not affected_notes:
        print_info(f"No notes found with tag '{old_tag}'")
        return

    print_info(f"Found {len(affected_notes)} note(s) with tag '{old_tag}'")

    # Confirm action
    if not confirm_action(f"Merge tag '{old_tag}' into '{new_tag}' in {len(affected_notes)} note(s)?", default=True):
        print_info("Merge cancelled")
        return

    # Merge tag in each note
    updated_count = 0
    for note in affected_notes:
        try:
            tags = note.tags
            # Remove old tag
            tags = [t for t in tags if t != old_tag]
            # Add new tag if not already present
            if new_tag not in tags:
                tags.append(new_tag)

            note.metadata['tags'] = sorted(tags)
            note.save()
            updated_count += 1
            print_verbose(f"Updated: {note.title}")
        except Exception as e:
            print_error(f"Failed to update {note.title}: {e}")

    if updated_count > 0:
        print_success(f"Merged tag in {updated_count} note(s)")
    else:
        print_error("No notes were updated")
