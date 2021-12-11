import json
import tkinter as tk
import tkinter.font as fnt
from tkinter import ttk
import urllib.request
from PIL import Image, ImageTk
import io
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas

with open("anime_data.json", "r") as anime_data:
    library = json.load(anime_data)
options = []
option_titles = []
library_titles = []
cover_image = []
mild_warnings = ("Afterlife", "Ahegao", "Angels", "Assassins", "Bisexual", "Body Horror", "Body Swapping", "Cosmic Horror", "Crossdressing", "Death Game", "DILF", "Drugs", "Ero Guru", "Feet", "Female Harem", "Flat Chest", "Gambling", "Gangs", "Gender Bending", "Ghost", "Gods", "Large Breasts", "Male Harem", "Masochism", "MILF", "Oiran", "Prostitution", "Reincarnation", "Slavery", "Succubus", "Suicide", "Sweat", "Teens' Love", "Tentacles", "Terrorism", "Torture", "Virginity", "Yandere", "Youkai")
extreme_warnings = ("Anal Sex", "Ashikoki", "Boobjob", "Boy's Love", "Cannibalism", "Cunnilingus", "Defloration", "Exhibitionism", "Facial", "Fellatio", "Femdom", "Flash", "Futanari", "Gore", "Group Sex", "Handjob", "Incest", "Inseki", "Irrumatio", "Lactation", "LGBTQ+ Themes", "Masturmation", "Nakadashi", "Netorare", "Netorase", "Netori", "Nudity", "Public Sex", "Rape", "Rimjob", "Scat", "Scissoring", "Sex Toys", "Sumata", "Threesome", "Transgenger", "Vore", "Voyeur", "Yaoi", "Yuri")
content_warnings = [0, 0, 0]

for show in library:
    library_titles.append(show["englishTitle"])


def add_options():
    library_var = tk.StringVar(value=library_titles)
    options_var = tk.StringVar(value=option_titles)

    dlg_selection = tk.Toplevel(window)
    dlg_selection.title("Option Selector")
    dlg_selection.attributes("-topmost")
    dlg_selection.transient(window)
    dlg_selection.grab_set()
    btn_confirm = tk.Button(dlg_selection, text="Confirm choices", command=lambda: dismiss_window(dlg_selection))
    lbox_library = tk.Listbox(dlg_selection, listvariable=library_var)
    lbox_selected = tk.Listbox(dlg_selection, listvariable=options_var)
    btn_add_option = tk.Button(dlg_selection, text="Add", command=lambda: add_to_list(lbox_library, lbox_selected))
    lbox_library.bind("<Double-1>", lambda x: add_to_list(lbox_library, lbox_selected))
    btn_remove_option = tk.Button(dlg_selection, text="Remove", command=lambda: remove_from_list(options, lbox_selected))
    lbox_selected.bind("<Double-1>", lambda x: remove_from_list(options, lbox_selected))

    lbox_library.grid(row=1, column=0, rowspan=4)
    lbox_selected.grid(row=1, column=2, rowspan=4)
    btn_add_option.grid(row=2, column=1)
    btn_remove_option.grid(row=3, column=1)
    btn_confirm.grid(row=5, column=1)
    dlg_selection.wait_window()


def convert_image(url):
    raw_url = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    raw_image = urllib.request.urlopen(raw_url).read()
    image_data = Image.open(io.BytesIO(raw_image))
    image = ImageTk.PhotoImage(image_data)
    if image not in cover_image:
        cover_image.append(image)

    return image


def plot_graph(show):
    frm_ratings.grid_slaves(row=1, column=0)[0].grid_remove()
    scores = [show["jaredScore"], show["simonScore"], show["kenanScore"]]
    ratings = [score_list[0] for score_list in scores]
    pacing_scores = []
    drama_scores = []
    for idx, score in enumerate(ratings):
        if score > 0:
            pacing_scores.append(scores[idx][1])
            drama_scores.append(scores[idx][2])

    graph_location = {
        "pacing": pacing_scores,
        "comedy": drama_scores
    }
    data_sorting = pandas.DataFrame(graph_location, columns=["pacing", "comedy"])
    # graph.axhline(0, color="black")
    # graph.axvline(0, color="black")
    graph_frame = plt.Figure(figsize=(5, 4), dpi=100)
    graph = graph_frame.add_subplot(111)
    graph.grid()
    graph.scatter([50, -50], [50, -50], s=[0, 0])
    scatter_chart = FigureCanvasTkAgg(graph_frame, frm_ratings)
    scatter_chart.get_tk_widget().grid(row=1, column=0, columnspan=4)
    graph.set_ylabel("< Drama \u2022 Comedy >")
    graph.set_xlabel("< Slow Pacing \u2022 Fast Pacing >")
    graph.scatter(data_sorting["pacing"], data_sorting["comedy"], color="g")
    # graph.set_title("Pacing vs. Comedy and Drama")


