from db.helpers import create_database_if_not_exists
from app.models import Model  # Importing directly from "db.query" causes the actual models not to be read


def setup_database(db_data):
    create_database_if_not_exists(db_data)

    for model in Model.__subclasses__():
        model.query.create_db_schema()
