# import options
import json
import tkinter as tk
from tkinter import ttk
Currys = ["Dad", "Mom", "Jared", "Simon", "Kenan", "Micah"]
tabletop = [["board"], ["card"]]
game_styles = [
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


def activate_player_collection():
    player_count = int(spin_players.get())
    for i in range(10):
        if i + 1 > player_count:
            for widget in frm_player_selection.grid_slaves(row=i, column=0):
                widget.grid_remove()
            for widget in frm_player_selection.grid_slaves(row=i, column=1):
                widget.grid_remove()

    for i in range(player_count):
        if frm_player_selection.grid_slaves(row=i, column=1):
            continue
        else:
            lbl_player_name = tk.Label(master=frm_player_selection, text=f"Player {i + 1}:")
            ent_player_name = tk.Entry(master=frm_player_selection, width=30)
            lbl_player_name.grid(row=i, column=0, sticky="e")
            ent_player_name.grid(row=i, column=1)


def add_to_list():
    #TODO: Use lambda to pass an argument into this.
    style_list = []
    selected = list_style_select.curselection()
    for i in selected:
        style_list.append(game_styles[i])
    style_list_var = tk.StringVar(value=style_list)
    list_collected_styles["listvariable"] = style_list_var


def check_results():
    players = []
    for field in frm_player_selection.grid_slaves(column=1):
        players.append(field.get())
    game_type = combo_game_type.get()
    competition_type = combo_competition_type.get()


window = tk.Tk()
window.title("Game Chooser")

frm_selection = tk.Frame(master=window)
frm_selection.rowconfigure([i for i in range(13)], minsize=25)
frm_selection.columnconfigure([0, 1], minsize=60)
frm_selection.grid()

frm_player_selection = tk.Frame(master=frm_selection, borderwidth=1, relief=tk.SUNKEN)
frm_player_selection.columnconfigure(0, minsize=60)
frm_player_selection.grid(row=0, column=1, rowspan=9, sticky="nsew", padx=5)

frm_results_display = tk.Frame(master=window)

lbl_players = tk.Label(master=frm_selection, text="Players:")
lbl_players.grid(row=0, column=0, sticky="w")

spin_players = ttk.Spinbox(frm_selection, from_=2.0, to=10.0, command=activate_player_collection)
spin_players.state(["readonly"])
spin_players.set(2)
activate_player_collection()
spin_players.grid(row=1, column=0)

lbl_game_type = tk.Label(master=frm_selection, text="Game type:")
lbl_game_type.grid(row=3, column=0, sticky="w")

combo_game_type = ttk.Combobox(frm_selection)
combo_game_type["values"] = ("Any type", "Tabletop game", "Video game", "Board game", "Card game")
combo_game_type.state(["readonly"])
combo_game_type.set("Any type")
combo_game_type.grid(row=4, column=0)

lbl_competition_type = tk.Label(master=frm_selection, text="Competition type:")
lbl_competition_type.grid(row=5, column=0, sticky="w")

combo_competition_type = ttk.Combobox(frm_selection)
combo_competition_type["values"] = ("Any competition", "Co-op", "PvP")
combo_competition_type.state(["readonly"])
combo_competition_type.set("Any competition")
combo_competition_type.grid(row=6, column=0)

lbl_style_select = tk.Label(master=frm_selection, text="Game styles:")
lbl_style_select.grid(row=8, column=0, sticky="w")

game_styles_var = tk.StringVar(value=game_styles)
list_style_select = tk.Listbox(master=frm_selection, listvariable=game_styles_var, selectmode="extended")
list_style_select.grid(row=9, column=0, sticky="ns")

lbl_style_veto = tk.Label(master=frm_selection, text="Game styles:")
lbl_style_veto.grid(row=10, column=0, sticky="w")

list_collected_styles = tk.Listbox(master=frm_selection, selectmode="extended")
list_collected_styles.grid(row=9, column=1, sticky="nse")

list_style_veto = tk.Listbox(master=frm_selection, listvariable=game_styles_var, selectmode="extended")
list_style_veto.grid(row=11, column=0, sticky="ns")

btn_collect = tk.Button(master=frm_selection, text="Collect", command=add_to_list)
btn_collect.grid()
btn_calculate = tk.Button(master=frm_selection, text="Calculate", command=check_results)
btn_calculate.grid(row=13, column=1, sticky="e", padx=5, pady=3)


window.mainloop()


# If the game has x feature, keep the game
def keep_feature(game_list, spec, dict_key, inclusion=True):
    sorting_list = []
    for game in game_list:
        if spec in game[dict_key]:
            sorting_list.append(game)
    return sorting_list


# Keeps or excludes a game if it has any feature x
def check_set(game_list, spec, dict_key, inclusion=True):
    sorting_list = []
    if inclusion:
        for game in game_list:
            if not set(game[dict_key]).isdisjoint(set(spec)):
                sorting_list.append(game)
    else:
        for game in game_list:
            if set(game[dict_key]).isdisjoint(set(spec)):
                sorting_list.append(game)
    return sorting_list


def print_formatted_list(element_list):
    for num, element in enumerate(element_list, start=1):
        if num != len(element_list):
            print(element + ", ", end="")
        else:
            print(element, end="")
        if num % 4 == 0:
            print()


if __name__ == "__main__":
    # Collects the number of players. Anything above 10 is rare and unlikely, so using 10 as your option should be fine.
    keep_looping = True
    while keep_looping:
        player_count = input("Welcome! How many people will be playing today? ")
        try:
            player_count = int(player_count)
            if player_count in range(2, 11):
                keep_looping = False
            else:
                raise ValueError
        except ValueError:
            print("I'm sorry, I didn't understand that. Please input an integer between 2 and 10.")

    # These get updated/reset after each calculation
    results_list = options.copy()

    results_list = keep_feature(results_list, player_count, "players").copy()

    player_names = []

    # Collects the names of the players
    for player in range(player_count):
        player_names.append(input(f"What is the name of player {player + 1}? ").title())

    calculation_list = []

    # If nobody in the current group owns the game, or if somebody in the group has vetoed the game, this rules it out.
    results_list = check_set(results_list, player_names, "ownedBy").copy()
    results_list = check_set(results_list, player_names, "vetoedBy", inclusion=False).copy()

    # If the game requires multiple copies and not everybody has a copy, this rules it out.
    for game in results_list:
        if game["shared"] is True or set(player_names) <= set(game["ownedBy"]):
            calculation_list.append(game)

    results_list = calculation_list.copy()
    calculation_list = []

    # This doesn't calculate perfectly (ex. board games) but should do what we need for our purposes.
    for game in results_list:
        game_owners = 0
        for player in player_names:
            if player in game["ownedBy"]:
                game_owners += 1
        if game_owners * game["copyPlayers"] >= len(player_names):
            calculation_list.append(game)

    results_list = calculation_list.copy()
    calculation_list = []

    ruled_out = len(options) - len(results_list)

    print(f"\nGreat! We've ruled out {ruled_out} {'game' if ruled_out == 1 else 'games'} "
          f"that would be impossible for your group to play.")

    # Filters by what type of game you want
    keep_looping = True
    while keep_looping:
        game_type = input("Let's narrow it down further. "
                          "Which type of game are you looking for. Video, tabletop, or either? ").lower()
        if game_type == "video":
            results_list = keep_feature(results_list, game_type, "type").copy()
            keep_looping = False

        elif game_type == "tabletop":
            for game in results_list:
                if game["type"] in tabletop:
                    calculation_list.append(game)
            results_list = calculation_list.copy()
            calculation_list = []
            keep_looping = False

        elif game_type == "either":
            keep_looping = False

        else:
            print("I'm sorry, I didn't understand that.")

    # Filters game by what style you want
    keep_looping = True
    while keep_looping:
        game_type = input("Do you want a co-op game, a PvP game, or either? ").lower()
        if game_type in ("co-op", "pvp"):
            results_list = keep_feature(results_list, game_type, "compType").copy()
            keep_looping = False

        elif game_type == "either":
            keep_looping = False

        else:
            print("I'm sorry, I didn't understand that.")

    chosen_styles = []

    # Filters by how the game "feels"
    keep_looping = True
    while keep_looping:
        game_type = input("If you like a specific \"feel\" of game, input it now. "
                          "For a list, type list. When you're done, type done. ").lower()
        if game_type in game_styles:
            chosen_styles.append(game_type)

        elif game_type == "list":
            print_formatted_list(game_styles)
            print()

        elif game_type == "done":
            if not chosen_styles:
                chosen_styles = game_styles.copy()
            keep_looping = False

        else:
            print("I'm sorry, I didn't understand that.")

    results_list = check_set(results_list, chosen_styles, "feel").copy()

    excluded_styles = []

    keep_looping = True
    while keep_looping:
        game_type = input("If you would like to exclude a specific game feeling, please input it now. "
                          "For a list, type list. When you're done, type done. ").lower()
        if game_type in game_styles:
            excluded_styles.append(game_type)

        elif game_type == "list":
            print_formatted_list(game_styles)
            print()

        elif game_type == "done":
            keep_looping = False

        else:
            print("I'm sorry, I didn't understand that.")

    results_list = check_set(results_list, excluded_styles, "feel", inclusion=False).copy()
    calculation_list = keep_feature(results_list, player_count, "idealPlayers").copy()
    non_ideal_games = len(results_list) - len(calculation_list)

    # Some games can be played with x players, but weren't designed that way. This optionally rules those out.
    print(f"\nYou currently have {len(results_list)} {'option' if len(results_list) == 1 else 'options'} for your game.")
    if non_ideal_games > 0:
        if input(f"Of these, {non_ideal_games} {'is' if non_ideal_games == 1 else 'are'} not ideal "
                 f"for your number of players. Would you like to rule those games out? ").lower() in ("yes", "y"):
            results_list = calculation_list.copy()
    else:
        print("You have the perfect number of players for any of these games, so we're done calculating! "
              "Here's your list now.")

    # Assigns points to games based on how many factors they fit
    for game in results_list:
        points = 0
        for player in player_names:
            if player in game["favoredBy"]:
                points += 1
            if player in game["loweredBy"]:
                points -= 1
        if chosen_styles != game_styles:
            for game_type in chosen_styles:
                if game_type in game["feel"]:
                    points += 1
        if player_count in game["idealPlayers"]:
            points += 1

        game["points"] = points

    # Gets the length of the longest game title in the list
    title_len = 0
    for game in results_list:
        if len(game["title"]) > title_len:
            title_len = len(game["title"])

    # Prints the list of games, sorted by points
    print("\n--Game Options--\n")
    for i in range(30, -1, -1):
        for game in results_list:
            if i == game["points"]:
                print(f"{game['title']:.<{title_len+10}}{str(game['points'])} {'point' if i == 1 else 'points'}")
