import json
import re

with open("options.json", "r") as option_list:
    options = json.load(option_list)

feelings = [
    "adventure",
    "chance",
    "combat",
    "comedy",
    "creative",
    "dice",
    "discovery",
    "fast",
    "fighting",
    "group",
    "mystery",
    "party",
    "puzzle",
    "race",
    "sim",
    "strategy",
    "teams",
    "trivia",
]


# Adds a game to the library
def add_game(add_num):

    for i in range(add_num):
        game = {
            "title": "game",
            "vetoedBy": [],
            "favoredBy": [],
            "loweredBy": [],
            "type": [],
            "feel": [],
            "shared": False,
            "players": [],
            "idealPlayers": [],
            "copyPlayers": 1,
            "compType": [],
            "ownedBy": [],
            "length": [],
            "turns": [],
            "points": 0
        }

        game["title"] = input("What is this game's title? ")  # Title collection

        cont = True  # Veto collection
        while cont:
            player = input("Is there anyone who will refuse to play this game? Put their name here. "
                           "When you're done, type done. ").title()
            if player == "Done":
                cont = False
            else:
                game["vetoedBy"].append(player)

        cont = True  # Favored collection
        while cont:
            player = input("Does anyone especially like this game? Put their name here. "
                           "When you're done, type done. ").title()
            if player == "Done":
                cont = False
            else:
                game["favoredBy"].append(player)

        cont = True  # Lowered collection
        while cont:
            player = input("Does anyone lean against this game? Put their name here. "
                           "When you're done, type done. ").title()
            if player == "Done":
                cont = False
            else:
                game["loweredBy"].append(player)

        cont = True  # Type collection
        while cont:
            gameType = input("Is this a video game, a board game, or a card game? ").lower()
            if gameType == "video":
                game["type"] = ["video"]
                cont = False
            elif gameType == "board":
                game["type"] = ["board"]
                cont = False
            elif gameType == "card":
                game["type"] = ["card"]
                cont = False
            else:
                print("I'm sorry, I didn't understand that. Please type video, board, or card.")

        cont = True  # Feel collection
        while cont:
            style = input("What is the \"feel\" of this game? "
                          "For a list, type list. When you're done, type done. ").lower()
            if style in feelings:
                game["feel"].append(style)

            elif style == "list":
                for num, feeling in enumerate(feelings, start=1):
                    if num != len(feelings):
                        print(feeling + ", ", end="")
                    else:
                        print(feeling, end="")
                    if num % 4 == 0:
                        print()
                print()

            elif style == "done":
                if not game["feel"]:
                    print("Please choose at least one feel for each game.")
                else:
                    cont = False

            else:
                print("I'm sorry, I didn't understand that.")

        if game["type"] == "video":  # Shared collection
            shared = input("Can multiple people play with just one copy of this game? Yes or no. ").lower()
            if shared in ("yes", "y"):
                game["shared"] = True
        else:
            game["shared"] = True

        play_count = re.split(r",\s*", input("How many players can play? Please split with a comma. ex. 2, 3, 4, 6 "))
        for i in play_count:
            game["players"].append(int(i))

        ideal_count = re.split(r",\s*",
                               input("What would be the perfect amount of players for this game? ex. 2, 5, 6 "))
        for i in ideal_count:
            if i in play_count:
                game["idealPlayers"].append(int(i))

        if game["shared"]:  # Max copy players collection
            if game["type"] in (["board"], ["card"]):
                game["copyPlayers"] = max(game["players"])
            else:
                game["copyPlayers"] = int(input("What is the maximum number of people who can play "
                                                "with one copy of this game? "))
        else:
            game["copyPlayers"] = 1

        cont = True  # Competition collection
        while cont:
            comp = input("Is this game pvp, co-op, or both? ").lower()
            if comp == "pvp":
                game["compType"] = ["pvp"]
                cont = False
            elif comp == "co-op":
                game["compType"] = ["co-op"]
                cont = False
            elif comp == "both":
                game["compType"] = ["pvp", "co-op"]
                cont = False
            else:
                print("I'm sorry, I didn't understand that. Please input pvp, co-op, or both.")

        cont = True  # Owner collection
        while cont:
            player = input("Who owns this game? "
                           "If this is a Curry family game, type family. When you're done, type done. ").title()
            if player == "Done":
                cont = False
            elif player == "Family":
                for member in ["Dad", "Mom", "Jared", "Hannah", "Simon", "Kenan", "Micah"]:
                    game["ownedBy"].append(member)
            else:
                game["ownedBy"].append(player)

        cont = True  # Turn style collection
        while cont:
            turns = input("Is this game turn-based, or real-time? ").lower()
            if turns == "turn-based":
                game["turns"] = ["turnBased"]
                cont = False
            elif turns == "real-time":
                game["turns"] = ["realTime"]
                cont = False
            else:
                print("I'm sorry, I didn't understand that.")

        options.append(game)
        print()


