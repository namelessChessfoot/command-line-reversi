import warnings

warnings.filterwarnings("ignore")
import requests

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import argparse


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def get_body(self):
        content_len = int(self.headers.get("Content-Length"))
        return self.rfile.read(content_len)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Good")

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        print("Post")
        print(self.get_body().decode())

    def log_message(self, format, *args):
        pass


def start_server(port):
    httpserver = HTTPServer(("", port), MyHandler)
    httpserver.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5678)
    args = parser.parse_args()
    st = Thread(target=start_server, args=[args.port])
    st.start()
    addr = input("Your peer's addr: ")
    while True:
        content = input("Say something to them: ")
        requests.post(f"http://{addr}", data=content)
