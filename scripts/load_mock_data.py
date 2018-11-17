import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from app.models import Recipe, User, Rating

MOCK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'mock_data')

if __name__ == '__main__':
    User.query.create()
    recipe = Recipe.query.create(name='Pasta', difficulty=2, vegetarian=True, preparation_time=5)
    Rating.query.create(value=3, recipe_id=recipe.id)
