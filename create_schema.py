import re

import psycopg2

from db.helpers import get_autocommit_connection, call_close
from core.environment import DB_DATA


def handle_db_creation_error(exception):
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if database_exists:
        print(message.capitalize())
    else:
        raise exception


def create_database_if_not_exists():
    connection = get_autocommit_connection(
        dbname=DB_DATA['dbname'],
        user=DB_DATA['user'],
        host=DB_DATA['host'],
        password=DB_DATA['password'],
    )
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE {};'.format(DB_DATA['dbname']))
    except psycopg2.ProgrammingError as exc:
        handle_db_creation_error(exc)
    finally:
        call_close(cursor, connection)


def create_recipe_table_if_not_exists():
    connection = get_autocommit_connection(**DB_DATA)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.recipe (
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        preparation_time INTEGER NOT NULL,
        difficulty INTEGER NOT NULL,
        vegetarian BOOLEAN NOT NULL
    );
    """)

    call_close(cursor, connection)


if __name__ == '__main__':
    create_database_if_not_exists()
    create_recipe_table_if_not_exists()
