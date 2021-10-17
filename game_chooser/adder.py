import json

with open("options.json", "r") as options:
    options = [json.load(options)]

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

add_num = int(input("Welcome! How many games will you be adding to the library today? "))

for i in range(add_num):
    game = {
        "title": "",
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
        game["vetoedBy"].append(player)

    cont = True  # Favored collection
    while cont:
        player = input("Does anyone especially like this game? Put their name here. "
                       "When you're done, type done. ").title()
        if player == "Done":
            cont = False
        game["favoredBy"].append(player)

    cont = True  # Lowered collection
    while cont:
        player = input("Does anyone lean against this game? Put their name here. "
                       "When you're done, type done. ").title()
        if player == "Done":
            cont = False
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

    shared = input("Can multiple people play with just one copy of this game? Yes or no. ").lower()  # Shared collection
    if shared in ("yes", "y"):
        game["shared"] = True

    cont = True
    while cont:
        cont = False
    # How many players can play this game? I need each individual combination...

    # Ideal players should be easier, since that's just a range, yes?
    # And maybe I could use a for loop on the previous answer...

    if game["shared"]:  # Max copy players collection
        if game["type"] in ("board", "card"):
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

with open("options.json", "w") as file:
    json.dump(options, file, indent=4)
