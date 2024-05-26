from .base_module import BaseModule

from random import randint


class ConnectModule(BaseModule):
    def __init__(self, network) -> None:
        super().__init__(network)
        self.action = "CONNECT"

    def make_request(self):
        self.network.peer = input("Whom do you want to connect to? ")
        message = input("Say something to your peer? ")
        self.rand = randint(0, 10000)
        return {
            "rand": self.rand,
            "message": message,
            "addr": f"{self.network.ipv4}:{self.network.port}",
        }

    def handle_request(self, req_body):
        if self.network.secret == -1:
            idea = input(
                f"Someone wants to connect and leaves the following message:\n[{req_body['message']}]\nType in [yes] to accept\n"
            )
            if idea == "yes":
                my_rand = randint(0, 10000)
                peer_rand = req_body["rand"]
                self.network.secret = my_rand + peer_rand
                self.network.peer = req_body["addr"]
                self.network.print_status()
                return my_rand
        return -1

    def handle_response(self, content):
        peer_rand = int(content)
        if peer_rand == -1:
            self.network.peer = "Unknown"
            print("Connection failed")
        else:
            self.network.secret = self.rand + int(content)
            print("Connection succeeded")
        self.network.print_status()

    def auth_on(self):
        return False
