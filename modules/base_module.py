class BaseModule:
    def __init__(self, network) -> None:
        self.action = "base"
        self.network = network

    def get_action(self):
        return self.action

    def handle_request(self, req_body):
        raise NotImplementedError()

    def handle_response(self, content):
        pass

    def make_request(self):
        raise NotImplementedError()

    def auth_on(self):
        return True