# Checks the status of a game already in the library
def check_game(title):
    match = None
    for game in options:
        if title == game["title"].lower():
            match = game

    if match:
        print_game = input("I've found a game with that title! Would you like to see it? ").lower()
        if print_game in ("yes", "y"):
            for field in match:
                print(f"{field}: {match[field] if match[field] else ''}")
            print()

    else:
        print("I'm sorry, I couldn't find that game in our library.")


def edit_game(title):
    match = None
    for game in options:
        if title == game["title"].lower():
            match = game

    if match:
        edit_style = input("What would you like to do with this entry?\n"
                           "(1) Add a player to the vetoed, favored, lowered, or owners category\n"
                           "(2) Remove a player from one of the above categories\n"
                           "(3) Correct the game's technical information\n").lower()

        if edit_style in ("1", "add"):
            category = input("Which category would you like to add to?\n"
                             "(1) Veto\n"
                             "(2) Favored\n"
                             "(3) Lowered\n"
                             "(4) Owned\n").lower()
            if category in ("1", "veto"):
                veto = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if veto in match["vetoedBy"]:
                    print("That person has already vetoed this game!")
                else:
                    match["vetoedBy"].append(veto)

            elif category in ("2", "favored"):
                favor = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if favor in match["favoredBy"]:
                    print("That person already favors this game!")
                else:
                    match["favoredBy"].append(favor)

            elif category in ("3", "lowered"):
                lower = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if lower in match["loweredBy"]:
                    print("That person already lowers this game!")
                else:
                    match["loweredBy"].append(lower)

            elif category in ("4", "owned"):
                owner = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if owner in match["ownedBy"]:
                    print("That person already owns this game!")
                else:
                    match["ownedBy"].append(owner)

            else:
                print("I'm sorry, I didn't understand that.")

        elif edit_style in ("2", "remove"):
            category = input("Which category would you like to remove from?\n"
                             "(1) Veto\n"
                             "(2) Favored\n"
                             "(3) Lowered\n"
                             "(4) Owned\n").lower()
            if category in ("1", "veto"):
                veto = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if veto in match["vetoedBy"]:
                    match["vetoedBy"].remove(veto)
                else:
                    print("That person hasn't vetoed this game!")

            elif category in ("2", "favored"):
                favor = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if favor in match["favoredBy"]:
                    match["favoredBy"].remove(favor)
                else:
                    print("That person hasn't favored this game!")

            elif category in ("3", "lowered"):
                lower = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if lower in match["loweredBy"]:
                    match["loweredBy"].remove(lower)
                else:
                    print("That person hasn't lowered this game!")

            elif category in ("4", "owned"):
                owner = input("Please put the first name or common title (e.g. \"Dad\") here. ").title()
                if owner in match["ownedBy"]:
                    match["ownedBy"].remove(owner)
                else:
                    print("That person doesn't own this game!")

            else:
                print("I'm sorry, I didn't understand that.")

        elif edit_style in ("3", "correct"):
            field = input("Which field needs to be corrected?\n"
                          "(1) Title\n"
                          "(2) Type\n"
                          "(3) Feel\n"
                          "(4) Shared\n"
                          "(5) Players\n"
                          "(6) Ideal number of players\n"
                          "(7) Copy players supported\n"
                          "(8) Competition type\n"
                          "(9) Length\n"
                          "(10) Turn style\n").lower()

            if field in ("1", "title"):
                new_title = input("Please input the correct full title for this game. "
                                  "Be sure to pay attention to capitalization and punctuation. ")
                trigger = False
                for game in options:
                    if new_title == game["title"]:
                        print("A game already exists with that title!")
                        trigger = True
                if not trigger:
                    match["title"] = new_title

            elif field in ("2", "type"):
                new_type = input("What type of game is this? Video, board, or card? ").lower()
                if new_type in ("video", "board", "card"):
                    match["type"] = [new_type]
                else:
                    print("Please input a valid game type.")

            elif field in ("3", "feel"):
                add_rem = input("Do you need to add or remove a feel from this game? ").lower()
                if add_rem == "add":
                    feel = input("Which feeling do you need to add? For a list, type list. ").lower()
                    if feel == "list":
                        for idx, feeling in enumerate(feelings, start=1):
                            if idx != len(feelings):
                                print(feeling + ", ", end="")
                            else:
                                print(feeling)
                            if idx % 4 == 0:
                                print()

                    else:
                        if feel in feelings:
                            if feel not in match["feel"]:
                                match["feel"].append(feel)
                            else:
                                print("This game already has that feeling assigned to it.")
                        else:
                            print("That is not in the list of approved feelings. Sorry. Please feel better.")

                elif add_rem == "remove":
                    feel = input("Which feeling do you need to remove? For a list, type list. ").lower()
                    if feel == "list":
                        for idx, feeling in enumerate(feelings, start=1):
                            if idx != len(feelings):
                                print(feeling + ", ", end="")
                            else:
                                print(feeling)
                            if idx % 4 == 0:
                                print()

                    else:
                        if feel in feelings:
                            if feel not in match["feel"]:
                                print("This game doesn't have that feeling assigned to it.")
                            else:
                                match["feel"].remove(feel)
                        else:
                            print("That is not in the list of approved feelings. Sorry. Please feel better.")
                else:
                    print("*Sigh...* What's so difficult about typing add or remove?")

            elif field in ("4", "shared"):
                pass

            elif field in ("5", "players"):
                pass

            elif field in ("6", "ideal"):
                pass

            elif field in ("7", "copy"):
                pass

            elif field in ("8", "competition"):
                pass

            elif field in ("9", "length"):
                pass

            elif field in ("10", "turn"):
                pass

            else:
                print("I'm sorry, I didn't understand that.")



    else:
        print("I'm sorry, I couldn't find that game in our library.")


def list_games():
    pass


if __name__ == "__main__":
    repeat = True
    while repeat:
        mode = input("Welcome! How may I be of assistance today? (Select a number or the first word)\n"
                     "(1) Add a game\n"
                     "(2) Check the library for an existing game\n"
                     "(3) Edit a game's entry\n"
                     "(4) List all games\n"
                     "(5) End program\n").lower()

        if mode in ("1", "add"):
            add = input("How many games would you like to add today? Please input an integer. ")
            add_game(int(add))

        elif mode in ("2", "check"):
            check = input("Which game would you like to check? "
                          "Please make sure the title is exact, including and punctuation. ").lower()
            check_game(check)

        elif mode in ("3", "edit"):
            alter = input("Which game would you like to edit? "
                          "Please make sure the title is exact, including and punctuation. ").lower()
            edit_game(alter)

        elif mode in ("4", "list"):
            list_games()

        elif mode in ("5", "end"):
            repeat = False
            break

        else:
            print("I'm sorry, I didn't understand that.")
            continue

        again = input("Will that be all today? ").lower()
        if again in ("yes", "y"):
            repeat = False


with open("options.json", "w") as file:
    json.dump(options, file, indent=4)
