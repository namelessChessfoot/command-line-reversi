import warnings

warnings.filterwarnings("ignore")
from network import Network
import argparse
from modules.chat_module import ChatModule
from modules.connect_module import ConnectModule
from modules.reversi_module import ReversiModule


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5678)
    args = parser.parse_args()
    modules = [ConnectModule, ChatModule]
    network = Network(args.port, modules)

    while True:
        print("Options:")
        mods = network.get_modules()
        l = len(mods)
        for i in range(l):
            print(f" >> {i}. {mods[i].get_action()}")
        try:
            ans = int(input("Your choice: "))
            if 0 <= ans < l:
                mod = mods[ans]
                req_body = mod.make_request()
                req_body["ACTION"] = mod.get_action()
                network.send(req_body, mod.handle_response)
        except Exception as e:
            pass
