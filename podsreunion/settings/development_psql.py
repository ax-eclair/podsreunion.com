import os

import dj_database_url

from . import *  # noqa: F403

DEBUG = True

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgres://podsreunion@localhost:5432/podsreunion",
        ),
        conn_max_age=0,
    )
}
