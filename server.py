import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = os.getenv('PORT', 8080)

if __name__ == '__main__':
    http_server = HTTPServer(('', PORT), BaseHTTPRequestHandler)
    print('Starting HTTP server at port {}'.format(PORT))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()