def add_to_list(lbox_out, lbox_in):
    selected = lbox_out.curselection()[0]

    if library_titles[selected] not in option_titles:
        options.append(library[selected])
        option_titles.append(library_titles[selected])

    options_var = tk.StringVar(value=option_titles)
    lbox_in["listvariable"] = options_var


def remove_from_list(options_list, lbox):

    options_list.pop(lbox.curselection()[0])
    option_titles.pop(lbox.curselection()[0])

    options_list_var = tk.StringVar(value=option_titles)
    lbox["listvariable"] = options_list_var


def dismiss_window(popup):
    popup.grab_release()
    popup.destroy()
    options_var = tk.StringVar(value=option_titles)
    lbox_options["listvariable"] = options_var


def toggle_spoilers():
    if spoiler_state.get() == 1:
        lbl_spoiler_tags.grid(row=5, column=0)
        cbox_spoiler_tags["text"] = f"\u25BC Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"
    else:
        lbl_spoiler_tags.grid_remove()
        cbox_spoiler_tags["text"] = f"\u25B6 Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"


def sort_tags(show):
    normal_tags = []
    spoiler_tags = []
    for tag in show["tags"]:
        if tag["isMediaSpoiler"]:
            spoiler_tags.append(f"{tag['name']} ({tag['rank']}%)")
            if tag["name"] in extreme_warnings:
                content_warnings[2] += 1
            elif tag['name'] in mild_warnings:
                content_warnings[1] += 1
            else:
                content_warnings[0] += 1
        else:
            normal_tags.append(f"{tag['name']} ({tag['rank']}%)")

    return normal_tags, spoiler_tags


def update_page_display(null):
    show = options[lbox_options.curselection()[0]]
    seenby = 0
    content_warnings[0] = 0
    content_warnings[1] = 0
    content_warnings[2] = 0
    for rating in (show["jaredScore"][0], show["simonScore"][0], show["kenanScore"][0]):
        if rating > 0:
            seenby += 1
    avg_house_score = (show["jaredScore"][0] + show["simonScore"][0] + show["kenanScore"][0]) // seenby
    if show["score"] >= 85:
        lbl_public_star.config(fg="purple")
    elif show["score"] >= 70:
        lbl_public_star.config(fg="blue")
    elif show["score"] >= 55:
        lbl_public_star.config(fg="orange")
    elif show["score"] >= 1:
        lbl_public_star.config(fg="red")
    else:
        lbl_public_star.config(fg="black")

    if avg_house_score >= 85:
        lbl_house_star.config(fg="purple")
    elif avg_house_score >= 70:
        lbl_house_star.config(fg="blue")
    elif avg_house_score >= 55:
        lbl_house_star.config(fg="orange")
    elif avg_house_score >= 1:
        lbl_house_star.config(fg="red")
    else:
        lbl_house_star.config(fg="black")

    lbl_title["text"] = f"{show['romajiTitle']} \u2022 {show['englishTitle']} \u2022 {show['nativeTitle']}"
    lbl_avg_rating["text"] = f"Public score: {show['score']}/100"
    lbl_house_rating["text"] = f"House score: {avg_house_score}/100"
    plot_graph(show)
    lbl_cover_image["image"] = convert_image(show["coverMed"])
    lbl_episodes["text"] = f"Total episodes: {show['episodes']}"
    lbl_seasons["text"] = f"Seasons: {show['seasons']}"
    lbl_movies["text"] = f"Movies: {show['movies']}"
    if show["unairedSeasons"] == 0:
        lbl_unaired_seasons["text"] = ""
    else:
        lbl_unaired_seasons["text"] = f"Unfinished Seasons: {show['unairedSeasons']}"
    lbl_description["text"] = show['description']
    lbl_genres_list["text"] = f"{', '.join(show['genres'])}"
    normal_tags, spoiler_tags = sort_tags(show)
    lbl_tags_list["text"] = f"{', '.join(normal_tags)}"
    lbl_spoiler_tags["text"] = f"{', '.join(spoiler_tags)}"
    if spoiler_state.get() == 1:
        cbox_spoiler_tags["text"] = f"\u25BC Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"
    else:
        cbox_spoiler_tags["text"] = f"\u25B6 Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"


