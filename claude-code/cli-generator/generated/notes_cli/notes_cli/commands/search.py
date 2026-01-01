"""Search command for notes CLI."""

import re

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from ..utils import (
    get_notes_dir,
    load_all_notes,
    parse_tags,
    format_datetime,
    print_verbose,
    use_color,
)

console = Console()


def _highlight_match(text: str, query: str, case_sensitive: bool = False) -> Text:
    """Highlight search query matches in text.

    Args:
        text: Text to highlight
        query: Search query
        case_sensitive: Whether to perform case-sensitive search

    Returns:
        Rich Text object with highlighted matches
    """
    if not use_color():
        return Text(text)

    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.escape(query)

    result = Text()
    last_end = 0

    for match in re.finditer(pattern, text, flags):
        # Add text before match
        result.append(text[last_end:match.start()])
        # Add highlighted match
        result.append(text[match.start():match.end()], style="bold yellow on black")
        last_end = match.end()

    # Add remaining text
    result.append(text[last_end:])
    return result


@click.command()
@click.argument('query', type=str, required=True)
@click.option(
    '--title-only', '-t',
    is_flag=True,
    help='Search only in note titles'
)
@click.option(
    '--content-only', '-c',
    is_flag=True,
    help='Search only in note content'
)
@click.option(
    '--case-sensitive', '-s',
    is_flag=True,
    help='Perform case-sensitive search'
)
@click.option(
    '--tags', '-T',
    type=str,
    default=None,
    help='Filter by tags (comma-separated)'
)
@click.pass_context
def search(ctx: click.Context, query: str, title_only: bool, content_only: bool,
           case_sensitive: bool, tags: str | None) -> None:
    """Search notes by content or title.

    Search through your notes for the specified query. By default, searches
    both titles and content. Results show matching context.

    Examples:
        notes-cli search "todo"
        notes-cli search "python" --title-only
        notes-cli search "meeting" --tags work
        notes-cli search "API" --case-sensitive
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        print_verbose(f"Searching for: {query}")

        # Validate options
        if title_only and content_only:
            raise click.ClickException("Cannot use both --title-only and --content-only")

        # Load all notes
        notes = load_all_notes(notes_dir)

        if not notes:
            console.print("No notes found.")
            return

        print_verbose(f"Loaded {len(notes)} notes")

        # Filter by tags if specified
        if tags:
            filter_tags = set(parse_tags(tags))
            print_verbose(f"Filtering by tags: {filter_tags}")
            notes = [note for note in notes if filter_tags.intersection(note.tags)]
            print_verbose(f"Filtered to {len(notes)} notes")

        # Search notes
        matches = []
        flags = 0 if case_sensitive else re.IGNORECASE

        for note in notes:
            matched = False
            match_context = []

            # Search in title
            if not content_only:
                if re.search(re.escape(query), note.title, flags):
                    matched = True
                    match_context.append(('title', note.title))
                    print_verbose(f"Title match: {note.title}")

            # Search in content
            if not title_only and note.content:
                lines = note.content.split('\n')
                for i, line in enumerate(lines):
                    if re.search(re.escape(query), line, flags):
                        matched = True
                        # Get context (current line and surrounding lines)
                        context_lines = []
                        for j in range(max(0, i-1), min(len(lines), i+2)):
                            context_lines.append(lines[j].strip())
                        context = ' '.join(context_lines)
                        # Truncate if too long
                        if len(context) > 100:
                            context = context[:97] + '...'
                        match_context.append(('content', context))
                        print_verbose(f"Content match: {note.title}")
                        break  # Only show first match per note

            if matched:
                matches.append((note, match_context))

        # Display results
        if not matches:
            console.print(f"No notes found matching '{query}'")
            return

        print_verbose(f"Found {len(matches)} matching notes")

        # Create results table
        table = Table(show_header=True, header_style="bold cyan" if use_color() else "bold")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Title", style="bold")
        table.add_column("Match", style="yellow" if use_color() else None)
        table.add_column("Modified", style="green" if use_color() else None, width=16)

        for note, contexts in matches:
            # Prepare match context display
            match_strs = []
            for match_type, match_text in contexts:
                if match_type == 'title':
                    if use_color():
                        match_strs.append(_highlight_match(match_text, query, case_sensitive))
                    else:
                        match_strs.append(match_text)
                else:
                    if use_color():
                        match_strs.append(_highlight_match(match_text, query, case_sensitive))
                    else:
                        match_strs.append(match_text)

            # Display first match context
            match_display = match_strs[0] if match_strs else "-"

            table.add_row(
                str(note.id),
                note.title,
                match_display,
                format_datetime(note.modified)
            )

        console.print(table)
        console.print(f"\n{len(matches)} note(s) found")

    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(f"Search failed: {e}")
