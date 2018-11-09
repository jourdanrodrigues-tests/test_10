from app.views import get_records, set_record, get_record, delete_record

__all__ = [
    'routes',
]

routes = {
    r'^/records/$': {
        'GET': get_records,
    },
    r'^/records/(?P<id>.+)/': {
        'GET': get_record,
        'PUT': set_record,
        'PATCH': set_record,
        'DELETE': delete_record,
    },
}
