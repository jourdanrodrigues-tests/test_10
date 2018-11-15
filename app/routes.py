from app.views import get_recipes, update_recipe, create_recipe, get_recipe, delete_recipe

__all__ = [
    'routes',
]

routes = {
    r'^/recipes/$': {
        'GET': get_recipes,
        'POST': create_recipe,
    },
    r'^/recipes/(?P<id>.+)/': {
        'GET': get_recipe,
        'PUT': update_recipe,
        'PATCH': update_recipe,
        'DELETE': delete_recipe,
    },
}
