"""CLI for {{ project_name }}."""

import typer

app = typer.Typer()


@app.command()
def hello(name: str = "world") -> None:
    """Say hello."""
    print(f"Hello, {name}!")
