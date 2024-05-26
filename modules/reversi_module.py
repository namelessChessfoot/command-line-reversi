from .base_module import BaseModule
import json


class ReversiModule(BaseModule):
    INVALID = -1
    NEW_GAME = 0
    PUT = 1

    def __init__(self, network) -> None:
        super().__init__(network)
        self.action = "REVERSI"
        self.board = None

    def make_request(self):
        if self.board == None:
            return {"event": "new_game"}
        position = list(
            map(int, input("Where you would like to put (like 2,3)? ").split(","))
        )
        print(position)
        self.position_attempt = position
        return {"event": "put", "position": position}

    def handle_request(self, req_body):
        event = req_body["event"]
        if event == "new_game":
            if self.board:
                return self.INVALID
            self.board = Board()
            self.board.print()
            return self.NEW_GAME
        elif event == "put":
            res = self.board.put(*req_body["position"])
            self.board.print()
            return self.PUT if res else self.INVALID
        return self.INVALID

    def handle_response(self, content):
        status_code = int(content)
        if status_code == self.NEW_GAME:
            self.board = Board()
        elif status_code == self.PUT:
            self.board.put(*self.position_attempt)
        else:
            print("Something went WRONG!!")
        self.board.print()


class Board:
    VAC = 0
    BLACK = 1
    WHITE = 2
    DISPLAY = [".", "B", "W"]

    def __init__(self) -> None:
        self.board = [[self.VAC] * 8 for _ in range(8)]
        self.board[3][3] = self.board[4][4] = self.WHITE
        self.board[4][3] = self.board[3][4] = self.BLACK
        self.hint = None
        self.cur = self.BLACK
        self.pre_process()

    def pre_process(self):
        self.hint = []
        for i in range(8):
            self.hint.append([])
            for j in range(8):
                self.hint[-1].append(self.if_put(i, j))

    def print(self):
        print("\\ ", end="")
        for c in range(8):
            print(c, end=" ")
        print()
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.get_hint()[i][j]:
                    print("*", end=" ")
                else:
                    print(self.DISPLAY[self.board[i][j]], end=" ")
            print()

    def range_check(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def get_opponent(self):
        return self.BLACK + self.WHITE - self.cur

    def if_put(self, x, y):
        ret = []
        oppo = self.get_opponent()
        if self.range_check(x, y) and self.board[x][y] == self.VAC:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    ops = []
                    nx = x + dx
                    ny = y + dy
                    while self.range_check(nx, ny) and self.board[nx][ny] == oppo:
                        ops.append([nx, ny])
                        nx += dx
                        ny += dy
                    if self.range_check(nx, ny) and self.board[nx][ny] == self.cur:
                        ret.extend(ops)
        return ret

    def get_hint(self):
        if not self.hint:
            self.pre_process()
        return self.hint

    def put(self, x, y):
        if not self.range_check(x, y) or not len(self.get_hint()[x][y]):
            return False
        for i, j in self.get_hint()[x][y]:
            self.board[i][j] = self.cur
        self.board[x][y] = self.cur
        self.hint = None
        self.cur = self.get_opponent()
        return True


# b = Board()
# while True:
#     b.print()
#     param = map(int, input().split(","))
#     b.put(*param)
