import warnings

warnings.filterwarnings("ignore")
from network import Network
import argparse
import json
from modules.chat_module import ChatModule


# def handle_chat(req_body):
#     print(f"        From peer: {req_body['message']}")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--port", type=int, default=5678)
#     args = parser.parse_args()
#     network = Network(args.port, [["CHAT", handle_chat]])
#     network.connect(input("who?"))
#     while True:
#         msg = input()
#         network.send({"ACTION": "CHAT", "message": msg})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5678)
    args = parser.parse_args()
    modules = [ChatModule()]
    callbacks = []
    for mod in modules:
        callbacks.append([mod.get_action(), mod.handle_request])
    network = Network(args.port, callbacks)
    network.connect(input("who?"))

    while True:
        print("Options:")
        l = len(modules)
        for i in range(l):
            print(f" >> {i}. {modules[i].get_action()}")
        try:
            ans = int(input("Your choice: "))
            if 0 <= ans < l:
                mod = modules[ans]
                req_body = mod.make_request()
                req_body["ACTION"] = mod.get_action()
                network.send(req_body, mod.handle_response)
        except Exception as e:
            continue
