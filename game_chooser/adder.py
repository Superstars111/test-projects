import json
import re
import string
from choice import game_styles, print_formatted_list

with open("options.json", "r") as option_list:
    options = json.load(option_list)


# Adds or removes a player (or players) from a field- specifically, favoredBy, vetoedBy, loweredBy, and ownedBy
def alter_player(alt_type, target, rem=False):
    keep_looping = True
    while keep_looping:
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


def insert_alphabetically(new_game, game_list):
    title_idx = 0
    comp_idx = 0
    game_idx = 0
    title_checked = False
    is_inserted = False
    while not is_inserted:
        if not title_checked:
            if len(game_list[game_idx]["title"]) >= 4:
                if game_list[game_idx]["title"] == "The Game of LIFE":
                    comp_idx = comp_idx + 12
                elif game_list[game_idx]["title"][0:2] == "A ":
                    comp_idx = comp_idx + 2
                elif game_list[game_idx]["title"][0:4] == "The ":
                    comp_idx = comp_idx + 4

            if len(new_game["title"]) >= 4:
                if new_game["title"][0:4] == "The ":
                    title_idx = title_idx + 4
                elif new_game["title"][0:2] == "A ":
                    title_idx = title_idx + 2
            title_checked = True

        if new_game["title"][title_idx] in (string.punctuation, " "):
            title_idx += 1
            continue
        if game_list[game_idx]["title"][comp_idx] in (string.punctuation, " "):
            comp_idx += 1
            continue

        if game_idx == len(game_list):
            # If you reach the end of the list, put it there
            game_list[game_idx] = [new_game]
            is_inserted = True
        elif title_idx == len(new_game["title"]):
            # If you've found a title that encompasses this one, put this title right before that one
            game_list[game_idx:game_idx] = [new_game]
            is_inserted = True
        elif comp_idx >= len(game_list[game_idx]["title"]):
            game_list[game_idx+1:game_idx+1] = [new_game]
            is_inserted = True
        elif new_game["title"][title_idx].lower() > game_list[game_idx]["title"][comp_idx].lower():
            # If you're still ahead of your alphabetic position, check the next game
            game_idx += 1
            title_idx = 0
            comp_idx = 0
            title_checked = False
        elif new_game["title"][title_idx].lower() == game_list[game_idx]["title"][comp_idx].lower():
            title_idx += 1
            comp_idx += 1
        elif new_game["title"][title_idx].lower() < game_list[game_idx]["title"][comp_idx].lower():
            game_list[game_idx:game_idx] = [new_game]
            is_inserted = True


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

        is_duplicate = False
        game["title"] = input("What is this game's title? Please be exact. ")  # Title collection
        for existing_game in options:
            if existing_game["title"] == game["title"]:
                is_duplicate = True
        if is_duplicate:
            print("That game already exists in the library!")
            break

        print("Is there anyone who will refuse to play this game?")  # Veto collection
        alter_player("vetoedBy", game)

        print("Does anyone especially like this game?")  # Favored collection
        alter_player("favoredBy", game)

        print("Does anyone lean against this game?")  # Lowered collection
        alter_player("loweredBy", game)

        keep_looping = True  # Type collection
        while keep_looping:
            game_type = input("Is this a video game, a board game, or a card game? ").lower()
            if game_type in ("video", "board", "card"):
                game["type"] = [game_type]
                keep_looping = False
            else:
                print("I'm sorry, I didn't understand that. Please type video, board, or card.")

        keep_looping = True  # Feel collection
        while keep_looping:
            style = input("What is the \"feel\" of this game? "
                          "For a list, type list. When you're done, type done. ").lower()
            if style in game_styles:
                game["feel"].append(style)

            elif style == "list":
                print_formatted_list(game_styles)
                print()

            elif style == "done":
                if not game["feel"]:
                    print("Please choose at least one feel for each game.")
                else:
                    keep_looping = False

            else:
                print("I'm sorry, I didn't understand that.")

        # Player count collection
        keep_looping = True
        while keep_looping:
            player_count = re.split(r",\s*", input("How many players can play? Please split with a comma. ex. 2, 3, 4, 6"
                                                 "\n>> "))
            try:
                game["players"] = [int(i) for i in player_count]
                keep_looping = False
            except ValueError:
                print("Please only use integers. If there are multiple, separate them with a comma.")

        # Ideal number of players collection
        if len(game["players"]) > 1:
            ideal_player_count = re.split(r",\s*", input("What would be the perfect amount of players for this game? ex. 2, 5, 6"
                                                  "\n>> "))
            for i in ideal_player_count:
                if i in player_count:
                    game["idealPlayers"].append(int(i))
        else:
            game["idealPlayers"] = game["players"]

        # Shared collection
        if game["type"] == ["video"]:
            sharable = input("Can multiple people play with just one copy of this game? Yes or no. ").lower()
            if sharable in ("yes", "y"):
                game["shared"] = True
        else:
            game["shared"] = True

        # Maximum players per copy collection
        if game["shared"]:
            if game["type"] in (["board"], ["card"]) or len(game["players"]) == 1:
                game["copyPlayers"] = max(game["players"])

            else:
                game["copyPlayers"] = int(input("What is the maximum number of people who can play with one copy of this game? "))

        else:
            game["copyPlayers"] = 1

        keep_looping = True  # Competition collection
        while keep_looping:
            competition_type = input("Is this game pvp, co-op, or both? ").lower()
            if competition_type in ("pvp", "co-op"):
                game["compType"] = [competition_type]
                keep_looping = False
            elif competition_type == "both":
                game["compType"] = ["pvp", "co-op"]
                keep_looping = False
            else:
                print("I'm sorry, I didn't understand that. Please input pvp, co-op, or both.")

        print("Who owns this game? If this is a Curry family game, you can type family.")  # Owner collection
        alter_player("ownedBy", game)

        keep_looping = True  # Turn style collection
        while keep_looping:
            turns = input("Is this game turn-based, or real-time? ").lower()
            if turns == "turn-based":
                game["turns"] = ["turnBased"]
                keep_looping = False
            elif turns == "real-time":
                game["turns"] = ["realTime"]
                keep_looping = False
            else:
                print("I'm sorry, I didn't understand that.")

        insert_alphabetically(game, options)
        print()


