import json
import re
import string

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


# Adds or removes a player (or players) from a field- specifically, favoredBy, vetoedBy, loweredBy, and ownedBy
def alter_player(alt_type, target, rem=False):
    cont = True
    while cont:
        play_name = input("Please put the first name or common title (e.g. \"Dad\") here. "
                          "When you're done, type done. ").title()
        if play_name == "Done":
            break
        if rem:
            if play_name in target[alt_type]:
                target[alt_type].remove(play_name)
            else:
                print("That person isn't in this field!")
        else:
            if play_name in target[alt_type]:
                print("That person is already in this field!")
            elif play_name == "Family":
                for member in ["Dad", "Mom", "Jared", "Hannah", "Simon", "Kenan", "Micah"]:
                    if member not in target[alt_type]:
                        target[alt_type].append(member)
            else:
                target[alt_type].append(play_name)


def alphabetize(new_game, game_list):
    s = 0
    c = 0
    g = 0
    title_check = False
    spot = False
    while not spot:
        if not title_check:
            if len(game_list[g]["title"]) >= 4:
                if game_list[g]["title"] == "The Game of LIFE":
                    c = c + 12
                elif game_list[g]["title"][0:2] == "A ":
                    c = c + 2
                elif game_list[g]["title"][0:4] == "The ":
                    c = c + 4

            if len(new_game["title"]) >= 4:
                if new_game["title"][0:4] == "The ":
                    s = s + 4
                elif new_game["title"][0:2] == "A ":
                    s = s + 2
            title_check = True

        if new_game["title"][s] in (string.punctuation, " "):
            s += 1
            continue
        if game_list[g]["title"][c] in (string.punctuation, " "):
            c += 1
            continue

        if g == len(game_list):
            # If you reach the end of the list, put it there
            game_list[g] = [new_game]
            spot = True
        elif s == len(new_game["title"]):
            # If you've found a title that encompasses this one, put this title right before that one
            game_list[g:g] = [new_game]
            spot = True
        elif c >= len(game_list[g]["title"]):
            game_list[g+1:g+1] = [new_game]
            spot = True
        elif new_game["title"][s].lower() > game_list[g]["title"][c].lower():
            # If you're still ahead of your alphabetic position, check the next game
            g += 1
            s = 0
            c = 0
            title_check = False
        elif new_game["title"][s].lower() == game_list[g]["title"][c].lower():
            s += 1
            c += 1
        elif new_game["title"][s].lower() < game_list[g]["title"][c].lower():
            game_list[g:g] = [new_game]
            spot = True


# Adds a new game to the library
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

        duplicate = False
        game["title"] = input("What is this game's title? Please be exact. ")  # Title collection
        for old_game in options:
            if old_game["title"] == game["title"]:
                duplicate = True
        if duplicate:
            print("That game already exist in the library!")
            break


        print("Is there anyone who will refuse to play this game?")  # Veto collection
        alter_player("vetoedBy", game)

        print("Does anyone especially like this game?")  # Favored collection
        alter_player("favoredBy", game)

        print("Does anyone lean against this game?")  # Lowered collection
        alter_player("loweredBy", game)

        cont = True  # Type collection
        while cont:
            game_type = input("Is this a video game, a board game, or a card game? ").lower()
            if game_type in ("video", "board", "card"):
                game["type"] = [game_type]
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

        # Player count collection
        cont = True
        while cont:
            play_count = re.split(r",\s*", input("How many players can play? Please split with a comma. ex. 2, 3, 4, 6"
                                                 "\n>> "))
            try:
                game["players"] = [int(i) for i in play_count]
                cont = False
            except TypeError:
                print("Please only use integers. If there are multiple, separate them with a comma.")

        # Ideal number of players collection
        if len(game["players"]) > 1:
            ideal_count = re.split(r",\s*", input("What would be the perfect amount of players for this game? ex. 2, 5, 6"
                                                  "\n>> "))
            for i in ideal_count:
                if i in play_count:
                    game["idealPlayers"].append(int(i))
        else:
            game["idealPlayers"] = game["players"]

        # Shared collection
        if game["type"] == ["video"]:
            shared = input("Can multiple people play with just one copy of this game? Yes or no. ").lower()
            if shared in ("yes", "y"):
                game["shared"] = True
        else:
            game["shared"] = True

        # Maximum players per copy collection
        if game["shared"]:
            if len(game["Players"]) > 1:
                if game["type"] in (["board"], ["card"]):
                    game["copyPlayers"] = max(game["players"])
                else:
                    game["copyPlayers"] = int(input("What is the maximum number of people who can play "
                                                    "with one copy of this game? "))
            else:
                game["copyPlayers"] = game["Players"]
        else:
            game["copyPlayers"] = 1

        cont = True  # Competition collection
        while cont:
            comp = input("Is this game pvp, co-op, or both? ").lower()
            if comp in ("pvp", "co-op"):
                game["compType"] = [comp]
                cont = False
            elif comp == "both":
                game["compType"] = ["pvp", "co-op"]
                cont = False
            else:
                print("I'm sorry, I didn't understand that. Please input pvp, co-op, or both.")

        print("Who owns this game? If this is a Curry family game, you can type family.")  # Owner collection
        alter_player("ownedBy", game)

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

        alphabetize(game, options)
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


