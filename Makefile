.PHONY: test typecheck ruff

test:
	uv run pytest

typecheck:
	uv run ty check

ruff:
	uv run ruff check .
