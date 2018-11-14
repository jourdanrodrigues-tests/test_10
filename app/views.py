from typing import Union, List

from app.models import Recipe

__all__ = [
    'get_recipe',
    'get_recipes',
    'create_recipe',
    'update_recipe',
    'delete_recipe',
]


def get_recipes(request, **kwargs) -> List[dict]:
    return Recipe.query.fetch_all()


def get_recipe(request, **kwargs) -> Union[dict, tuple]:
    recipe_id = kwargs['id']
    try:
        return Recipe.query.filter(id=recipe_id).fetch_one()
    except Recipe.DoesNotExist:
        return {'detail': 'Recipe of ID {} does not exist.'.format(recipe_id)}, 404


def update_recipe(request, **kwargs) -> dict:
    recipe_id = kwargs['id']
    Recipe.query.filter(id=recipe_id).update(**request.data)
    return {'id': recipe_id, **request.data}


def create_recipe(request) -> dict:
    return Recipe.query.create(**request.data)


def delete_recipe(request, **kwargs) -> tuple:
    Recipe.query.filter(id=kwargs['id']).delete()
    return None, 204