# Takes an existing game and alters it
def edit_game(title):
    match = None
    for game in options:
        if title == game["title"].lower():
            match = game

    if match:
        edit_style = input("What would you like to do with this entry?\n"
                           "(1) Add a player to the vetoed, favored, lowered, or owners category\n"
                           "(2) Remove a player from one of the above categories\n"
                           "(3) Correct the game's technical information\n"
                           ">> ").lower()

        if edit_style in ("1", "add"):
            category = input("Which category would you like to add to?\n"
                             "(1) Veto\n"
                             "(2) Favored\n"
                             "(3) Lowered\n"
                             "(4) Owned\n"
                             ">> ").lower()
            if category in ("1", "veto"):
                alter_player("vetoedBy", match)

            elif category in ("2", "favored"):
                alter_player("favoredBy", match)

            elif category in ("3", "lowered"):
                alter_player("loweredBy", match)

            elif category in ("4", "owned"):
                alter_player("ownedBy", match)

            else:
                print("I'm sorry, I didn't understand that.")

        elif edit_style in ("2", "remove"):
            category = input("Which category would you like to remove from?\n"
                             "(1) Veto\n"
                             "(2) Favored\n"
                             "(3) Lowered\n"
                             "(4) Owned\n"
                             ">> ").lower()
            if category in ("1", "veto"):
                alter_player("vetoedBy", match, rem=True)

            elif category in ("2", "favored"):
                alter_player("favoredBy", match, rem=True)

            elif category in ("3", "lowered"):
                alter_player("loweredBy", match, rem=True)

            elif category in ("4", "owned"):
                alter_player("ownedBy", match, rem=True)

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
                          "(10) Turn style\n"
                          ">> ").lower()

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
                shared = input("Can multiple people play with one copy of this game? ").lower()
                if shared in ("yes", "y"):
                    match["shared"] = True
                else:
                    match["shared"] = False

            elif field in ("5", "players"):
                play_count = re.split(r",\s*",
                                      input("How many players can play? Please split with a comma. ex. 2, 3, 4, 6 "))
                for i in play_count:
                    match["players"].append(int(i))
                if match["type"] in ("board", "card"):
                    match["copyPlayers"] = max(match["players"])

            elif field in ("6", "ideal"):
                ideal_count = re.split(r",\s*", input("What would be the perfect amount of players for this game? "
                                                      "ex. 2, 5, 6. Note that the game must allow"
                                                      " for that many players."))
                for i in ideal_count:
                    if i in match["players"]:
                        match["idealPlayers"].append(int(i))

            elif field in ("7", "copy"):
                if match["type"] in ("board", "card"):
                    match["copyPlayers"] = max(match["players"])
                    print("The game has been updated automatically.")
                else:
                    copy = input("What is the maximum number of people who can play with a single copy of this game? ")
                    match["copyPlayers"] = int(copy)

            elif field in ("8", "competition"):
                comp = input("Is this a co-op game, a pvp game, or both? ").lower()
                if comp in ("co-op", "pvp"):
                    match["compType"] = [comp]
                elif comp == "both":
                    match["compType"] = ["pvp", "co-op"]
                else:
                    print("I'm sorry, I didn't understand that.")

            elif field in ("9", "length"):
                match["length"] = [input("Is this game short, mid, long, day, or arb? ").lower()]

            elif field in ("10", "turn"):
                turns = input("Do you play this game in turns, or in real-time? ").lower()
                if turns == "turns":
                    match["turns"] = ["turnBased"]
                elif turns == "real-time":
                    match["turns"] = ["realTime"]
                else:
                    print("I'm sorry, I didn't understand that.")

            else:
                print("I'm sorry, I didn't understand that.")

    else:
        print("I'm sorry, I couldn't find that game in our library.")


# Lists the games in the library by title
def list_games():
    for game in options:
        print(game["title"])


if __name__ == "__main__":
    repeat = True
    while repeat:
        mode = input("Welcome! How may I be of assistance today? (Select a number or the first word)\n"
                     "(1) Add a game\n"
                     "(2) Check the library for an existing game\n"
                     "(3) Edit a game's entry\n"
                     "(4) List all games\n"
                     "(5) End program\n"
                     ">> ").lower()

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
