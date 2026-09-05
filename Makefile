.PHONY: install test validate explore lint clean

install:
	python -m pip install -e '.[dev]'

test:
	python -m pytest -q

validate:
	python tests/validate_workflows.py
	python -m pytest -q

explore:
	python -m owf002.repo_explorer . --format markdown

lint:
	python -m compileall -q src tests

clean:
	rm -rf .pytest_cache .coverage htmlcov build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
