# Deployment Notes

POD-42 focuses on a local Django migration. Do not deploy this app as part of
the issue unless a later task explicitly asks for it.

## Heroku foundation

The repository includes a `Procfile` for an eventual Heroku web process:

```text
web: gunicorn podsreunion.wsgi --log-file -
```

Production settings live at:

```text
podsreunion.settings.production
```

Expected Heroku environment variables:

```text
DJANGO_SETTINGS_MODULE=podsreunion.settings.production
SECRET_KEY=<secure random value>
DATABASE_URL=<Heroku Postgres URL>
ALLOWED_HOSTS=<app-name>.herokuapp.com,podsreunion.com
CSRF_TRUSTED_ORIGINS=https://<app-name>.herokuapp.com,https://podsreunion.com
```

Static files are configured for collection into `staticfiles/` and serving with
WhiteNoise.
