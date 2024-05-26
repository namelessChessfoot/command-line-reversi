import warnings

warnings.filterwarnings("ignore")
import socket
import requests
import json
from random import randint

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class Network:
    def __init__(self, port, callbacks=[]) -> None:
        def handle_connect(req_body):
            if self.secret == -1:
                idea = input(
                    f"Someone wants to connect and leaves the following message:\n[{req_body['message']}]\nType in [yes] to accept\n"
                )
                if idea == "yes":
                    my_rand = randint(0, 10000)
                    peer_rand = req_body["rand"]
                    self.secret = my_rand + peer_rand
                    self.peer = req_body["addr"]
                    self.print_status()
                    return my_rand
            return -1

        for i in range(len(callbacks)):
            func = callbacks[i][1]

            def with_auth(req_body):
                if (
                    self.secret == -1
                    or "secret" not in req_body
                    or self.secret != req_body["secret"]
                ):
                    print("Auth failed")
                    return -2
                return func(req_body)

            callbacks[i][1] = with_auth
        callbacks.append(["CONNECT", handle_connect])

        class MyHandler(BaseHTTPRequestHandler):
            def __init__(self, request, client_address, server):
                super().__init__(request, client_address, server)

            def get_body(self):
                content_len = int(self.headers.get("Content-Length"))
                return self.rfile.read(content_len)

            def do_POST(self):
                self.send_response(200)
                self.end_headers()
                req_body = json.loads(self.get_body().decode())
                for action, func in callbacks:
                    if action == req_body["ACTION"]:
                        self.wfile.write(json.dumps(func(req_body)).encode())
                        return
                self.wfile.write(b"Not supported")

            def log_message(self, format, *args):
                pass

        server_thread = Thread(target=HTTPServer(("", port), MyHandler).serve_forever)
        server_thread.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ipv4 = s.getsockname()[0]
        s.close()
        self.port = port
        self.peer = "Unknown"
        self.secret = -1
        self.print_status()

    def print_status(self):
        print()
        print(f"Listening to {self.ipv4}:{self.port} with secret {self.secret}")
        print(f"Send to {self.peer} with secret {self.secret}")
        print()

    def connect(self, peer, message="Hi, this is Keming Xu"):
        if len(peer) > 0:
            self.peer = peer
            my_rand = randint(0, 10000)

            def callback(content):
                peer_rand = int(content)
                if peer_rand == -1:
                    print("Connection failed")
                else:
                    self.secret = my_rand + int(content)
                    print("Connection succeeded")

            self.send(
                {
                    "ACTION": "CONNECT",
                    "rand": my_rand,
                    "message": message,
                    "addr": f"{self.ipv4}:{self.port}",
                },
                callback,
            )
        self.print_status()

    def send(self, data, callback=lambda rsp: 0):
        if self.peer == "Unknown":
            return
        try:
            data["secret"] = self.secret
            callback(
                requests.post(
                    f"http://{self.peer}", data=json.dumps(data)
                ).content.decode()
            )
        except Exception as e:
            print(e)
