# Based on a tutorial
import math
import random


class Player:
    def __init__(self, letter):
        self.letter = letter


class RandomComputer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class GeniusComputer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)["position"]
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.winner == other_player:
            return {"position": None,
                    "score": 1 * (state.num_empty_squares() + 1) if other_player == max_player
                    else -1 * (state.num_empty_squares() + 1)
                    }

        elif not state.empty_squares():
            return {"position": None, "score": 0}

        if player == max_player:
            best = {"position": None, "score": -math.inf}
        else:
            best = {"position": None, "score": math.inf}

        for possible_move in state.available_moves():
            # Step 1: try a move
            state.make_move(possible_move, player)
            # Step 2: check with minimax
            sim_score = self.minimax(state, other_player)
            # Step 3: undo the move
            state.board[possible_move] = " "
            state.winner = None
            sim_score["position"] = possible_move
            # Step 4: update dictionaries if necessary
            if player == max_player:  # This maximizes the max player
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:  # This minimizes the other player
                if sim_score["score"] < best["score"]:
                    best = sim_score
        return best


class Human(Player):
    def __init__(self, letter):
        super().__init__(letter)

    # Checks if the desired square is real and available. If so, returns it as the next desired move.
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move 0-8: ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
            except ValueError:
                print("Invalid square! Please try again.")

            return val
