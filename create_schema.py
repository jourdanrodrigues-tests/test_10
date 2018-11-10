import re

import psycopg2

from core.environment import DB_DATA


def get_db_connection(**kwargs):
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    return conn


def close(*args):
    for arg in args:
        arg.close()


def handle_db_creation_error(exception):
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if database_exists:
        print(message.capitalize())
    else:
        raise exception


def create_database_if_not_exists():
    connection = get_db_connection(
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
        close(cursor, connection)


def create_recipe_table_if_not_exists():
    connection = get_db_connection(**DB_DATA)
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

    close(cursor, connection)


if __name__ == '__main__':
    create_database_if_not_exists()
    create_recipe_table_if_not_exists()
