import requests

from app.models import Recipe, User


class TestGet:
    def test_when_id_exists_for_recipe_then_returns_data(self, server_host):
        recipe_data = {
            'name': 'A recipe name',
            'difficulty': 3,
            'vegetarian': False,
            'preparation_time': 15,
        }
        recipe_id = Recipe.query.create(**recipe_data).id

        response = requests.get(server_host + '/recipes/{}/'.format(recipe_id))

        data = response.json()
        expected_data = {'id': recipe_id, **recipe_data}

        try:
            assert expected_data == data
            assert response.status_code == 200
        finally:
            Recipe.query.filter(id=recipe_id).delete()

    def test_when_id_does_not_exist_for_recipe_then_returns_not_found_response(self, server_host):
        response = requests.get(server_host + '/recipes/51241515/')

        assert response.json() == {'detail': 'Not found.'}
        assert response.status_code == 404


class TestPut:
    def test_when_no_authorization_header_is_sent_then_returns_unauthorized_response(self, server_host):
        recipe_data = {}  # It won't get to the view anyway

        response = requests.put(server_host + '/recipes/1/', json=recipe_data)
        data = response.json()

        assert data == {'detail': 'Authorization not sent or invalid.'}
        assert response.status_code == 401

    def test_when_id_does_not_exist_for_recipe_then_returns_not_found_response(self, server_host):
        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.put(server_host + '/recipes/51241515/', headers=headers)

        try:
            assert response.json() == {'detail': 'Not found.'}
            assert response.status_code == 404
        finally:
            User.query.filter(id=user_id).delete()

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

    def test_when_id_does_not_exist_for_recipe_then_returns_not_found_response(self, server_host):
        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.patch(server_host + '/recipes/51241515/', headers=headers)

        try:
            assert response.json() == {'detail': 'Not found.'}
            assert response.status_code == 404
        finally:
            User.query.filter(id=user_id).delete()

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

    def test_when_id_does_not_exist_for_recipe_then_returns_not_found_response(self, server_host):
        user_id = User.query.create().id
        headers = {'Authorization': str(user_id)}

        response = requests.delete(server_host + '/recipes/51241515/', headers=headers)

        try:
            assert response.json() == {'detail': 'Not found.'}
            assert response.status_code == 404
        finally:
            User.query.filter(id=user_id).delete()

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
