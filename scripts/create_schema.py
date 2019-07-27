import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from core.environment import DB_DATA
from db.handlers import setup_database

if __name__ == '__main__':
    setup_database(DB_DATA)
