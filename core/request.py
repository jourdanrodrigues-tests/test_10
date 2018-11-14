import json
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

__all__ = [
    'RequestHandler',
]


METHODS_WITH_BODY = ['POST', 'PUT', 'PATCH', 'DELETE']


# noinspection PyPep8Naming
class MethodsMixin:
    def handle_method(self, method: str) -> None:
        raise NotImplementedError()

    def do_HEAD(self) -> None:
        self.handle_method('HEAD')

    def do_GET(self) -> None:
        self.handle_method('GET')

    def do_POST(self) -> None:
        self.handle_method('POST')

    def do_PUT(self) -> None:
        self.handle_method('PUT')

    def do_PATCH(self) -> None:
        self.handle_method('PUT')

    def do_DELETE(self) -> None:
        self.handle_method('DELETE')


class RequestHandler(MethodsMixin, BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data = None
        self.query_params = None
        self.routes = kwargs.pop('routes')

        super().__init__(*args, **kwargs)

    def get_query_params(self):
        path = self.path.split('?')

        no_query_params = len(path) < 2
        if no_query_params:
            return {}

        query_params = parse_qs(path[1])
        return {
            key: value[0] if len(value) == 1 else value
            for key, value in query_params.items()
        }

    def get_route(self) -> tuple:
        for path, route in self.routes.items():
            match = re.match(path, self.path.split('?')[0])
            if match:
                return route, match.groupdict()
        return None, {}

    def _get_payload(self) -> dict:
        payload_length = int(self.headers.get('Content-Length'))
        payload = self.rfile.read(payload_length)
        return json.loads(payload)

    def send_response(self, code: int, message: str = None) -> None:
        super().send_response(code, message)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def send_body(self, content: dict) -> None:
        self.wfile.write(json.dumps(content).encode())

    def send_not_found_response(self) -> None:
        self.send_response(404)
        self.send_body({'detail': 'Not found'})

    def handle_method(self, method: str) -> None:
        route, kwargs = self.get_route()
        if route is None:
            self.send_not_found_response()
            return

        if method == 'HEAD':
            self.send_response(200)
            return

        if method not in route:
            self.send_response(405)
            self.send_body({'detail': 'Method "{}" is not allowed'.format(method)})
            return

        self.query_params = self.get_query_params()
        if method in METHODS_WITH_BODY:
            self.data = self._get_payload()

        view = route[method]
        response = view(self, **kwargs)
        content, status_code = response if isinstance(response, tuple) else (response, 200)

        self.send_response(status_code)
        if content is not None:
            self.send_body(content)
