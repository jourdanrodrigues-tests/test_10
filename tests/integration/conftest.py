import pytest

from core.environment import DB_DATA
from db.handlers import setup_database, drop_database


@pytest.fixture(scope='session', autouse=True)
def database():
    DB_DATA['dbname'] += '_test'
    setup_database(DB_DATA)
    return DB_DATA


def pytest_sessionfinish():
    drop_database(DB_DATA)
