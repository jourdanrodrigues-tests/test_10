import requests

from app.models import Recipe


class TestGet:
    def test_that_it_retrieves_all_recipes_on_the_database(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }
        Recipe.query.create(**recipe_data)

        response = requests.get(server_host + '/recipes/')

        data = response.json()
        created_id = data[0]['id']
        expected_data = [{'id': created_id, **recipe_data}]

        try:
            assert expected_data == data
        finally:
            Recipe.query.filter(id=created_id).delete()

    def test_when_filtered_by_name_then_returns_recipes_that_match(self, server_host):
        id1 = Recipe.query.create(name='A random name', difficulty=2, vegetarian=True, preparation_time=15).id
        id2 = Recipe.query.create(name='Another random recipe', difficulty=1, vegetarian=False, preparation_time=5).id

        response = requests.get(server_host + '/recipes/?name=Another')
        data = response.json()

        try:
            assert isinstance(data, list) and len(data) == 1
        finally:
            Recipe.query.filter(id__in=[id1, id2]).delete()
