.PHONY: test typecheck ruff all-tests

test:
	uv run pytest --cov={{ package_name }} --cov-report=term-missing --cov-report=xml

typecheck:
	uv run ty check

ruff:
	uv run ruff check .

all-tests: test typecheck ruff
