from functools import partial
from http.server import HTTPServer

from app.routes import routes
from core.environment import PORT
from core.request import RequestHandler


def initialize_server(port: int) -> None:
    http_server = HTTPServer(
        ('', port),
        partial(RequestHandler, routes=routes),
    )

    print('Starting HTTP server at port {}'.format(port))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass

    print('Stopping HTTP server')
    http_server.server_close()


if __name__ == '__main__':
    initialize_server(PORT)
