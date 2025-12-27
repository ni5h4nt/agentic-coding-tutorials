"""Tests for md_convert CLI commands."""

import pytest
from click.testing import CliRunner
from pathlib import Path

from md_convert.cli import cli, main


class TestCLI:
    """Test the main CLI group."""

    def test_cli_help(self):
        """Test that --help works."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Convert Markdown files to HTML" in result.output

    def test_cli_version(self):
        """Test that --version works."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_verbose_flag(self):
        """Test the verbose global flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["-v", "--help"])
        assert result.exit_code == 0

    def test_cli_quiet_flag(self):
        """Test the quiet global flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["-q", "--help"])
        assert result.exit_code == 0


class TestConvertCommand:
    """Test the convert command."""

    def test_convert_help(self):
        """Test convert --help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["convert", "--help"])
        assert result.exit_code == 0
        assert "Convert a Markdown file to HTML" in result.output
        assert "--output" in result.output
        assert "--theme" in result.output
        assert "--standalone" in result.output

    def test_convert_basic(self, sample_markdown: Path):
        """Test basic conversion creates HTML file."""
        runner = CliRunner()
        result = runner.invoke(cli, ["convert", str(sample_markdown)])
        assert result.exit_code == 0
        assert "Converted:" in result.output

        # Verify output file was created
        output_file = sample_markdown.with_suffix(".html")
        assert output_file.exists()
        content = output_file.read_text()
        assert "<h1" in content  # H1 from markdown (may have id attribute)
        assert "Sample Document" in content

    def test_convert_with_output(self, sample_markdown: Path, temp_dir: Path):
        """Test conversion with output option."""
        output_file = temp_dir / "output.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        assert output_file.exists()
        assert "<h1" in output_file.read_text()  # H1 may have id attribute

    def test_convert_with_theme(self, sample_markdown: Path, temp_dir: Path):
        """Test conversion with theme option."""
        output_file = temp_dir / "themed.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "--theme", "github",
            "-o", str(output_file),
            "--standalone"
        ])
        assert result.exit_code == 0
        content = output_file.read_text()
        # Verify HTML was created with syntax highlighting CSS
        assert "<!DOCTYPE html>" in content

    def test_convert_invalid_theme(self, sample_markdown: Path):
        """Test conversion with invalid theme."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "--theme", "invalid"
        ])
        assert result.exit_code != 0
        assert "Invalid value for" in result.output
        assert "--theme" in result.output

    def test_convert_standalone(self, sample_markdown: Path, temp_dir: Path):
        """Test standalone HTML generation."""
        output_file = temp_dir / "standalone.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "--standalone",
            "--title", "My Document",
            "-o", str(output_file)
        ])
        assert result.exit_code == 0

        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "<title>My Document</title>" in content
        assert "<body>" in content
        assert "</html>" in content

    def test_convert_standalone_auto_title(self, sample_markdown: Path, temp_dir: Path):
        """Test standalone HTML generates title from filename."""
        output_file = temp_dir / "auto_title.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "--standalone",
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        content = output_file.read_text()
        assert "<title>Sample</title>" in content

    def test_convert_no_highlight(self, sample_markdown: Path, temp_dir: Path):
        """Test disabling syntax highlighting."""
        output_file = temp_dir / "no_highlight.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "--no-highlight",
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        content = output_file.read_text()
        # Should not have codehilite class when highlighting is disabled
        assert "codehilite" not in content

    def test_convert_verbose(self, sample_markdown: Path, temp_dir: Path):
        """Test verbose output."""
        output_file = temp_dir / "verbose.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "-v", "convert", str(sample_markdown),
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        assert "Reading:" in result.output
        assert "Converting with theme:" in result.output

    def test_convert_quiet(self, sample_markdown: Path, temp_dir: Path):
        """Test quiet mode suppresses output."""
        output_file = temp_dir / "quiet.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "-q", "convert", str(sample_markdown),
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        assert result.output == ""  # No output in quiet mode

    def test_convert_creates_output_directory(self, sample_markdown: Path, temp_dir: Path):
        """Test that convert creates output directory if needed."""
        output_file = temp_dir / "subdir" / "nested" / "output.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_convert_preserves_code_blocks(self, sample_markdown: Path, temp_dir: Path):
        """Test that code blocks are preserved in output."""
        output_file = temp_dir / "code.html"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(sample_markdown),
            "-o", str(output_file)
        ])
        assert result.exit_code == 0
        content = output_file.read_text()
        # Code content should be present
        assert "hello" in content.lower()

    def test_convert_nonexistent_file(self, temp_dir: Path):
        """Test error when input file doesn't exist."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "convert", str(temp_dir / "nonexistent.md")
        ])
        assert result.exit_code != 0


class TestBatchCommand:
    """Test the batch command."""

    def test_batch_help(self):
        """Test batch --help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["batch", "--help"])
        assert result.exit_code == 0
        assert "Convert multiple Markdown files" in result.output
        assert "--output-dir" in result.output
        assert "--recursive" in result.output
        assert "--pattern" in result.output

    def test_batch_basic(self, sample_markdown_dir: Path):
        """Test basic batch conversion."""
        runner = CliRunner()
        result = runner.invoke(cli, ["batch", str(sample_markdown_dir)])
        assert result.exit_code == 0
        assert "batch command called" in result.output

    def test_batch_with_output_dir(self, sample_markdown_dir: Path, temp_dir: Path):
        """Test batch conversion with output directory."""
        output_dir = temp_dir / "output"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "batch", str(sample_markdown_dir),
            "-o", str(output_dir)
        ])
        assert result.exit_code == 0

    def test_batch_recursive(self, sample_markdown_dir: Path):
        """Test recursive batch conversion."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "batch", str(sample_markdown_dir),
            "--recursive"
        ])
        assert result.exit_code == 0

    def test_batch_with_pattern(self, sample_markdown_dir: Path):
        """Test batch conversion with file pattern."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "batch", str(sample_markdown_dir),
            "--pattern", "*.markdown"
        ])
        assert result.exit_code == 0


class TestThemesCommand:
    """Test the themes command."""

    def test_themes_help(self):
        """Test themes --help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["themes", "--help"])
        assert result.exit_code == 0
        assert "List available syntax highlighting themes" in result.output

    def test_themes_basic(self):
        """Test basic themes list."""
        runner = CliRunner()
        result = runner.invoke(cli, ["themes"])
        assert result.exit_code == 0
        assert "themes command called" in result.output

    def test_themes_with_preview(self):
        """Test themes with preview option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["themes", "--preview"])
        assert result.exit_code == 0


class TestMainEntrypoint:
    """Test the main entrypoint function."""

    def test_main_exists(self):
        """Test that main function exists and is callable."""
        assert callable(main)
