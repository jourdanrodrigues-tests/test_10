import re

import psycopg2

__all__ = [
    'call_close',
    'raise_if_database_does_not_exist',
    'get_autocommit_connection',
    'create_database_if_not_exists',
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


def create_database_if_not_exists(db_data):
    postgres_db_data = db_data.copy()
    postgres_db_data['dbname'] = 'postgres'
    connection = get_autocommit_connection(**db_data)
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE {};'.format(db_data['dbname']))
    except psycopg2.ProgrammingError as exc:
        raise_if_database_does_not_exist(exc)
    finally:
        call_close(cursor, connection)
