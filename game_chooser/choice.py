import options


def sort(game_list, spec, dict_key, inclusion=True):
    for game in game_list:
        if spec in game[dict_key]:
            calc.append(game)


def set_sort(game_list, spec, dict_key, inclusion=True):
    if inclusion:
        for game in game_list:
            if not set(game[dict_key]).isdisjoint(spec):
                calc.append(game)
    else:
        for game in game_list:
            if set(game[dict_key]).isdisjoint(spec):
                calc.append(game)


# Collects the number of players. Anything above 10 is rare and unlikely, so using 10 as your option should work fine.
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
results = options.options.copy()  # Used for filtering from and final results
calc = []  # Used for filtering into and updating results

# Limits possible games to only what can be played with the current number of players
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
ruled = len(options.options) - len(results)

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
            if game["type"] in options.tabletop:
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

retry = True
while retry:
    style = input("If you like a specific \"feel\" of game, input it now. "
                  "For a list, type list. When you're done, type done. ").lower()
    if style in options.feelings:
        feel.append(style)
    elif style == "list":
        for feeling in options.feelings:
            print(feeling)

    elif style == "done":
        if not feel:
            feel = options.feelings.copy()
        retry = False
    else:
        print("I'm sorry, I didn't understand that.")

set_sort(results, feel, "feel")

results = calc.copy()
calc = []
feel = []

retry = True
while retry:
    style = input("If you would like to exclude a specific game feeling, please input it now. "
                  "For a list, type list. When you're done, type done. ").lower()
    if style in options.feelings:
        feel.append(style)
    elif style == "list":
        for feeling in options.feelings:
            print(feeling)
    elif style == "done":
        retry = False
    else:
        print("I'm sorry, I didn't understand that.")

set_sort(results, feel, "feel", inclusion=False)

results = calc.copy()
calc = []
feel = []

# Some games can be played with x players, but weren't designed that way. This optionally rules those out.
print(f"\nYou currently have {len(results)} {'option' if len(results) == 1 else 'options'} for your game.")
limiter = input("Should we rule out games where you don't have the perfect number of players? ").lower()
if limiter in ("yes", "y"):
    for game in results:
        if play_count in game["idealPlayers"]:
            calc.append(game)
else:
    calc = results.copy()

results = calc.copy()
calc = []


print("\n--Game Options--\n")
for game in results:
    print(game["title"])
