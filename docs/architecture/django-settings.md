# Django Settings

Settings are split into modules under `podsreunion/settings/`.

## Modules

- `development_sqlite.py` is the default local development setup.
- `development_psql.py` is available for local Postgres development.
- `production.py` is shaped for eventual Heroku deployment.

`manage.py`, `podsreunion/asgi.py`, and `podsreunion/wsgi.py` load `.env` and
fall back to `podsreunion.settings.development_sqlite` when
`DJANGO_SETTINGS_MODULE` is not set.

## Static files

Source static files live in `static/`. Public asset URLs use Django's
`/static/...` convention.
