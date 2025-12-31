"""Export command for notes CLI."""

import json
from pathlib import Path

import click
from rich.console import Console

from ..utils import (
    get_notes_dir,
    load_all_notes,
    parse_tags,
    print_success,
    print_error,
    print_verbose,
    print_info,
)

console = Console()


@click.command()
@click.argument('output', type=click.Path(), required=True)
@click.option(
    '--format', '-f',
    type=click.Choice(['html', 'pdf', 'txt', 'json']),
    default='html',
    help='Export format'
)
@click.option(
    '--tags', '-t',
    type=str,
    default=None,
    help='Filter by tags (comma-separated)'
)
@click.option(
    '--single-file', '-s',
    is_flag=True,
    help='Export all notes to a single file'
)
@click.pass_context
def export(ctx: click.Context, output: str, format: str, tags: str | None, single_file: bool) -> None:
    """Export notes to different formats.

    Export your notes to HTML, PDF, plain text, or JSON format. Can export
    to a single file or multiple files in a directory.

    Examples:
        notes-cli export ./export/notes.html
        notes-cli export ./output --format json
        notes-cli export ./docs --format html --tags python
        notes-cli export ./all.txt --format txt --single-file
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        output_path = Path(output).expanduser().resolve()

        print_verbose(f"Export format: {format}")
        print_verbose(f"Output path: {output_path}")

        # Load notes
        notes = load_all_notes(notes_dir)

        if not notes:
            raise click.ClickException("No notes to export")

        print_verbose(f"Loaded {len(notes)} notes")

        # Filter by tags
        if tags:
            filter_tags = set(parse_tags(tags))
            print_verbose(f"Filtering by tags: {filter_tags}")
            notes = [note for note in notes if filter_tags.intersection(note.tags)]
            print_verbose(f"Filtered to {len(notes)} notes")

        if not notes:
            raise click.ClickException("No notes match the specified filters")

        # Export based on format
        if format == 'json':
            _export_json(notes, output_path, single_file)
        elif format == 'txt':
            _export_txt(notes, output_path, single_file)
        elif format == 'html':
            _export_html(notes, output_path, single_file)
        elif format == 'pdf':
            _export_pdf(notes, output_path, single_file)

        print_success(f"Exported {len(notes)} note(s) to {output_path}")

    except click.ClickException:
        raise
    except Exception as e:
        print_error(f"Export failed: {e}")
        raise click.Abort()


def _export_json(notes, output_path: Path, single_file: bool) -> None:
    """Export notes to JSON format.

    Args:
        notes: List of Note objects
        output_path: Output path
        single_file: Whether to export to single file
    """
    if single_file:
        # Export all notes to one JSON file
        data = []
        for note in notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'tags': note.tags,
                'created': note.created,
                'modified': note.modified,
                'content': note.content
            })

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print_verbose(f"Exported to single JSON file: {output_path}")
    else:
        # Export each note to separate JSON file
        output_path.mkdir(parents=True, exist_ok=True)

        for note in notes:
            data = {
                'id': note.id,
                'title': note.title,
                'tags': note.tags,
                'created': note.created,
                'modified': note.modified,
                'content': note.content
            }

            note_filename = f"{note.id}_{note.filepath.stem}.json"
            note_path = output_path / note_filename

            with open(note_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print_verbose(f"Exported: {note_filename}")


def _export_txt(notes, output_path: Path, single_file: bool) -> None:
    """Export notes to plain text format.

    Args:
        notes: List of Note objects
        output_path: Output path
        single_file: Whether to export to single file
    """
    if single_file:
        # Export all notes to one text file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, note in enumerate(notes):
                if i > 0:
                    f.write('\n\n' + '='*80 + '\n\n')

                f.write(f"Title: {note.title}\n")
                f.write(f"ID: {note.id}\n")
                if note.tags:
                    f.write(f"Tags: {', '.join(note.tags)}\n")
                f.write(f"Created: {note.created}\n")
                f.write(f"Modified: {note.modified}\n")
                f.write('\n' + '-'*80 + '\n\n')
                f.write(note.content)

        print_verbose(f"Exported to single text file: {output_path}")
    else:
        # Export each note to separate text file
        output_path.mkdir(parents=True, exist_ok=True)

        for note in notes:
            note_filename = f"{note.filepath.stem}.txt"
            note_path = output_path / note_filename

            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {note.title}\n")
                f.write(f"ID: {note.id}\n")
                if note.tags:
                    f.write(f"Tags: {', '.join(note.tags)}\n")
                f.write(f"Created: {note.created}\n")
                f.write(f"Modified: {note.modified}\n")
                f.write('\n' + '-'*80 + '\n\n')
                f.write(note.content)

            print_verbose(f"Exported: {note_filename}")


def _export_html(notes, output_path: Path, single_file: bool) -> None:
    """Export notes to HTML format.

    Args:
        notes: List of Note objects
        output_path: Output path
        single_file: Whether to export to single file
    """
    try:
        import markdown
    except ImportError:
        raise click.ClickException(
            "Markdown library required for HTML export. Install with: pip install markdown"
        )

    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            color: #333;
        }}
        .note {{
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #eee;
        }}
        .note:last-child {{
            border-bottom: none;
        }}
        .metadata {{
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }}
        .metadata dt {{
            font-weight: bold;
            display: inline;
        }}
        .metadata dd {{
            display: inline;
            margin: 0 0 0.5rem 0;
        }}
        .tag {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 3px;
            font-size: 0.85rem;
            margin-right: 0.3rem;
        }}
        h1 {{
            color: #2c3e50;
        }}
        code {{
            background: #f5f5f5;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

    if single_file:
        # Export all notes to one HTML file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content_parts = []
        for note in notes:
            note_html = f'<div class="note">'
            note_html += f'<h1>{_html_escape(note.title)}</h1>'

            note_html += '<dl class="metadata">'
            note_html += f'<dt>ID:</dt> <dd>{note.id}</dd><br>'
            if note.tags:
                note_html += '<dt>Tags:</dt> <dd>'
                for tag in note.tags:
                    note_html += f'<span class="tag">{_html_escape(tag)}</span>'
                note_html += '</dd><br>'
            note_html += f'<dt>Created:</dt> <dd>{_html_escape(note.created)}</dd><br>'
            note_html += f'<dt>Modified:</dt> <dd>{_html_escape(note.modified)}</dd>'
            note_html += '</dl>'

            # Convert markdown to HTML
            md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])
            note_html += md.convert(note.content)
            note_html += '</div>'

            content_parts.append(note_html)

        html = html_template.format(
            title="Exported Notes",
            content='\n'.join(content_parts)
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print_verbose(f"Exported to single HTML file: {output_path}")
    else:
        # Export each note to separate HTML file
        output_path.mkdir(parents=True, exist_ok=True)

        for note in notes:
            note_filename = f"{note.filepath.stem}.html"
            note_path = output_path / note_filename

            content = '<div class="note">'
            content += f'<h1>{_html_escape(note.title)}</h1>'

            content += '<dl class="metadata">'
            content += f'<dt>ID:</dt> <dd>{note.id}</dd><br>'
            if note.tags:
                content += '<dt>Tags:</dt> <dd>'
                for tag in note.tags:
                    content += f'<span class="tag">{_html_escape(tag)}</span>'
                content += '</dd><br>'
            content += f'<dt>Created:</dt> <dd>{_html_escape(note.created)}</dd><br>'
            content += f'<dt>Modified:</dt> <dd>{_html_escape(note.modified)}</dd>'
            content += '</dl>'

            # Convert markdown to HTML
            md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])
            content += md.convert(note.content)
            content += '</div>'

            html = html_template.format(
                title=_html_escape(note.title),
                content=content
            )

            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(html)

            print_verbose(f"Exported: {note_filename}")


def _export_pdf(notes, output_path: Path, single_file: bool) -> None:
    """Export notes to PDF format.

    Args:
        notes: List of Note objects
        output_path: Output path
        single_file: Whether to export to single file
    """
    raise click.ClickException(
        "PDF export not yet implemented. Try HTML format: --format html"
    )


def _html_escape(text: str) -> str:
    """Escape HTML special characters.

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;'))