if __name__ == "__main__":
    window = tk.Tk()
    default_font = fnt.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window.title("Anime Data Displayinator 9001 (Beta)")
    frm_anime_display = tk.Frame(window)
    frm_ratings = tk.Frame(frm_anime_display)
    frm_series_info = tk.Frame(frm_anime_display)
    frm_tags = tk.Frame(frm_anime_display)
    lbl_title = tk.Label(frm_anime_display, text="Anime Data Program", font=("Arial", 20), wraplength=900)
    lbl_avg_rating = tk.Label(frm_ratings, text="Public score: 0/100")
    lbl_house_rating = tk.Label(frm_ratings, text="House score: 0/100")
    lbl_public_star = tk.Label(frm_ratings, text="\u2605")
    lbl_house_star = tk.Label(frm_ratings, text="\u2605")
    #cnvs_graph = tk.Canvas(frm_anime_display)
    lbl_cover_image = tk.Label(frm_series_info)
    lbl_episodes = tk.Label(frm_series_info, text="Episodes: 0")
    lbl_seasons = tk.Label(frm_series_info, text="Seasons: 0")
    lbl_unaired_seasons = tk.Label(frm_series_info, text="Unfinished Seasons: 0")
    lbl_movies = tk.Label(frm_series_info, text="Movies: 0")
    frm_description = tk.Frame(frm_anime_display, width=300, height=300, borderwidth=2, relief="solid")
    lbl_description = tk.Label(frm_description, text="", wraplength=440)
    lbl_genres = tk.Label(frm_tags, text="Genres:")
    lbl_genres_list = tk.Label(frm_tags, text="", wraplength=400)
    lbl_tags = tk.Label(frm_tags, text="Tags:")
    lbl_tags_list = tk.Label(frm_tags, text="", wraplength=400)
    spoiler_state = tk.IntVar()
    cbox_spoiler_tags = tk.Checkbutton(frm_tags, text="\u25B6 Spoiler Tags: (0, 0, 0)",
                                       command=toggle_spoilers, variable=spoiler_state)
    lbl_spoiler_tags = tk.Label(frm_tags, text="SPOILERS! Hide this before selecting a series.", wraplength=400)
    lbox_options = tk.Listbox(window, height=35)
    btn_options = tk.Button(window, text="Add Options", command=add_options)

    lbox_options.bind("<<ListboxSelect>>", update_page_display)

    lbl_title.grid(row=0, column=0, columnspan=2, pady=8)
    lbl_avg_rating.grid(row=0, column=0, sticky="e")
    lbl_public_star.grid(row=0, column=1, sticky="w")
    lbl_house_rating.grid(row=0, column=2, sticky="e")
    lbl_house_star.grid(row=0, column=3, sticky="w")
    #cnvs_graph.grid(row=2, column=0, rowspan=6, columnspan=2)

    graph_frame = plt.Figure(figsize=(5, 4), dpi=100)
    graph = graph_frame.add_subplot(111)
    graph.grid()
    graph.scatter([50, -50], [50, -50], s=[0, 0])
    scatter_chart = FigureCanvasTkAgg(graph_frame, frm_ratings)
    scatter_chart.get_tk_widget().grid(row=1, column=0, columnspan=4)
    graph.set_ylabel("< Drama \u2022 Comedy >")
    graph.set_xlabel("< Slow Pacing \u2022 Fast Pacing >")

    lbl_cover_image.grid(row=0, column=0, rowspan=4, sticky="w", padx=15)
    lbl_episodes.grid(row=0, column=1)
    lbl_seasons.grid(row=1, column=1)
    lbl_movies.grid(row=2, column=1)
    lbl_unaired_seasons.grid(row=3, column=1)
    lbl_description.grid(sticky="new")
    frm_description.columnconfigure(0, minsize=450)
    frm_description.rowconfigure(0, minsize=330)
    frm_ratings.grid(row=1, column=0, padx=10)
    frm_series_info.grid(row=1, column=1)
    frm_tags.grid(row=2, column=0)
    frm_description.grid(row=2, column=1)
    lbl_genres.grid(row=0, column=0)
    lbl_genres_list.grid(row=1, column=0)
    lbl_tags.grid(row=2, column=0)
    lbl_tags_list.grid(row=3, column=0)
    cbox_spoiler_tags.grid(row=4, column=0)

    frm_tags.rowconfigure(5, minsize=30)
    frm_anime_display.rowconfigure(0, minsize=90)
    frm_anime_display.grid()
    lbox_options.grid(row=0, column=1, sticky="s")
    btn_options.grid(row=1, column=1, pady=7)

    window.mainloop()
