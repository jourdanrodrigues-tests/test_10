import re

import psycopg2


__all__ = [
    'call_close',
    'raise_if_database_does_not_exist',
    'get_autocommit_connection',
]


def raise_if_database_does_not_exist(exception: Exception) -> None:
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if not database_exists:
        raise exception


def call_close(*args) -> None:
    for arg in args:
        arg.close()


def get_autocommit_connection(**kwargs):
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    return conn