# Checks the status of a game already in the library
def check_game(title, print_results=True):
    match = None
    for game in options:
        if title == game["title"].lower():
            match = game

    if match:
        print_game = input("I've found a game that has that title! Would you like to see it? ").lower()
        if print_game in ("yes", "y"):
            for field in match:
                print(f"{field}: {match[field] if match[field] else ''}")
            print()
        return True

    else:
        if print_results:
            print("I'm sorry, I couldn't find that game in our library.")
        return False


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
                if not check_game(new_title, print_results=False):
                    match["title"] = new_title

            elif field in ("2", "type"):
                new_type = input("What type of game is this? Video, board, or card? ").lower()
                if new_type in ("video", "board", "card"):
                    match["type"] = [new_type]
                else:
                    print("Please input a valid game type.")

            elif field in ("3", "feel"):
                adjustment_type = input("Do you need to add or remove a feel from this game? ").lower()
                if adjustment_type in ("add", "remove"):
                    feel = input(f"Which feeling do you need to {adjustment_type}? For a list, type list. ").lower()

                    if feel in game_styles:
                        if adjustment_type == "add":
                            if feel not in match["feel"]:
                                match["feel"].append(feel)
                            else:
                                print("This game already has that feeling assigned to it.")
                        else:
                            if feel not in match["feel"]:
                                print("This game doesn't have that feeling assigned to it.")
                            else:
                                match["feel"].remove(feel)

                    elif feel == "list":
                        print_formatted_list(game_styles)

                    else:
                        print("That is not in the list of approved feelings. Sorry. Please feel better.")

                else:
                    print("*Sigh...* What's so difficult about typing add or remove?")

            elif field in ("4", "shared"):
                if input("Can multiple people play with one copy of this game? ").lower() in ("yes", "y"):
                    match["shared"] = True
                else:
                    match["shared"] = False

            elif field in ("5", "players"):
                match["players"] = []
                play_count = re.split(r",\s*", input("How many players can play? Please split with a comma. ex. 2, 3, 4, 6 "))

                for i in play_count:
                    match["players"].append(int(i))

                if match["type"] in (["board"], ["card"]):
                    match["copyPlayers"] = max(match["players"])

            elif field in ("6", "ideal"):
                match["idealPlayers"] = []
                ideal_players = re.split(r",\s*", input("What would be the perfect amount of players for this game? "
                                                        "ex. 2, 5, 6. Note that the game must allow for that many players. "))
                for i in ideal_players:
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
                competition_type = input("Is this a co-op game, a pvp game, or both? ").lower()
                if competition_type in ("co-op", "pvp"):
                    match["compType"] = [competition_type]
                elif competition_type == "both":
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
            add_game(int(input("How many games would you like to add today? Please input an integer. ")))

        elif mode in ("2", "check"):
            check = input("Which game would you like to check? "
                          "Please make sure the title is exact, including punctuation. ").lower()
            check_game(check)

        elif mode in ("3", "edit"):
            alter = input("Which game would you like to edit? "
                          "Please make sure the title is exact, including punctuation. ").lower()
            edit_game(alter)

        elif mode in ("4", "list"):
            list_games()

        elif mode in ("5", "end"):
            repeat = False
            break

        else:
            print("I'm sorry, I didn't understand that.")
            continue

        if input("Will that be all today? ").lower() in ("yes", "y"):
            repeat = False


with open("options.json", "w") as file:
    json.dump(options, file, indent=4)
