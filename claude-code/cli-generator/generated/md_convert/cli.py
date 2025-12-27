"""Convert Markdown files to HTML with syntax highlighting for code blocks"""

import sys
from pathlib import Path

import click
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


# Theme to Pygments style mapping
THEME_STYLES = {
    "monokai": "monokai",
    "github": "github-dark",
    "dracula": "dracula",
    "solarized": "solarized-dark",
}


def _get_theme_css(theme: str) -> str:
    """Get CSS for a syntax highlighting theme."""
    style = THEME_STYLES.get(theme, "monokai")
    formatter = HtmlFormatter(style=style)
    return formatter.get_style_defs(".codehilite")


def _convert_markdown_to_html(
    content: str,
    theme: str,
    no_highlight: bool,
) -> str:
    """Convert markdown content to HTML with optional syntax highlighting."""
    extensions = ["fenced_code", "tables", "toc"]

    if not no_highlight:
        extensions.append("codehilite")
        extension_configs = {
            "codehilite": {
                "css_class": "codehilite",
                "guess_lang": True,
            }
        }
    else:
        extension_configs = {}

    md = markdown.Markdown(
        extensions=extensions,
        extension_configs=extension_configs,
    )

    return md.convert(content)


def _wrap_standalone_html(
    html_content: str,
    title: str,
    theme: str,
    no_highlight: bool,
) -> str:
    """Wrap HTML content in a complete HTML document with embedded CSS."""
    css = ""
    if not no_highlight:
        css = f"<style>\n{_get_theme_css(theme)}\n</style>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }}
        pre {{
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 0.5rem;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
        }}
    </style>
    {css}
</head>
<body>
{html_content}
</body>
</html>"""


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """Convert Markdown files to HTML with syntax highlighting for code blocks"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output HTML file (defaults to input name with .html extension)")
@click.option("-t", "--theme", type=click.Choice(["monokai", "github", "dracula", "solarized"]), default="monokai", help="Syntax highlighting theme")
@click.option("-s", "--standalone", is_flag=True, help="Generate standalone HTML with CSS embedded")
@click.option("--title", help="Page title for standalone HTML")
@click.option("--no-highlight", is_flag=True, help="Disable syntax highlighting")
@click.pass_context
def convert(ctx: click.Context, input_file: str, output: str | None, theme: str, standalone: bool, title: str | None, no_highlight: bool) -> None:
    """Convert a Markdown file to HTML

    Examples:
        md_convert convert README.md
        md_convert convert README.md -o output.html
        md_convert convert doc.md --theme github --standalone
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)

    input_path = Path(input_file)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix(".html")

    # Determine title for standalone HTML
    if standalone and not title:
        title = input_path.stem.replace("-", " ").replace("_", " ").title()

    try:
        # Read input file
        if verbose:
            click.echo(f"Reading: {input_path}")

        content = input_path.read_text(encoding="utf-8")

        # Convert markdown to HTML
        if verbose:
            click.echo(f"Converting with theme: {theme}")
            if no_highlight:
                click.echo("Syntax highlighting disabled")

        html_content = _convert_markdown_to_html(content, theme, no_highlight)

        # Wrap in standalone HTML if requested
        if standalone:
            if verbose:
                click.echo(f"Generating standalone HTML with title: {title}")
            html_content = _wrap_standalone_html(html_content, title or "", theme, no_highlight)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output file
        output_path.write_text(html_content, encoding="utf-8")

        if not quiet:
            click.echo(f"✓ Converted: {input_path} → {output_path}")

    except PermissionError:
        click.echo(f"Error: Permission denied writing to {output_path}", err=True)
        sys.exit(1)
    except UnicodeDecodeError:
        click.echo(f"Error: Unable to read {input_path} - not a valid text file", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)

@cli.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.option("-o", "--output-dir", type=click.Path(), help="Output directory (defaults to same as input)")
@click.option("-t", "--theme", type=click.Choice(["monokai", "github", "dracula", "solarized"]), default="monokai", help="Syntax highlighting theme")
@click.option("-r", "--recursive", is_flag=True, help="Process subdirectories recursively")
@click.option("-p", "--pattern", default="*.md", help="File pattern to match")
@click.pass_context
def batch(ctx: click.Context, input_dir: Path, output_dir: Path | None, theme: str | None, recursive: bool, pattern: str | None) -> None:
    """Convert multiple Markdown files at once

    Examples:
        md_convert batch ./docs
        md_convert batch ./docs -o ./html -r
        md_convert batch ./docs --pattern "*.markdown" --theme dracula
    """
    # TODO: Implement batch command
    click.echo("batch command called")

@cli.command()
@click.option("-p", "--preview", is_flag=True, help="Show a preview of each theme")
@click.pass_context
def themes(ctx: click.Context, preview: bool) -> None:
    """List available syntax highlighting themes

    Examples:
        md_convert themes
        md_convert themes --preview
    """
    # TODO: Implement themes command
    click.echo("themes command called")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()