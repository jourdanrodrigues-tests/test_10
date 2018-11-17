import os
import sys

import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from app.models import Recipe, Rating, User
from core.environment import DB_DATA
from db.helpers import get_autocommit_connection, call_close, raise_if_database_does_not_exist


def create_database_if_not_exists():
    db_data = DB_DATA.copy()
    db_data['dbname'] = 'postgres'
    connection = get_autocommit_connection(**db_data)
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE {};'.format(DB_DATA['dbname']))
    except psycopg2.ProgrammingError as exc:
        raise_if_database_does_not_exist(exc)
    finally:
        call_close(cursor, connection)


def create_db_schemas(*args):
    for model in args:
        model.query.create_db_schema()


if __name__ == '__main__':
    create_database_if_not_exists()
    create_db_schemas(Recipe, User, Rating)
