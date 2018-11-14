import json
import re
from http.server import BaseHTTPRequestHandler

from app.routes import routes

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
        super().__init__(*args, **kwargs)

        self.data = None

    def get_route(self) -> tuple:
        for path, route in routes.items():
            match = re.match(path, self.path)
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

        if method in METHODS_WITH_BODY:
            self.data = self._get_payload()

        view = route[method]
        response = view(self, **kwargs)
        content, status_code = response if isinstance(response, tuple) else (response, 200)

        self.send_response(status_code)
        if content is not None:
            self.send_body(content)
