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
