from app.views import get_recipes, update_recipe, create_recipe, get_record, delete_recipe

__all__ = [
    'routes',
]

routes = {
    r'^/records/$': {
        'GET': get_recipes,
        'POST': create_recipe,
    },
    r'^/records/(?P<id>.+)/': {
        'GET': get_record,
        'PUT': update_recipe,
        'PATCH': update_recipe,
        'DELETE': delete_recipe,
    },
}
