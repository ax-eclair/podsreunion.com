.PHONY: sync run migrate seed reseed-hard test check lint format format-check collectstatic

PORT ?= 8100
SQLITE_DB ?= db.sqlite3

sync:
	uv sync

run:
	uv run python manage.py runserver $(PORT)

migrate:
	uv run python manage.py migrate

seed: migrate
	uv run python manage.py loaddata dev_superuser

reseed-hard:
	rm -f $(SQLITE_DB)
	$(MAKE) seed

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

check: lint format-check test
	@echo "Passing local checks"

collectstatic:
	uv run python manage.py collectstatic --noinput
