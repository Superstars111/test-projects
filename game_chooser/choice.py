#import options
import json
Currys = ["Dad", "Mom", "Jared", "Simon", "Kenan", "Micah"]
tabletop = [["board"], ["card"]]
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

with open("options.json", "r") as option_list:
    options = json.load(option_list)


# If the game has x feature, keep the game
def sort(game_list, spec, dict_key, inclusion=True):
    for game in game_list:
        if spec in game[dict_key]:
            calc.append(game)


# Keeps or excludes a game if it has any feature x
def set_sort(game_list, spec, dict_key, inclusion=True):
    if inclusion:
        for game in game_list:
            if not set(game[dict_key]).isdisjoint(spec):
                calc.append(game)
    else:
        for game in game_list:
            if set(game[dict_key]).isdisjoint(spec):
                calc.append(game)


if __name__ == "__main__":
    # Collects the number of players. Anything above 10 is rare and unlikely, so using 10 as your option should be fine.
    retry = True
    while retry:
        play_count = input("Welcome! How many people will be playing today? ")
        try:
            play_count = int(play_count)
            if play_count in range(2, 11):
                retry = False
            else:
                raise ValueError
        except ValueError:
            print("I'm sorry, I didn't understand that. Please input an integer between 2 and 10.")

    # These get updated/reset after each calculation
    results = options.copy()  # Used for filtering from and final results
    calc = []  # Used for filtering into and updating results

    sort(results, play_count, "players")

    results = calc.copy()
    calc = []
    players = []

    # Collects the names of the players
    for player in range(play_count):
        players.append(input(f"What is the name of player {player + 1}? ").title())

    # If nobody in the current group owns the game, or if somebody in the group has vetoed the game, this rules it out.
    for game in results:
        if set(game["vetoedBy"]).isdisjoint(set(players)) and not set(game["ownedBy"]).isdisjoint(set(players)):
            calc.append(game)

    results = calc.copy()
    calc = []

    # If the game requires multiple copies and not everybody has a copy, this rules it out.
    for game in results:
        if game["shared"] is True or set(players) <= set(game["ownedBy"]):
            calc.append(game)

    results = calc.copy()
    calc = []
    owners = 0

    # This doesn't calculate perfectly (ex. board games) but should do what we need for our purposes.
    for game in results:
        for player in players:
            if player in game["ownedBy"]:
                owners += 1
        if owners * game["copyPlayers"] >= len(players):
            calc.append(game)
        owners = 0

    results = calc.copy()
    calc = []

    ruled = len(options) - len(results)

    print(f"\nGreat! We've ruled out {ruled} {'game' if ruled == 1 else 'games'} "
          f"that would be impossible for your group to play.")

    # Filters by what type of game you want
    retry = True
    while retry:
        style = input("Let's narrow it down further. "
                      "Which type of game are you looking for. Video, tabletop, or either? ").lower()
        if style == "video":
            sort(results, style, "type")
            retry = False

        elif style == "tabletop":
            for game in results:
                if game["type"] in tabletop:
                    calc.append(game)
            retry = False

        elif style == "either":
            calc = results.copy()
            retry = False

        else:
            print("I'm sorry, I didn't understand that.")

    results = calc.copy()
    calc = []

    # Filters game by what style you want
    retry = True
    while retry:
        style = input("Do you want a co-op game, a PvP game, or either? ").lower()
        if style in ("co-op", "pvp"):
            sort(results, style, "compType")
            retry = False

        elif style == "either":
            calc = results.copy()
            retry = False

        else:
            print("I'm sorry, I didn't understand that.")

    results = calc.copy()
    calc = []
    feel = []

    # Filters by how the game "feels"
    retry = True
    while retry:
        style = input("If you like a specific \"feel\" of game, input it now. "
                      "For a list, type list. When you're done, type done. ").lower()
        if style in feelings:
            feel.append(style)

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
            if not feel:
                feel = feelings.copy()
            retry = False

        else:
            print("I'm sorry, I didn't understand that.")

    set_sort(results, feel, "feel")

    results = calc.copy()
    calc = []
    exclude = []

    retry = True
    while retry:
        style = input("If you would like to exclude a specific game feeling, please input it now. "
                      "For a list, type list. When you're done, type done. ").lower()
        if style in feelings:
            exclude.append(style)

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
            retry = False

        else:
            print("I'm sorry, I didn't understand that.")

    set_sort(results, exclude, "feel", inclusion=False)

    results = calc.copy()
    calc = []

    # Some games can be played with x players, but weren't designed that way. This optionally rules those out.
    print(f"\nYou currently have {len(results)} {'option' if len(results) == 1 else 'options'} for your game.")
    limiter = input("Should we rule out games where you don't have the perfect number of players? ").lower()

    if limiter in ("yes", "y"):
        sort(results, play_count, "idealPlayers")
    else:
        calc = results.copy()

    results = calc.copy()
    calc = []
    points = 0

    # Assigns points to games based on how many factors they fit
    for game in results:
        for player in players:
            if player in game["favoredBy"]:
                points += 1
            if player in game["loweredBy"]:
                points -= 1
        if feel != feelings:
            for style in feel:
                if style in game["feel"]:
                    points += 1
        if play_count in game["idealPlayers"]:
            points += 1

        game["points"] = points
        points = 0

    # Gets the length of the longest game title in the list
    title_len = 0
    for game in results:
        if len(game["title"]) > title_len:
            title_len = len(game["title"])

    # Prints the list of games, sorted by points
    print("\n--Game Options--\n")
    for i in range(30, -1, -1):
        for game in results:
            if i == game["points"]:
                print(f"{game['title']:.<{title_len+10}}{str(game['points'])} {'point' if i == 1 else 'points'}")
