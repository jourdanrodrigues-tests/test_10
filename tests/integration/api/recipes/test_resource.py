import requests

from app.models import Recipe, User


class TestGet:
    def test_that_it_retrieves_all_recipes_on_the_database(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }
        recipe_id = Recipe.query.create(**recipe_data).id

        response = requests.get(server_host + '/recipes/')

        data = response.json()
        expected_data = [{'id': recipe_id, **recipe_data}]

        try:
            assert expected_data == data
        finally:
            Recipe.query.filter(id=recipe_id).delete()

    def test_when_filtered_by_name_then_returns_recipes_that_match(self, server_host):
        id1 = Recipe.query.create(name='A random name', difficulty=2, vegetarian=True, preparation_time=15).id
        id2 = Recipe.query.create(name='Another random recipe', difficulty=1, vegetarian=False, preparation_time=5).id

        response = requests.get(server_host + '/recipes/?name=Another')
        data = response.json()

        try:
            assert isinstance(data, list) and len(data) == 1
        finally:
            Recipe.query.filter(id__in=[id1, id2]).delete()


class TestPost:
    def test_when_no_authorization_header_is_sent_then_returns_unauthorized_response(self, server_host):
        recipe_data = {}  # It won't get to the view anyway

        response = requests.post(server_host + '/recipes/', json=recipe_data)
        data = response.json()

        assert data == {'detail': 'Authorization not sent or invalid.'}
        assert response.status_code == 401

    def test_when_authorized_and_data_is_valid_then_returns_data_with_created_id(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.post(server_host + '/recipes/', json=recipe_data, headers=headers)
        data = response.json()
        expected_data = {'id': data['id'], **recipe_data}

        try:
            assert expected_data == data
            assert response.status_code == 200
        finally:
            User.query.filter(id=user_id).delete()
            Recipe.query.filter(id=data['id']).delete()

    def test_when_authorized_and_data_difficulty_is_above_3_then_returns_bad_request_response(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 4,
            'vegetarian': False,
            'preparation_time': 15,
        }

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.post(server_host + '/recipes/', json=recipe_data, headers=headers)
        data = response.json()

        try:
            assert data == {'detail': 'Recipe difficulty should be between 1 and 3.'}
            assert response.status_code == 400
        finally:
            User.query.filter(id=user_id).delete()

    def test_when_authorized_and_data_difficulty_is_below_1_then_returns_bad_request_response(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 0,
            'vegetarian': False,
            'preparation_time': 15,
        }

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.post(server_host + '/recipes/', json=recipe_data, headers=headers)
        data = response.json()

        try:
            assert data == {'detail': 'Recipe difficulty should be between 1 and 3.'}
            assert response.status_code == 400
        finally:
            User.query.filter(id=user_id).delete()
