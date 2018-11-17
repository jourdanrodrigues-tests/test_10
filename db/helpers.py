import re

import psycopg2


__all__ = [
    'call_close',
    'handle_db_creation_error',
    'get_autocommit_connection',
]


def handle_db_creation_error(exception):
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if database_exists:
        print(message.capitalize())
    else:
        raise exception


def call_close(*args) -> None:
    for arg in args:
        arg.close()


def get_autocommit_connection(**kwargs):
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    return conn
