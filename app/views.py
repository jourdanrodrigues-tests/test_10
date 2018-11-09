__all__ = [
    'set_record',
    'get_record',
    'get_records',
    'delete_record',
]


records = {}


def get_records(handler, **kwargs):
    return records


def get_record(handler, **kwargs):
    key = handler.path[8:]
    return (records[key], 200) if key in records else (None, 404)


def set_record(handler, **kwargs):
    record_id = kwargs['id']
    payload = handler.get_payload()
    records[record_id] = payload
    return payload


def delete_record(handler, **kwargs):
    key = handler.path[8:]
    del records[key]
    return None, 204
