from functools import partial
from http.server import HTTPServer

from app.routes import routes
from core.environment import PORT
from core.request import RequestHandler


def get_http_server(port: int) -> HTTPServer:
    return HTTPServer(
        ('', port),
        partial(RequestHandler, routes=routes),
    )


if __name__ == '__main__':
    server = get_http_server(PORT)

    print('Starting HTTP server at port {}'.format(PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('Stopping HTTP server')
        server.server_close()
