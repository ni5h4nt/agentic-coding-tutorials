"""View command for notes CLI."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from ..utils import (
    get_notes_dir,
    find_note,
    print_error,
    print_verbose,
    use_color,
)

console = Console()


@click.command()
@click.argument('note', type=str, required=True)
@click.option(
    '--raw', '-r',
    is_flag=True,
    help='Display raw markdown without rendering'
)
@click.option(
    '--pager/--no-pager', '-p/',
    default=True,
    help='Use pager for long content'
)
@click.pass_context
def view(ctx: click.Context, note: str, raw: bool, pager: bool) -> None:
    """View/read a note in the terminal.

    Display the content of a note. Notes can be referenced by title or ID.
    By default, markdown is rendered with syntax highlighting.

    Examples:
        notes-cli view "My First Note"
        notes-cli view 123456
        notes-cli view "Meeting Notes" --raw
        notes-cli view "Long Document" --no-pager
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        print_verbose(f"Searching for note: {note}")

        # Find the note
        note_obj = find_note(notes_dir, note)
        if not note_obj:
            raise click.ClickException(f"Note not found: {note}")

        print_verbose(f"Found note: {note_obj.title} (ID: {note_obj.id})")

        # Prepare output
        output_lines = []

        # Add metadata header
        metadata_text = f"**Title:** {note_obj.title}\n"
        metadata_text += f"**ID:** {note_obj.id}\n"
        if note_obj.tags:
            metadata_text += f"**Tags:** {', '.join(note_obj.tags)}\n"
        metadata_text += f"**Created:** {note_obj.created}\n"
        metadata_text += f"**Modified:** {note_obj.modified}\n"

        if raw:
            # Raw mode: show frontmatter and content as-is
            import frontmatter
            with open(note_obj.filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            if pager:
                click.echo_via_pager(raw_content)
            else:
                console.print(raw_content)
        else:
            # Rendered mode: display with rich formatting
            if use_color():
                # Create panel with metadata
                metadata_panel = Panel(
                    metadata_text,
                    title=f"[bold]{note_obj.title}[/bold]",
                    border_style="blue"
                )

                # Render markdown content
                if note_obj.content.strip():
                    md = Markdown(note_obj.content)
                else:
                    md = "[dim]Empty note[/dim]"

                # Combine output
                if pager:
                    # For pager, we need plain text
                    with console.capture() as capture:
                        console.print(metadata_panel)
                        console.print()
                        console.print(md)
                    click.echo_via_pager(capture.get())
                else:
                    console.print(metadata_panel)
                    console.print()
                    console.print(md)
            else:
                # No color mode
                output = f"{metadata_text}\n{'='*60}\n\n{note_obj.content}"
                if pager:
                    click.echo_via_pager(output)
                else:
                    console.print(output)

    except click.ClickException:
        raise
    except Exception as e:
        print_error(f"Failed to view note: {e}")
        raise click.Abort()
