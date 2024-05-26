from .base_module import BaseModule


class ChatModule(BaseModule):
    def __init__(self, network) -> None:
        super().__init__(network)
        self.action = "CHAT"

    def make_request(self):
        msg = input("Say something to your peer: ")
        return {"message": msg}

    def handle_request(self, req_body):
        print(f"        Your peer: {req_body['message']}")
        return

    def handle_response(self, content):
        pass
