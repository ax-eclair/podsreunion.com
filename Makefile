.PHONY: sync run migrate test check lint format collectstatic

sync:
	uv sync

run:
	uv run python manage.py runserver 8100

migrate:
	uv run python manage.py migrate

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format --check .

check: lint format test
	@echo "Passing local checks"

collectstatic:
	uv run python manage.py collectstatic --noinput
