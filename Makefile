.PHONY: test typecheck

test:
	uv run pytest

typecheck:
	uv run ty check
