import random


def generator(x):
    random_number = random.randint(1, x)
    guess = 0
    attempts = 0
    while guess != random_number:
        guess = int(input(f"Guess a number between 1 and {x}: "))
        if guess < random_number:
            print("Sorry, guess again! That's too low.")
            attempts += 1
        elif guess > random_number:
            print("Sorry, guess again! That's too high.")
            attempts += 1
        elif guess == random_number:
            attempts += 1

    print(f"Congratulations! The correct number was {random_number}! That took you {attempts} tries.")


generator(int(input("Generate a number between 1 and...?: ")))
