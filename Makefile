.PHONY: test typecheck ruff

test:
	uv run pytest --cov=pep723_to_wheel --cov-report=term-missing --cov-report=xml

typecheck:
	uv run ty check

ruff:
	uv run ruff check .
