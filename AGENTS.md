# Agent guide for pep723-to-wheel

## Repository overview
- `src/pep723_to_wheel/` contains the library and CLI implementation.
- `tests/` holds pytest coverage for core behavior.
- `pyproject.toml` defines dependencies, entry points, and tooling.

## Development setup
- Requires Python 3.12+ (see `pyproject.toml`).
- Install dev dependencies with your preferred environment manager (e.g. `uv sync --all-extras` or `pip install -e ".[dev]"`).

## Common commands
- Run tests: `make test`
- Run type checks: `make typecheck`

## Style and conventions
- Keep changes focused and covered by tests when possible.
- Prefer updating or adding pytest tests in `tests/` for behavior changes.
- For CLI changes, update both `src/pep723_to_wheel/cli.py` and any relevant tests.

## Tips
- Use `pep723_to_wheel.core` for the main build/import logic.
- The CLI entry point is `pep723_to_wheel.cli:app`.
