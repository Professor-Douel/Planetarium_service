import os

import time

import django
from django.db import connections
from django.db.utils import OperationalError


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Planetarium_service.settings"
)
django.setup()


def wait_for_db():
    print("Waiting for database...")
    db_conn = None

    while not db_conn:
        try:
            db_conn = connections["default"]
            db_conn.cursor()
            print("Database is available!")
            break
        except OperationalError:
            print("Database is not ready, wait 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    wait_for_db()
