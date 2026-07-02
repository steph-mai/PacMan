PYTHON = uv run python
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
CONFIG ?= config.json

.PHONY: install run debug clean lint lint-strict test

install:
	@uv sync

run:
	@$(PYTHON) pac-man.py $(CONFIG)

debug:
	@$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	@echo "Remove temporary files or caches"
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .uv_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -delete
	@echo "Cleaning complete."
lint:
	@echo "--- Running Flake8 ---"
	@uv run flake8 . --exclude .venv
	@echo "--- Running MyPy ---"
	@uv run mypy . $(MYPY_FLAGS)

lint-strict:
	@echo "--- Running Flake8 ---"
	@uv run flake8 . --exclude .venv
	@echo "--- Running MyPy ---"
	@uv run mypy . --strict

test:
	@echo "Launching the entire suite of tests..."
	@uv run pytest -v
