"""Download YouTube videos with quality selection and format options."""

import sys
from pathlib import Path

import click


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Show detailed progress")
@click.option("-q", "--quiet", is_flag=True, help="Suppress output except errors")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """Download YouTube videos with quality selection and format options."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


@cli.command()
@click.argument("url")
@click.option("-o", "--output", type=click.Path(), default=".", help="Output directory")
@click.option(
    "-q",
    "--quality",
    type=click.Choice(["best", "1080p", "720p", "480p", "360p", "audio-only"]),
    default="best",
    help="Video quality",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["mp4", "webm", "mkv", "mp3"]),
    default="mp4",
    help="Output format",
)
@click.option("-n", "--filename", help="Custom filename (without extension)")
@click.option("-r", "--resume", is_flag=True, help="Resume interrupted download")
@click.option("--retry", type=int, default=3, help="Number of retry attempts on failure")
@click.pass_context
def download(
    ctx: click.Context,
    url: str,
    output: str,
    quality: str,
    output_format: str,
    filename: str | None,
    resume: bool,
    retry: int,
) -> None:
    """Download a single video from YouTube.

    Examples:
        yt-download download "https://youtube.com/watch?v=abc123"
        yt-download download "https://youtube.com/watch?v=abc123" -q 720p -o ~/Videos
        yt-download download "https://youtube.com/watch?v=abc123" --format mp3
        yt-download download "https://youtube.com/watch?v=abc123" --resume --retry 5
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)

    output_path = Path(output)

    try:
        # Validate URL
        if not _is_valid_youtube_url(url):
            click.echo("Error: Invalid YouTube URL", err=True)
            sys.exit(1)

        # Ensure output directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        if verbose:
            click.echo(f"Downloading: {url}")
            click.echo(f"Quality: {quality}")
            click.echo(f"Format: {output_format}")
            click.echo(f"Output: {output_path}")
            if resume:
                click.echo("Resume mode: enabled")
            click.echo(f"Retry attempts: {retry}")

        # TODO: Implement actual download using yt-dlp
        # This is a stub that shows the intended behavior
        if not quiet:
            click.echo(f"[STUB] Would download {url} to {output_path}")

    except PermissionError:
        click.echo(f"Error: Permission denied writing to {output_path}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)


@cli.command()
@click.argument("url")
@click.option("-j", "--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def info(ctx: click.Context, url: str, as_json: bool) -> None:
    """Display video information without downloading.

    Examples:
        yt-download info "https://youtube.com/watch?v=abc123"
        yt-download info "https://youtube.com/watch?v=abc123" --json
    """
    verbose = ctx.obj.get("verbose", False)

    try:
        if not _is_valid_youtube_url(url):
            click.echo("Error: Invalid YouTube URL", err=True)
            sys.exit(1)

        if verbose:
            click.echo(f"Fetching info for: {url}")

        # TODO: Implement actual info retrieval using yt-dlp
        if as_json:
            click.echo('{"title": "[STUB] Video Title", "duration": 0, "formats": []}')
        else:
            click.echo("[STUB] Video information would be displayed here")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)


@cli.command()
@click.argument("source")
@click.option("-o", "--output", type=click.Path(), default=".", help="Output directory")
@click.option(
    "-q",
    "--quality",
    type=click.Choice(["best", "1080p", "720p", "480p", "360p", "audio-only"]),
    default="best",
    help="Video quality",
)
@click.option("-c", "--concurrent", type=int, default=3, help="Number of concurrent downloads")
@click.option("-r", "--resume", is_flag=True, help="Resume interrupted downloads")
@click.option("--retry", type=int, default=3, help="Number of retry attempts per video")
@click.option("--skip-errors", is_flag=True, help="Continue on download errors")
@click.pass_context
def batch(
    ctx: click.Context,
    source: str,
    output: str,
    quality: str,
    concurrent: int,
    resume: bool,
    retry: int,
    skip_errors: bool,
) -> None:
    """Download multiple videos from a file or playlist.

    SOURCE can be a playlist URL or a file containing URLs (one per line).

    Examples:
        yt-download batch "https://youtube.com/playlist?list=PL123"
        yt-download batch urls.txt -o ~/Videos -c 5
        yt-download batch urls.txt --resume --retry 5
        yt-download batch urls.txt -c 10 --skip-errors
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)

    output_path = Path(output)

    try:
        # Ensure output directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        # Determine if source is a file or URL
        source_path = Path(source)
        urls: list[str] = []

        if source_path.exists() and source_path.is_file():
            # Read URLs from file
            urls = [
                line.strip()
                for line in source_path.read_text().splitlines()
                if line.strip() and not line.startswith("#")
            ]
            if verbose:
                click.echo(f"Loaded {len(urls)} URLs from {source_path}")
        elif _is_valid_youtube_url(source) and "playlist" in source.lower():
            # Playlist URL
            if verbose:
                click.echo(f"Processing playlist: {source}")
            urls = [source]  # yt-dlp handles playlist expansion
        else:
            click.echo("Error: Source must be a playlist URL or file with URLs", err=True)
            sys.exit(1)

        if verbose:
            click.echo(f"Quality: {quality}")
            click.echo(f"Concurrent downloads: {concurrent}")
            click.echo(f"Output: {output_path}")
            if resume:
                click.echo("Resume mode: enabled")
            click.echo(f"Retry attempts: {retry}")
            if skip_errors:
                click.echo("Skip errors: enabled")

        # TODO: Implement actual batch download using yt-dlp
        if not quiet:
            click.echo(f"[STUB] Would download {len(urls)} video(s) to {output_path}")

    except PermissionError:
        click.echo(f"Error: Permission denied writing to {output_path}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)


def _is_valid_youtube_url(url: str) -> bool:
    """Check if URL is a valid YouTube URL."""
    valid_hosts = [
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "m.youtube.com",
    ]
    return any(host in url.lower() for host in valid_hosts)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
