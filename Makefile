.PHONY: test typecheck ruff all-tests

test:
	uv run pytest

typecheck:
	uv run ty check

ruff:
	uv run ruff check .

all-tests: test typecheck ruff
