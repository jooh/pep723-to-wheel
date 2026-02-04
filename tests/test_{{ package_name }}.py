"""Placeholder tests for {{ package_name }}."""

import {{ package_name }}
{% if has_cli %}
from typer.testing import CliRunner

from {{ package_name }}.cli import app

runner = CliRunner()
{% endif %}

def test_import() -> None:
    """Verify the package can be imported."""
    assert {{ package_name }}.__doc__ is not None
{% if has_cli %}

def test_cli_hello() -> None:
    """Verify CLI hello command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "hello" in result.stdout.lower()


def test_cli_hello_default() -> None:
    """Verify CLI hello command with default name."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Hello, world!" in result.stdout


def test_cli_hello_with_name() -> None:
    """Verify CLI hello command with name option."""
    result = runner.invoke(app, ["--name", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout
{% endif %}
