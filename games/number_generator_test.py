import random

finished = False


def generator(x):
    random_number = random.randint(1, x)
    guess = 0
    attempts = 0
    while guess != random_number:
        guess = int(input(f"Guess a number between 1 and {x}: "))
        if guess < random_number:
            print("Sorry, guess again! That's too low.")
        elif guess > random_number:
            print("Sorry, guess again! That's too high.")
        attempts += 1

    print(f"Congratulations! The correct number was {random_number}! That took you {attempts} tries.")


def comp_guesser(low, high):
    feedback = ""
    attempts = 0
    while feedback != "C":
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low  # It doesn't matter whether this is low or high.
        feedback = input(f"Is {guess} too high (H), too low (L), or correct (C)? ").upper()
        if feedback == "H":
            high = guess - 1
        elif feedback == "L":
            low = guess + 1
        attempts += 1

    print(f"Yay! That's another victory for the computer! Your number was {guess}. That took me {attempts} tries.")


while finished is False:
    mode = input("Would you like to guess a number (guess), "
                 "or choose a number for the computer to guess (choose)? ").lower()
    if mode == "guess":
        generator(int(input("Generate a number between 1 and...?: ")))
    elif mode == "choose":
        comp_guesser(int(input("Choose the lower boundry for the computer to guess. ")),
                     int(input("Choose the upper boundry for the computer to guess. ")))
    elif mode != "guess" or "choose":
        print("I'm sorry, I didn't understand that.")
    gameend = "blank"
    while gameend == "blank":
        gameend = input("Would you like to play again? Y/N: ").upper()
        if gameend == "N":
            print("Thank you for playing!")
            finished = True
        elif gameend != "Y":
            print("I'm sorry, I didn't understand that.")
            gameend = "blank"
