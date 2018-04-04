from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from cowpy import cow


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head><title>cowsay</title></head>')
            self.wfile.write(b'<body><header><nav><ul><li>')
            self.wfile.write(b'<a href="/cowsay">cowsay</a></li></ul></nav>')
            self.wfile.write(b'</header><main>Make a penguin talk</main>')
            self.wfile.write(b'</body></html>')
            return

        elif parsed_path.path == '/cowsay':
            cow_cls = cow.get_cow('tux')
            cheese = cow_cls()
            msg = cheese.milk(
                'Welcome to cowsay, if you want to play around with what I say'
                ' go to the end point of /cow?msg=text and replace text '
                'with whatever you want me to say.')
            msg = msg.encode('utf8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg)
            return

        elif parsed_path.path == '/cow':
            try:
                message = json.loads(parsed_qs['msg'][0])
            except KeyError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No bueno')
                return

            cow_cls = cow.get_cow('tux')
            cheese = cow_cls()
            msg = cheese.milk(message)
            msg = msg.encode('utf8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/cow':
            try:
                message = parsed_qs['msg'][0]
            except KeyError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No bueno')
                return

            cow_cls = cow.get_cow('tux')
            cheese = cow_cls()
            msg = cheese.milk(message)
            msg = json.dumps({"content": msg})
            msg = msg.encode('utf8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')


def create_server():
    return HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)


def run_forever():
    server = create_server()

    try:
        print('Starting server on port 3000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    run_forever()
