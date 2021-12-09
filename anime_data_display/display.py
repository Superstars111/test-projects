import json
import tkinter as tk
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

for show in library:
    library_titles.append(show["englishTitle"])


def add_options():
    library_var = tk.StringVar(value=library_titles)
    options_var = tk.StringVar(value=option_titles)

    dlg_selection = tk.Toplevel(window)
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
    scatter_chart = FigureCanvasTkAgg(graph_frame, frm_anime_display)
    scatter_chart.get_tk_widget().grid(row=2, column=0, rowspan=4, columnspan=2)
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
        lbl_spoiler_tags.grid(row=11, column=0)
        cbox_spoiler_tags["text"] = "\u25BC Spoiler Tags: (0, 0, 0)"
    else:
        lbl_spoiler_tags.grid_remove()
        cbox_spoiler_tags["text"] = "\u25B6 Spoiler Tags: (0, 0, 0)"


def update_page_display(test):
    show = options[lbox_options.curselection()[0]]
    seenby = 0
    for rating in (show["jaredScore"][0], show["simonScore"][0], show["kenanScore"][0]):
        if rating > 0:
            seenby += 1

    lbl_title["text"] = f"{show['romajiTitle']} \u2022 {show['englishTitle']} \u2022 {show['nativeTitle']}"
    lbl_avg_rating["text"] = f"Public rating: {show['score']}/100 \u2605"
    lbl_house_rating["text"] = f"House rating: {(show['jaredScore'][0] + show['simonScore'][0] + show['kenanScore'][0])//seenby}/100 \u2605"
    plot_graph(show)
    lbl_cover_image["image"] = convert_image(show["coverSmall"])
    lbl_episodes["text"] = f"Total episodes: {show['episodes']}"
    lbl_seasons["text"] = f"Seasons: {show['seasons']}"
    lbl_movies["text"] = f"Movies: {show['movies']}"
    if show["unairedSeasons"] == 0:
        lbl_unaired_seasons["text"] = ""
    else:
        lbl_unaired_seasons["text"] = f"Unfinished Seasons: {show['unairedSeasons']}"
    lbl_description["text"] = show['description']
    lbl_genres_list["text"] = f"{', '.join(show['genres'])}"


if __name__ == "__main__":
    window = tk.Tk()
    frm_anime_display = tk.Frame(window)
    lbl_title = tk.Label(frm_anime_display, text="Anime Data Program", font=("Arial", 15))
    lbl_avg_rating = tk.Label(frm_anime_display, text="Avg Rating Here")
    lbl_house_rating = tk.Label(frm_anime_display, text="House Rating Here")
    cnvs_graph = tk.Canvas(frm_anime_display)
    lbl_cover_image = tk.Label(frm_anime_display)
    lbl_episodes = tk.Label(frm_anime_display, text="Episodes: 0")
    lbl_seasons = tk.Label(frm_anime_display, text="Seasons: 0")
    lbl_unaired_seasons = tk.Label(frm_anime_display, text="Unfinished Seasons: 0")
    lbl_movies = tk.Label(frm_anime_display, text="Movies: 0")
    frm_description = tk.Frame(frm_anime_display, width=300, height=300, borderwidth=2, relief="solid")
    lbl_description = tk.Label(frm_description, text="", wraplength=450)
    lbl_genres = tk.Label(frm_anime_display, text="Genres:")
    lbl_genres_list = tk.Label(frm_anime_display, text="")
    lbl_tags = tk.Label(frm_anime_display, text="Tags:")
    lbl_tags_list = tk.Label(frm_anime_display, text="")
    spoiler_state = tk.IntVar()
    cbox_spoiler_tags = tk.Checkbutton(frm_anime_display, text="\u25B6 Spoiler Tags: (0, 0, 0)",
                                       command=toggle_spoilers, variable=spoiler_state)
    lbl_spoiler_tags = tk.Label(frm_anime_display, text="SPOILERS")
    lbox_options = tk.Listbox(window, height=35)
    btn_options = tk.Button(window, text="Add Options", command=add_options)

    lbox_options.bind("<<ListboxSelect>>", update_page_display)

    lbl_title.grid(row=0, column=0, columnspan=4, pady=8)
    lbl_avg_rating.grid(row=1, column=0)
    lbl_house_rating.grid(row=1, column=1)
    #cnvs_graph.grid(row=2, column=0, rowspan=6, columnspan=2)

    graph_frame = plt.Figure(figsize=(5, 4), dpi=100)
    graph = graph_frame.add_subplot(111)
    graph.grid()
    graph.scatter([50, -50], [50, -50], s=[0, 0])
    scatter_chart = FigureCanvasTkAgg(graph_frame, frm_anime_display)
    scatter_chart.get_tk_widget().grid(row=2, column=0, rowspan=4, columnspan=2)
    graph.set_ylabel("< Drama \u2022 Comedy >")
    graph.set_xlabel("< Slow Pacing \u2022 Fast Pacing >")

    lbl_cover_image.grid(row=2, column=2, rowspan=4)
    lbl_episodes.grid(row=2, column=3)
    lbl_seasons.grid(row=3, column=3)
    lbl_movies.grid(row=4, column=3)
    lbl_unaired_seasons.grid(row=5, column=3)
    lbl_description.grid()
    frm_description.grid(row=6, column=2, rowspan=4, columnspan=2)
    lbl_genres.grid(row=6, column=0)
    lbl_genres_list.grid(row=7, column=0)
    lbl_tags.grid(row=8, column=0)
    lbl_tags_list.grid(row=9, column=0)
    cbox_spoiler_tags.grid(row=10, column=0)

    frm_anime_display.grid()
    lbox_options.grid(row=0, column=1)
    btn_options.grid(row=1, column=1)

    window.mainloop()
