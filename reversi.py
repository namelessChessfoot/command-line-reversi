import warnings

warnings.filterwarnings("ignore")
from network import Network
import argparse
import json


def handle_chat(req_body):
    print(f"        From peer: {req_body['message']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5678)
    args = parser.parse_args()
    network = Network(args.port, [["CHAT", handle_chat]])
    network.connect(input("who?"))
    while True:
        msg = input()
        network.send({"ACTION": "CHAT", "message": msg})
