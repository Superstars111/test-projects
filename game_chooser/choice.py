import options

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

results = options.options.copy()
calc = []

for game in results:
    if play_count in game["players"]:
        calc.append(game)

results = calc.copy()
calc = []
players = []

for player in range(play_count):
    players.append(input(f"What is the name of player {player + 1}? ").title())

for game in results:
    if set(game["vetoedBy"]).isdisjoint(set(players)) and not set(game["ownedBy"]).isdisjoint(set(players)):
        calc.append(game)

results = calc.copy()
calc = []

for game in results:
    if game["shared"] is True or (game["shared"] is False and set(players) <= set(game["ownedBy"])):
        calc.append(game)

results = calc.copy()
calc = []
ruled = len(options.options) - len(results)

print(f"\nGreat! We've ruled out {ruled} games that would be impossible for your group to play.")

retry = True
while retry:
    style = input("Let's narrow it down further. "
                  "Which type of game are you looking for. Video, tabletop, or either? ").lower()
    if style == "video":
        for game in results:
            if game["type"] == "video":
                calc.append(game)
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
retry = True
while retry:
    style = input("Do you want a co-op game, a PvP game, or either? ").lower()
    if style == "co-op":
        for game in results:
            if game["compType"] == ("co-op" or "modes"):
                calc.append(game)
        retry = False

    elif style == "pvp":
        for game in results:
            if game["compType"] == ("pvp" or "modes"):
                calc.append(game)
        retry = False

    elif style == "either":
        calc = results.copy()
        retry = False

    else:
        print("I'm sorry, I didn't understand that.")

results = calc.copy()
calc = []

print(f"You currently have {len(results)} options for your game.")
limiter = input("Should we rule out games where you don't have the perfect number of players? ").lower()
if limiter in ("yes", "y"):
    for game in results:
        if play_count in game["idealPlayers"]:
            calc.append(game)

results = calc.copy()
calc = []


print("\n--Game Options--\n")
for game in results:
    print(game["title"])
