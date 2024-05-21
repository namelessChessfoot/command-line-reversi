from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def get_body(self):
        content_len = int(self.headers.get("Content-Length"))
        return self.rfile.read(content_len)

    def do_GET(self):
        pass

    def do_POST(self):
        print(self.get_body())


httpserver = HTTPServer(("", 5678), MyHandler)
httpserver.serve_forever()
