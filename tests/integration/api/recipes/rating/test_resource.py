import requests

from app.models import Recipe, Rating


class TestPost:
    def test_when_recipe_exists_and_data_is_valid_then_creates_a_rating_entry(self, server_host):
        recipe = Recipe.query.create(name='A recipe name', difficulty=3, vegetarian=False, preparation_time=15)

        post_data = {'value': 1}

        response = requests.post(server_host + '/recipes/{}/rating/'.format(recipe.id), json=post_data)

        data = response.json()
        expected_data = {'id': data['id'], 'recipe_id': recipe.id, **post_data}

        try:
            assert expected_data == data
        finally:
            Rating.query.filter(id=data['id']).delete()
            Recipe.query.filter(id=recipe.id).delete()

    def test_when_recipe_exists_and_value_is_below_1_then_returns_bad_request_response(self, server_host):
        recipe = Recipe.query.create(name='A recipe name', difficulty=3, vegetarian=False, preparation_time=15)

        post_data = {'value': 0}

        response = requests.post(server_host + '/recipes/{}/rating/'.format(recipe.id), json=post_data)

        data = response.json()

        try:
            assert data == {'detail': 'Rating value should be between 1 and 5.'}
        finally:
            Recipe.query.filter(id=recipe.id).delete()

    def test_when_recipe_exists_and_value_is_above_5_then_returns_bad_request_response(self, server_host):
        recipe = Recipe.query.create(name='A recipe name', difficulty=3, vegetarian=False, preparation_time=15)

        post_data = {'value': 6}

        response = requests.post(server_host + '/recipes/{}/rating/'.format(recipe.id), json=post_data)

        data = response.json()

        try:
            assert data == {'detail': 'Rating value should be between 1 and 5.'}
        finally:
            Recipe.query.filter(id=recipe.id).delete()

    def test_when_id_does_not_exist_for_recipe_then_returns_not_found_response(self, server_host):
        response = requests.post(server_host + '/recipes/51241515/rating/', json={})

        assert response.json() == {'detail': 'Not found.'}
        assert response.status_code == 404
