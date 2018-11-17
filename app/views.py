from typing import Union, List

from app.authorizations import authentication_required
from app.models import Recipe, Rating
from core.exceptions import NotFoundError

__all__ = [
    'set_rating',
    'get_recipe',
    'get_recipes',
    'create_recipe',
    'update_recipe',
    'delete_recipe',
]


def get_recipes(request, **kwargs) -> List[dict]:
    name_search = request.query_params.get('name')
    if name_search:
        recipes = Recipe.query.filter(name__contains=name_search).fetch_all()
    else:
        recipes = Recipe.query.fetch_all()

    return [recipe.to_dict() for recipe in recipes]


def get_recipe(request, **kwargs) -> Union[dict, tuple]:
    recipe_id = kwargs['id']
    try:
        recipe = Recipe.query.filter(id=recipe_id).fetch_one()
        return recipe.to_dict()
    except Recipe.DoesNotExist:
        raise NotFoundError('Recipe of ID {} does not exist.'.format(recipe_id))


@authentication_required
def update_recipe(request, **kwargs) -> dict:
    recipe_id = int(kwargs['id'])
    Recipe.query.filter(id=recipe_id).update(**request.data)
    return {'id': recipe_id, **request.data}


@authentication_required
def create_recipe(request) -> dict:
    recipe = Recipe.query.create(**request.data)
    return recipe.to_dict()


@authentication_required
def delete_recipe(request, **kwargs) -> tuple:
    Recipe.query.filter(id=kwargs['id']).delete()
    return None, 204


def set_rating(request, **kwargs) -> tuple:
    recipe_id = kwargs['id']

    if not Recipe.query.filter(id=recipe_id).exists():
        raise NotFoundError('Recipe of ID {} does not exist.'.format(recipe_id))

    rating = Rating.query.create(recipe_id=int(recipe_id), **request.data)
    return rating.to_dict()
