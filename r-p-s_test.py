import random

replay = True
yes = ("y", "yes")
no = ("n", "no")


def play():
    user = input("Select rock, paper, or scissors.\n").lower()
    computer = random.choice(("rock", "paper", "scissors"))

    if user == computer:
        print("It's a tie")

    elif is_win(user, computer):
        print("You won!")

    else:
        print("You lost...")


def is_win(player, opponent):
    if (player == "rock" and opponent == "scissors") or (player == "scissors" and opponent == "paper") \
            or (player == "paper" and opponent == "rock"):
        return True


while replay:
    play()
    again = ""
    while again == "":
        again = input("Would you like to play again? ").lower()
        if again in no:
            print("Thanks for playing!")
            replay = False
        elif again not in yes:
            print("I'm sorry, I didn't understand that.")
