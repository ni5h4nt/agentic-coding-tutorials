"""Main CLI entry point for notes_cli."""

import sys
from pathlib import Path

import click

from . import __version__


@click.group(invoke_without_command=True)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose debug output'
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Suppress non-error output'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Disable colored output'
)
@click.option(
    '--notes-dir', '-d',
    type=click.Path(),
    default=str(Path.home() / '.notes'),
    help='Notes directory'
)
@click.version_option(version=__version__, prog_name='notes-cli')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, no_color: bool, notes_dir: str) -> None:
    """A markdown-based note-taking CLI for creating, managing, searching, and organizing notes.

    Examples:
        notes-cli create "My First Note"
        notes-cli list --tags python
        notes-cli search "todo"
        notes-cli edit "My First Note"
    """
    # Ensure obj dict exists for passing global options
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['no_color'] = no_color
    ctx.obj['notes_dir'] = notes_dir

    # Set up color handling
    if no_color:
        import os
        os.environ['NO_COLOR'] = '1'

    # Show help if no command provided
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Import and register commands
from .commands import create, list, view, search, edit, delete, tag, export

cli.add_command(create.create)
cli.add_command(list.list_notes)
cli.add_command(view.view)
cli.add_command(search.search)
cli.add_command(edit.edit)
cli.add_command(delete.delete)
cli.add_command(tag.tag)
cli.add_command(export.export)


def main() -> None:
    """Entry point for the CLI."""
    try:
        cli(obj={})
    except click.ClickException as e:
        e.show()
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)


if __name__ == '__main__':
    main()
