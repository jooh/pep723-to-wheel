# Agent guide for {{ project_name }}

## Repository overview
- `src/{{ package_name }}/` contains the library{% if has_cli %} and CLI{% endif %} implementation.
- `tests/` holds pytest coverage for core behavior.
- `pyproject.toml` defines dependencies, entry points, and tooling.

## Development setup
- Requires Python {{ min_python_version }}+ (see `pyproject.toml`).
- Environment management is with uv.
- Run Python and related CLI tools via `uv run` so they use the uv virtualenv.

## Common commands
- Run tests: `make test`
- Run type checks: `make typecheck`
- Run ruff checks: `make ruff`
- Run all checks: `make all-tests`

## Style and conventions
- TDD for all code development - write test, then run to verify it fails, then develop, then verify the test passes.
- All tasks should end by running `make all-tests` and verifying it passes.
- Prefer updating or adding pytest tests in `tests/` for behavior changes.
{%- if has_cli %}
- For CLI changes, update both `src/{{ package_name }}/cli.py` and any relevant tests.
{%- endif %}
- Target modern Python {{ min_python_version }}+ syntax, no need to be backwards compatible.

## Tips
- The main package is `{{ package_name }}`.
{%- if has_cli %}
- The CLI entry point is `{{ package_name }}.cli:app`.
{%- endif %}
