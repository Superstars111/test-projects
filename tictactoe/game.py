# Based on a tutorial
from player import Human, RandomComputer, GeniusComputer
import time


class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.winner = None

    # Prints the board. This should be called after each turn.
    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    # Prints the board with numbers in the squares. This should only be called once at the beginning.
    @staticmethod
    def print_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    # Tracks which squares have been taken and which are still available.
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
        # Tutorial says that this is a longer version of the same thing
        # moves = []
        # for (i, spot) in enumerate(self.board):
        #    if spot == " ":
        #        moves.append(i)
        # return moves

    # I think this checks to see if there are any blank squares left, but I'm not sure how the syntax works
    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return len(self.available_moves())
        # Or return self.board.count(" ")

    # Replaces an empty square with the given letter. Also calls a function to check if it was a winning move.
    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.won_game(square, letter):
                self.winner = letter
            return True
        return

    # Checks to see if there are three in a row
    def won_game(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


def play(game, x, o, print_game=True):

    if print_game:
        game.print_nums()

    letter = "X"
    while game.empty_squares():
        if letter == "O":
            square = o.get_move(game)
        else:
            square = x.get_move(game)

        # I believe this should always return True. One return specifies it, and the other doesn't.
        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print("")

            if game.winner:
                if print_game:
                    print(letter + " wins!")
                return "O" if letter == "O" else "X"

            letter = "O" if letter == "X" else "X"

        if print_game:
            time.sleep(0.8)

    if print_game:
        print("It's a tie...")


# Plays and replays the game until no longer desired
replay = True
while replay:

    if __name__ == "__main__":

        t = TicTacToe()
        x_player = Human("X")
        o_player = Human("O")
        mode = input("How many players would you like? 1, 2, or a simulation (sim)? ").lower()
        if mode == "2":
            play(t, Human("X"), Human("O"), print_game=True)

        elif mode == "1":
            level = input("Would you like to play against the random computer (r), "
                          "or the genius computer (g)? ").lower()
            order = input("Would you like to be X or O? ").lower()
            if level == "r" and order == "x":
                play(t, Human("X"), RandomComputer("O"), print_game=True)

            elif level == "r" and order == "o":
                play(t, RandomComputer("X"), Human("O"), print_game=True)

            elif level == "g" and order == "x":
                play(t, Human("X"), GeniusComputer("O"), print_game=True)

            elif level == "g" and order == "o":
                play(t, GeniusComputer("X"), Human("O"), print_game=True)

            elif level not in ("r", "g") or order not in ("x", "o"):
                print("I'm sorry, I didn't understand your choices. Please use single letters.")

        elif mode == "sim":
            sim_count = input("How many simulations would you like to run? (High numbers may take a while.) ")
            try:
                int(sim_count)
            except ValueError:
                print("Please input an integer.")
            sim_type = input("Would you like two genius computers (g), "
                             "two random computers (r), or one of each (both)? ").lower()
            if sim_type == "g":
                x_player = GeniusComputer("X")
                o_player = GeniusComputer("O")

            elif sim_type == "r":
                x_player = RandomComputer("X")
                o_player = RandomComputer("O")

            elif sim_type == "both":
                sim_order = input("Would you like the Genius to be X or O? ").lower()
                if sim_order == "x":
                    x_player = GeniusComputer("X")
                    o_player = RandomComputer("O")

                elif sim_order == "o":
                    x_player = RandomComputer("X")
                    o_player = GeniusComputer("O")

                elif sim_order not in ("x", "o"):
                    print("I'm sorry, I didn't understand that.")

            elif sim_type not in ("g", "r", "both"):
                print("I'm sorry, I didn't understand that.")

            if sim_type in ("g", "r", "both"):
                x_wins = 0
                o_wins = 0
                ties = 0
                for test in range(int(sim_count)):
                    result = play(TicTacToe(), x_player, o_player, print_game=False)
                    if result == "X":
                        x_wins += 1
                    elif result == "O":
                        o_wins += 1
                    else:
                        ties += 1

                print(f"X won {x_wins} times, O won {o_wins} times, and there were {ties} ties.")

        endgame = ""
        while endgame == "":
            yes = ("y", "yes")
            no = ("n", "no")
            endgame = input("Would you like to play again? ").lower()

            if endgame in no:
                print("Thanks for playing!")
                replay = False

            elif endgame not in (yes or no):
                print("I'm sorry, I didn't understand that.")
                endgame = ""
