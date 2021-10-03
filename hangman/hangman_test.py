import random
import string

from hangwords import words


# This checks to make sure that the word chosen doesn't have any non real letters.
# For example, "x-ray," which is in the list of given words.
def get_valid_word():
    chosen = random.choice(words)
    while ("-" or " ") in chosen:
        chosen = random.choice(words)

    return chosen.upper()


# This allows the actual game itself to be played
def hangman():
    chosen = get_valid_word()  # This is the word the computer has chosen
    word_letters = set(chosen)  # The letters in the chosen word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # The letters the player has already guessed
    man = "0-<--<"
    death = ""

    attempts = 6

    # This section receives and checks player input
    while len(word_letters) > 0 and attempts > 0:
        print("You have", attempts, "attempts remaining.\n"
              "Guessed letters: ", " ".join(used_letters))  # Would like to be able to alphabetize these eventually
        visible_word = [letter if letter in used_letters else "_" for letter in chosen]
        print("Current word: ", " ".join(visible_word))

        player_letter = input("Guess a letter: ").upper()
        if player_letter in alphabet - used_letters:
            used_letters.add(player_letter)
            if player_letter in word_letters:
                word_letters.remove(player_letter)

            else:
                attempts = attempts - 1
                death = death + man[:1]
                man = man[1:]
                print("Wrong guess!", death)  # May want to add 0-<--< later

        elif player_letter in used_letters:
            print("You already guessed that letter!")

        else:
            print("That's not a real letter... At least not in this language. Sorry.")

    if attempts == 0:
        print(f"Alas, you are dead. The word was {chosen}")
    else:
        print(f"You won! The correct word was {chosen}!")


replay = True
while replay:
    hangman()
    again = ""
    yes = ("y", "yes")
    no = ("n", "no")
    while again == "":
        again = input("Would you like to play again? ").lower()
        if again in no:
            print("Thanks for playing!")
            replay = False
        elif again not in yes:
            print("I'm sorry, I didn't understand that.")
