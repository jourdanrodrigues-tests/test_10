from functools import partial
from http.server import HTTPServer

from app.routes import routes
from core.environment import PORT
from core.request import RequestHandler

if __name__ == '__main__':
    http_server = HTTPServer(
        ('', PORT),
        partial(RequestHandler, routes=routes),
    )

    print('Starting HTTP server at port {}'.format(PORT))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass

    print('Stopping HTTP server')
    http_server.server_close()
