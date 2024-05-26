import warnings

warnings.filterwarnings("ignore")
import socket
import requests
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class Network:
    def __init__(self, port, module_constructors) -> None:

        self.modules = []
        callbacks = {}
        for cons in module_constructors:
            mod = cons(self)
            self.modules.append(mod)
            func = mod.handle_request
            if mod.auth_on():

                def with_auth(req_body):
                    if (
                        self.secret == -1
                        or "secret" not in req_body
                        or self.secret != req_body["secret"]
                    ):
                        print("Auth failed")
                        return -2
                    return func(req_body)

                callbacks[mod.get_action()] = with_auth
            else:
                callbacks[mod.get_action()] = func

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
                action = req_body["ACTION"]
                if action in callbacks:
                    self.wfile.write(json.dumps(callbacks[action](req_body)).encode())
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

    def get_modules(self):
        return self.modules

    def print_status(self):
        print()
        print(f"Listening to {self.ipv4}:{self.port} with secret {self.secret}")
        print(f"Send to {self.peer} with secret {self.secret}")
        print()

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
