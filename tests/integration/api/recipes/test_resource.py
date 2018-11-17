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


class TestPut:
    def test_when_no_authorization_header_is_sent_then_returns_unauthorized_response(self, server_host):
        recipe_data = {}  # It won't get to the view anyway

        response = requests.put(server_host + '/recipes/1/', json=recipe_data)
        data = response.json()

        assert data == {'detail': 'Authorization not sent or invalid.'}
        assert response.status_code == 401

    def test_when_authorized_and_data_is_valid_then_updates_and_returns_data(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }
        recipe_id = Recipe.query.create(**recipe_data).id

        recipe_data['name'] = 'One fine recipe'
        recipe_data['vegetarian'] = True

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.put(server_host + '/recipes/{}/'.format(recipe_id), json=recipe_data, headers=headers)
        data = response.json()
        expected_data = {'id': recipe_id, **recipe_data}

        try:
            assert expected_data == data
            assert Recipe.query.filter(**expected_data).exists()
            assert response.status_code == 200
        finally:
            User.query.filter(id=user_id).delete()
            Recipe.query.filter(id=data['id']).delete()


class TestPatch:
    def test_when_no_authorization_header_is_sent_then_returns_unauthorized_response(self, server_host):
        recipe_data = {}  # It won't get to the view anyway

        response = requests.patch(server_host + '/recipes/1/', json=recipe_data)
        data = response.json()

        assert data == {'detail': 'Authorization not sent or invalid.'}
        assert response.status_code == 401

    def test_when_authorized_and_data_is_valid_then_updates_and_returns_data(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }
        recipe_id = Recipe.query.create(**recipe_data).id

        recipe_data['name'] = 'One fine recipe'
        recipe_data['vegetarian'] = True

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.patch(server_host + '/recipes/{}/'.format(recipe_id), json=recipe_data, headers=headers)
        data = response.json()
        expected_data = {'id': recipe_id, **recipe_data}

        try:
            assert expected_data == data
            assert Recipe.query.filter(**expected_data).exists()
            assert response.status_code == 200
        finally:
            User.query.filter(id=user_id).delete()
            Recipe.query.filter(id=data['id']).delete()


class TestDelete:
    def test_when_no_authorization_header_is_sent_then_returns_unauthorized_response(self, server_host):
        response = requests.delete(server_host + '/recipes/1/')
        data = response.json()

        assert data == {'detail': 'Authorization not sent or invalid.'}
        assert response.status_code == 401

    def test_when_authorized_and_data_is_valid_then_updates_and_returns_data(self, server_host):
        recipe = Recipe.query.create(name='A recipe name', difficulty=3, vegetarian=False, preparation_time=15)

        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.delete(server_host + '/recipes/{}/'.format(recipe.id), headers=headers)

        try:
            assert not Recipe.query.filter(id=recipe.id).exists()
            assert response.status_code == 204
        finally:
            User.query.filter(id=user_id).delete()
