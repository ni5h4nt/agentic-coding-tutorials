"""Create command for notes CLI."""

from pathlib import Path

import click
import frontmatter

from ..utils import (
    get_notes_dir,
    sanitize_filename,
    open_in_editor,
    parse_tags,
    print_success,
    print_error,
    print_verbose,
)


@click.command()
@click.argument('title', type=str, required=True)
@click.option(
    '--editor', '-e',
    type=str,
    default=None,
    help='Editor to use (overrides $EDITOR)'
)
@click.option(
    '--tags', '-t',
    type=str,
    default=None,
    help='Comma-separated tags'
)
@click.option(
    '--template', '-T',
    type=str,
    default=None,
    help='Template file to use'
)
@click.pass_context
def create(ctx: click.Context, title: str, editor: str | None, tags: str | None, template: str | None) -> None:
    """Create a new markdown note.

    Creates a new note with the specified title. Opens the note in your
    preferred editor (from $EDITOR or --editor option).

    Examples:
        notes-cli create "My First Note"
        notes-cli create "Python Tips" --tags python,programming
        notes-cli create "Meeting Notes" --editor vim
    """
    try:
        notes_dir = get_notes_dir(ctx.obj['notes_dir'])
        print_verbose(f"Using notes directory: {notes_dir}")

        # Create sanitized filename
        filename = sanitize_filename(title) + '.md'
        filepath = notes_dir / filename

        # Check if file already exists
        if filepath.exists():
            raise click.ClickException(f"Note with title '{title}' already exists")

        print_verbose(f"Creating note: {filepath}")

        # Parse tags
        tag_list = parse_tags(tags)

        # Load template if specified
        template_content = ""
        if template:
            template_path = Path(template).expanduser()
            if not template_path.exists():
                raise click.ClickException(f"Template file not found: {template}")
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_post = frontmatter.load(f)
                    template_content = template_post.content
                print_verbose(f"Loaded template from: {template_path}")
            except Exception as e:
                raise click.ClickException(f"Failed to read template: {e}")

        # Create initial note with frontmatter
        from datetime import datetime
        import hashlib

        # Generate unique ID
        hash_obj = hashlib.md5(str(filepath).encode())
        note_id = int(hash_obj.hexdigest()[:8], 16) % 1000000

        metadata = {
            'id': note_id,
            'title': title,
            'tags': tag_list,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }

        post = frontmatter.Post(template_content, **metadata)

        # Write initial note
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        print_verbose(f"Created note with ID: {note_id}")

        # Open in editor
        try:
            open_in_editor(filepath, editor)
        except click.ClickException:
            # Editor failed, but note was created
            print_error("Failed to open editor")
            print_success(f"Note created: {title} (ID: {note_id})")
            raise click.Abort()

        print_success(f"Note created: {title} (ID: {note_id})")

    except click.ClickException:
        raise
    except click.Abort:
        raise
    except Exception as e:
        print_error(f"Failed to create note: {e}")
        raise click.Abort()
