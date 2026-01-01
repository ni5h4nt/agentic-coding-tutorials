"""List command for notes CLI."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..utils import (
    get_notes_dir,
    load_all_notes,
    parse_tags,
    format_datetime,
    format_filesize,
    print_verbose,
    use_color,
)

console = Console()


@click.command('list')
@click.option(
    '--tags', '-t',
    type=str,
    default=None,
    help='Filter by tags (comma-separated)'
)
@click.option(
    '--sort-by', '-s',
    type=click.Choice(['created', 'modified', 'title', 'size']),
    default='modified',
    help='Sort notes by field'
)
@click.option(
    '--reverse', '-r',
    is_flag=True,
    help='Reverse sort order'
)
@click.option(
    '--limit', '-n',
    type=int,
    default=None,
    help='Limit number of notes displayed'
)
@click.pass_context
def list_notes(ctx: click.Context, tags: str | None, sort_by: str, reverse: bool, limit: int | None) -> None:
    """List all notes with optional filtering.

    Display a table of all notes with their metadata. Filter by tags,
    sort by various fields, and limit results.

    Examples:
        notes-cli list
        notes-cli list --tags python,programming
        notes-cli list --sort-by created --reverse
        notes-cli list --limit 10
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        print_verbose(f"Loading notes from: {notes_dir}")

        # Load all notes
        notes = load_all_notes(notes_dir)

        if not notes:
            console.print("No notes found. Create one with: notes-cli create \"My First Note\"")
            return

        print_verbose(f"Loaded {len(notes)} notes")

        # Filter by tags if specified
        if tags:
            filter_tags = set(parse_tags(tags))
            print_verbose(f"Filtering by tags: {filter_tags}")
            notes = [note for note in notes if filter_tags.intersection(note.tags)]
            print_verbose(f"Filtered to {len(notes)} notes")

        if not notes:
            console.print("No notes match the specified filters.")
            return

        # Sort notes
        if sort_by == 'title':
            notes.sort(key=lambda n: n.title.lower(), reverse=reverse)
        elif sort_by == 'created':
            notes.sort(key=lambda n: n.created, reverse=reverse)
        elif sort_by == 'modified':
            notes.sort(key=lambda n: n.modified, reverse=reverse)
        elif sort_by == 'size':
            notes.sort(key=lambda n: n.filepath.stat().st_size, reverse=reverse)

        print_verbose(f"Sorted by {sort_by} (reverse={reverse})")

        # Limit results
        if limit and limit > 0:
            notes = notes[:limit]
            print_verbose(f"Limited to {limit} notes")

        # Create table
        table = Table(show_header=True, header_style="bold cyan" if use_color() else "bold")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Title", style="bold")
        table.add_column("Tags", style="yellow" if use_color() else None)
        table.add_column("Modified", style="green" if use_color() else None)
        table.add_column("Size", justify="right", style="blue" if use_color() else None)

        for note in notes:
            tags_str = ', '.join(note.tags) if note.tags else '-'
            table.add_row(
                str(note.id),
                note.title,
                tags_str,
                format_datetime(note.modified),
                format_filesize(note.filepath)
            )

        console.print(table)
        console.print(f"\n{len(notes)} note(s) displayed")

    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(f"Failed to list notes: {e}")
