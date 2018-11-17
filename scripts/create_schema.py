import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from app.models import Recipe, Rating, User
from core.environment import DB_DATA
from db.helpers import create_database_if_not_exists


def create_db_schemas(*args):
    for model in args:
        model.query.create_db_schema()


if __name__ == '__main__':
    create_database_if_not_exists(DB_DATA)
    create_db_schemas(Recipe, User, Rating)
