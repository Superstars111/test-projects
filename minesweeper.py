# Built based on a tutorial from freeCodeCamp.org

import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Making the board
        self.board = self.make_board()
        self.board_val()

        # Keeping track of where we've dug
        self.dug = set()

    # This will make a new board based on the number of bombs and the size
    def make_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                continue

            board[row][col] = "*"
            bombs_planted += 1

        return board

    # Assigns numbers 0-8 to all empty spaces
    def board_val(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num(r, c)

    # Determines the number of bombs near a specific square
    def get_num(self, row, col):
        num_near_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size, (col+1) + 1)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    num_near_bombs += 1
        return num_near_bombs

    def dig(self, row, col):
        self.dug.add((row, col))  # Remembers that we've dug here before

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size, (col+1) + 1)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        # This is where she stopped explaining what she was doing
                string_rep = ""

        # Her notes say that this gets the max widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # This builds the numbers at the top that label the columns
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        # Yeah... No clue how this part works
        for idx, col in enumerate(indices):
            form = "%-" + str(widths[idx]) + "s"
            cells.append(form % col)
        indices_row += "  ".join(cells)
        indices_row += " \n"

        # This part builds the grid into a single string. ...Not entirely sure how.
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                form = "%-" + str(widths[idx]) + "s"
                cells.append(form % col)
            string_rep += " |".join(cells)
            string_rep += " |\n"

        # This builds the final string. Numbers at the top + dashes and \n + grid (including newlines) + more dashes.
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-"*str_len + "\n" + string_rep + "-"*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: Create board and place bombs
    board = Board(dim_size, num_bombs)

    # Step 2: Show board and ask where to dig

    # Step 3a: If location is a bomb, show game over
    # Step 3b: If location is not a bomb, automatically dig until each square is next to a bomb
    # Step 4: Repeat 2 and 3 until there are no places left to dig
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # Regex splits at the comma followed by any whitespace
        dig_loc = re.split(",(\\s)*", input("Where would you like to dig? r, c "))
        row, col = int(dig_loc[0]), int(dig_loc[-1])  # Takes the first and last options
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location!")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("Congrats! You won!")
    else:
        print("AAAAARGH! MAH LEG!")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == "__main__":
    play()
