# Getting Started

PodsReunion uses Django and `uv`.

## Install dependencies

```bash
uv sync
```

## Environment

Local development works without an `.env` file. By default, Django uses:

```text
DJANGO_SETTINGS_MODULE=podsreunion.settings.development_sqlite
```

To customize settings, copy the example file:

```bash
cp .env.example .env
```

## Local database

The current app only serves static pages, but Django's standard database tables
can be created with:

```bash
make migrate
```

## Run locally

```bash
make run
```

Open [http://localhost:8100](http://localhost:8100).

## Tests

```bash
make test
```

The test suite is intentionally small for now. It checks that the public pages
and representative static assets return `200`.

## Checks

```bash
make check
```
