"""Tests for passgen CLI."""

import string

from click.testing import CliRunner

from passgen.cli import (
    PRESETS,
    _analyze_password,
    _build_charset,
    _calculate_entropy,
    _generate_password,
    _get_strength_rating,
    cli,
)


class TestCLI:
    """Tests for main CLI group."""

    def test_help(self, runner: CliRunner) -> None:
        """Test --help flag."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "password generator" in result.output.lower()

    def test_version(self, runner: CliRunner) -> None:
        """Test --version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_no_command(self, runner: CliRunner) -> None:
        """Test CLI without command shows usage error."""
        result = runner.invoke(cli)
        assert result.exit_code == 2  # Click returns 2 for missing command
        assert "Usage:" in result.output


class TestGenerateCommand:
    """Tests for generate command."""

    def test_default_generation(self, runner: CliRunner) -> None:
        """Test default password generation."""
        result = runner.invoke(cli, ["generate"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert len(password) == 16

    def test_custom_length(self, runner: CliRunner) -> None:
        """Test password generation with custom length."""
        result = runner.invoke(cli, ["generate", "-l", "24"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert len(password) == 24

    def test_multiple_passwords(self, runner: CliRunner) -> None:
        """Test generating multiple passwords."""
        result = runner.invoke(cli, ["generate", "-n", "5"])
        assert result.exit_code == 0
        passwords = result.output.strip().split("\n")
        assert len(passwords) == 5

    def test_with_symbols(self, runner: CliRunner) -> None:
        """Test password generation with symbols."""
        # Generate multiple to increase chance of symbols
        result = runner.invoke(cli, ["generate", "-s", "-l", "50"])
        assert result.exit_code == 0
        password = result.output.strip()
        # Check that symbols are possible (not guaranteed in every password)
        assert len(password) == 50

    def test_no_uppercase(self, runner: CliRunner) -> None:
        """Test password without uppercase."""
        result = runner.invoke(cli, ["generate", "--no-uppercase", "-l", "20"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert password == password.lower() or not any(c in string.ascii_uppercase for c in password)

    def test_no_lowercase(self, runner: CliRunner) -> None:
        """Test password without lowercase."""
        result = runner.invoke(cli, ["generate", "--no-lowercase", "-l", "20"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert not any(c in string.ascii_lowercase for c in password)

    def test_no_digits(self, runner: CliRunner) -> None:
        """Test password without digits."""
        result = runner.invoke(cli, ["generate", "--no-digits", "-l", "20"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert not any(c in string.digits for c in password)

    def test_exclude_characters(self, runner: CliRunner) -> None:
        """Test excluding specific characters."""
        result = runner.invoke(cli, ["generate", "-x", "abc123", "-l", "30"])
        assert result.exit_code == 0
        password = result.output.strip()
        for char in "abc123":
            assert char not in password

    def test_no_ambiguous(self, runner: CliRunner) -> None:
        """Test excluding ambiguous characters."""
        result = runner.invoke(cli, ["generate", "--no-ambiguous", "-l", "100"])
        assert result.exit_code == 0
        password = result.output.strip()
        for char in "0O1lI":
            assert char not in password

    def test_invalid_length(self, runner: CliRunner) -> None:
        """Test invalid length raises error."""
        result = runner.invoke(cli, ["generate", "-l", "0"])
        assert result.exit_code != 0
        assert "at least 1" in result.output.lower()

    def test_invalid_count(self, runner: CliRunner) -> None:
        """Test invalid count raises error."""
        result = runner.invoke(cli, ["generate", "-n", "0"])
        assert result.exit_code != 0
        assert "at least 1" in result.output.lower()

    def test_verbose_output(self, runner: CliRunner) -> None:
        """Test verbose output shows extra info."""
        result = runner.invoke(cli, ["--verbose", "generate"])
        assert result.exit_code == 0
        assert "Character set size:" in result.output

    def test_quiet_output(self, runner: CliRunner) -> None:
        """Test quiet mode suppresses extra output."""
        result = runner.invoke(cli, ["--quiet", "generate"])
        assert result.exit_code == 0
        # Should only have the password, no extra text
        lines = result.output.strip().split("\n")
        assert len(lines) == 1


class TestStrengthCommand:
    """Tests for strength command."""

    def test_weak_password(self, runner: CliRunner, sample_passwords: dict) -> None:
        """Test weak password analysis."""
        result = runner.invoke(cli, ["strength", sample_passwords["weak"]])
        assert result.exit_code == 0
        assert "weak" in result.output.lower()

    def test_strong_password(self, runner: CliRunner, sample_passwords: dict) -> None:
        """Test strong password analysis."""
        result = runner.invoke(cli, ["strength", sample_passwords["very_strong"]])
        assert result.exit_code == 0
        assert "strong" in result.output.lower()

    def test_verbose_analysis(self, runner: CliRunner, sample_passwords: dict) -> None:
        """Test verbose strength analysis."""
        result = runner.invoke(cli, ["strength", sample_passwords["moderate"], "-v"])
        assert result.exit_code == 0
        assert "Length:" in result.output
        assert "Entropy:" in result.output
        assert "Has uppercase:" in result.output

    def test_min_length_warning(self, runner: CliRunner) -> None:
        """Test minimum length warning."""
        result = runner.invoke(cli, ["strength", "short", "--min-length", "12"])
        assert result.exit_code == 0
        assert "shorter than minimum" in result.output.lower()

    def test_min_length_pass(self, runner: CliRunner) -> None:
        """Test password meeting minimum length."""
        result = runner.invoke(cli, ["strength", "LongEnoughPassword123!", "--min-length", "12"])
        assert result.exit_code == 0
        assert "shorter than minimum" not in result.output.lower()

    def test_quiet_mode(self, runner: CliRunner, sample_passwords: dict) -> None:
        """Test quiet mode only shows rating."""
        result = runner.invoke(cli, ["--quiet", "strength", sample_passwords["moderate"]])
        assert result.exit_code == 0
        # Should only have the rating word
        output = result.output.strip().lower()
        assert output in ["very weak", "weak", "moderate", "strong", "very strong"]


class TestPresetsCommand:
    """Tests for presets command."""

    def test_list_presets(self, runner: CliRunner) -> None:
        """Test listing presets."""
        result = runner.invoke(cli, ["presets", "--list"])
        assert result.exit_code == 0
        for preset_name in PRESETS:
            assert preset_name in result.output

    def test_no_args_lists_presets(self, runner: CliRunner) -> None:
        """Test that no arguments lists presets."""
        result = runner.invoke(cli, ["presets"])
        assert result.exit_code == 0
        assert "pin" in result.output
        assert "memorable" in result.output

    def test_use_pin_preset(self, runner: CliRunner) -> None:
        """Test using PIN preset."""
        result = runner.invoke(cli, ["presets", "--use", "pin"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert len(password) == 4
        assert password.isdigit()

    def test_use_strong_preset(self, runner: CliRunner) -> None:
        """Test using strong preset."""
        result = runner.invoke(cli, ["presets", "--use", "strong"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert len(password) == 16

    def test_use_paranoid_preset(self, runner: CliRunner) -> None:
        """Test using paranoid preset."""
        result = runner.invoke(cli, ["presets", "-u", "paranoid"])
        assert result.exit_code == 0
        password = result.output.strip()
        assert len(password) == 32

    def test_invalid_preset(self, runner: CliRunner) -> None:
        """Test invalid preset name."""
        result = runner.invoke(cli, ["presets", "--use", "invalid"])
        assert result.exit_code != 0


class TestHelperFunctions:
    """Tests for internal helper functions."""

    def test_build_charset_default(self) -> None:
        """Test default charset includes upper, lower, digits."""
        charset = _build_charset()
        assert all(c in charset for c in "ABC")
        assert all(c in charset for c in "abc")
        assert all(c in charset for c in "123")
        assert "!" not in charset  # No symbols by default

    def test_build_charset_with_symbols(self) -> None:
        """Test charset with symbols."""
        charset = _build_charset(symbols=True)
        assert "!" in charset or "@" in charset

    def test_build_charset_exclude(self) -> None:
        """Test excluding characters from charset."""
        charset = _build_charset(exclude="aeiou")
        assert "a" not in charset
        assert "e" not in charset
        assert "i" not in charset

    def test_build_charset_no_ambiguous(self) -> None:
        """Test excluding ambiguous characters."""
        charset = _build_charset(no_ambiguous=True)
        for char in "0O1lI":
            assert char not in charset

    def test_generate_password_length(self) -> None:
        """Test password generation length."""
        charset = _build_charset()
        password = _generate_password(charset, 20)
        assert len(password) == 20

    def test_generate_password_uses_charset(self) -> None:
        """Test password only uses provided charset."""
        charset = "abc"
        password = _generate_password(charset, 100)
        assert all(c in charset for c in password)

    def test_calculate_entropy(self) -> None:
        """Test entropy calculation."""
        # Simple password with 2 unique chars
        entropy = _calculate_entropy("aabb")
        assert entropy > 0

        # Empty password
        entropy = _calculate_entropy("")
        assert entropy == 0

    def test_analyze_password(self) -> None:
        """Test password analysis."""
        analysis = _analyze_password("Abc123!@#")
        assert analysis["length"] == 9
        assert analysis["has_uppercase"] is True
        assert analysis["has_lowercase"] is True
        assert analysis["has_digits"] is True
        assert analysis["has_symbols"] is True
        assert analysis["entropy"] > 0

    def test_get_strength_rating_weak(self) -> None:
        """Test weak strength rating."""
        rating, color = _get_strength_rating(20, 5, 8)
        assert rating in ["very weak", "weak"]
        assert color == "red"

    def test_get_strength_rating_too_short(self) -> None:
        """Test too short password rating."""
        rating, color = _get_strength_rating(100, 5, 8)
        assert rating == "weak"
        assert color == "red"

    def test_get_strength_rating_strong(self) -> None:
        """Test strong strength rating."""
        rating, color = _get_strength_rating(80, 20, 8)
        assert "strong" in rating
        assert color in ["green", "bright_green"]


class TestMainEntrypoint:
    """Tests for main entrypoint."""

    def test_main_function(self, runner: CliRunner) -> None:
        """Test main() function works."""
        from passgen.cli import main

        # main() calls cli() internally, so we just verify it exists
        assert callable(main)
