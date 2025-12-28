"""Pytest fixtures for passgen CLI tests."""

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_passwords() -> dict[str, str]:
    """Provide sample passwords for testing."""
    return {
        "weak": "abc",
        "moderate": "MyPassword123",
        "strong": "MyP@ssw0rd!2024",
        "very_strong": "X9#kL2$mN7@pQ4&wR1!sT6*vU3^yZ8",
    }
