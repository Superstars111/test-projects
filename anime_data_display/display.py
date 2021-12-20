import json
import requests as rq
import collection
import tkinter as tk
import tkinter.font as fnt
import urllib.request
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas
import decimal as dc
import alphabetize

with open("anime_data.json", "r") as anime_data:
    library = json.load(anime_data)
options = []
option_titles = []
library_titles = []
cover_image = []
mild_warnings = ("Afterlife", "Ahegao", "Angels", "Assassins", "Bisexual", "Body Swapping", "Bullying", "Cosmic Horror", "Crossdressing", "Death Game", "DILF", "Drugs", "Ero Guru", "Feet", "Female Harem", "Flat Chest", "Gambling", "Gangs", "Gender Bending", "Ghost", "Gods", "Large Breasts", "Male Harem", "Masochism", "MILF", "Oiran", "Prostitution", "Reincarnation", "Slavery", "Succubus", "Sweat", "Teens' Love", "Tentacles", "Terrorism", "Virginity", "Yandere", "Youkai")
extreme_warnings = ("Anal Sex", "Ashikoki", "Body Horror", "Boobjob", "Boy's Love", "Cannibalism", "Cunnilingus", "Defloration", "Ero Guro", "Exhibitionism", "Facial", "Fellatio", "Femdom", "Flash", "Futanari", "Gore", "Group Sex", "Handjob", "Incest", "Inseki", "Irrumatio", "Lactation", "LGBTQ+ Themes", "Masturmation", "Nakadashi", "Netorare", "Netorase", "Netori", "Nudity", "Public Sex", "Rape", "Rimjob", "Scat", "Scissoring", "Sex Toys", "Suicide", "Sumata", "Threesome", "Torture", "Transgenger", "Vore", "Voyeur", "Yaoi", "Yuri")
content_warnings = [0, 0, 0]

for show in library:
    library_titles.append(show["defaultTitle"])


class Root:
    def __init__(self, parent):
        self.parent = parent
        parent.title("Anime Data Displayinator 9001 (Beta)")
        self.show = {}
        self.spoiler_state = tk.IntVar()

        self.lbox_options = tk.Listbox(self.parent, height=35)
        self.lbox_options.bind("<<ListboxSelect>>", self.update_page_display)
        self.btn_options = tk.Button(self.parent, text="Add Options", command=self.add_options)

        # Build main window
        self.frm_anime_display = tk.Frame(self.parent)
        self.lbl_title = tk.Label(self.frm_anime_display, text="Anime Data Program", font=("Arial", 20), wraplength=900)

        # Build ratings frame
        self.frm_ratings = tk.Frame(self.frm_anime_display)
        self.lbl_avg_rating = tk.Label(self.frm_ratings, text="Public score: 0/100")
        self.lbl_house_rating = tk.Label(self.frm_ratings, text="House score: 0/100")
        self.lbl_public_star = tk.Label(self.frm_ratings, text="\u2605")
        self.lbl_house_star = tk.Label(self.frm_ratings, text="\u2605")
        graph_frame = plt.Figure(figsize=(5, 4), dpi=100)
        graph = graph_frame.add_subplot(111)
        graph.scatter([50, -50], [50, -50], s=[0, 0])
        scatter_chart = FigureCanvasTkAgg(graph_frame, self.frm_ratings)
        graph.set_ylabel("< Drama \u2022 Comedy >")
        graph.set_xlabel("< Slow Pacing \u2022 Fast Pacing >")

        # Build data frame
        self.frm_series_info = tk.Frame(self.frm_anime_display)
        self.lbl_cover_image = tk.Label(self.frm_series_info)
        self.lbl_episodes = tk.Label(self.frm_series_info, text="Episodes: 0")
        self.lbl_seasons = tk.Label(self.frm_series_info, text="Seasons: 0")
        self.lbl_unaired_seasons = tk.Label(self.frm_series_info, text="Unfinished Seasons: 0", width=22)
        self.lbl_movies = tk.Label(self.frm_series_info, text="Movies: 0")

        # Build tags frame
        self.frm_tags = tk.Frame(self.frm_anime_display)
        lbl_genres = tk.Label(self.frm_tags, text="Genres:")
        self.lbl_genres_list = tk.Label(self.frm_tags, text="", wraplength=490)
        lbl_tags = tk.Label(self.frm_tags, text="Tags:")
        self.lbl_tags_list = tk.Label(self.frm_tags, text="", wraplength=490)
        lbl_warnings = tk.Label(self.frm_tags, text="Content Warnings:")
        self.lbl_warnings_list = tk.Label(self.frm_tags, text="", wraplength=490)
        self.cbox_spoiler_tags = tk.Checkbutton(self.frm_tags, text="\u25B6 Spoiler Tags: (0, 0, 0)",
                                                command=self.toggle_spoilers, variable=self.spoiler_state)
        self.lbl_spoiler_tags = tk.Label(self.frm_tags, text="SPOILERS! Hide this before selecting a series.",
                                         wraplength=490)

        # Build synopsis frame
        self.frm_description = tk.Frame(self.frm_anime_display, width=300, height=300, borderwidth=2, relief="solid")
        self.txt_description = tk.Text(self.frm_description, height=18, width=55, state="disabled",
                                       wrap="word", font=default_font, bg="gray92")
        self.sbar = tk.Scrollbar(self.frm_description, orient=tk.VERTICAL, command=self.txt_description.yview)


        # Grid main window
        self.lbox_options.grid(row=0, column=1, sticky="ns", padx=10, pady=5)
        self.btn_options.grid(row=1, column=1, pady=7, padx=3, sticky="n")
        self.frm_anime_display.grid(row=0, column=0)
        self.frm_anime_display.rowconfigure(0, minsize=120)
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=8)

        # Grid ratings frame
        self.frm_ratings.grid(row=1, column=0, padx=15)
        self.lbl_avg_rating.grid(row=0, column=0, sticky="e")
        self.lbl_public_star.grid(row=0, column=1, sticky="w")
        self.lbl_house_rating.grid(row=0, column=2, sticky="e")
        self.lbl_house_star.grid(row=0, column=3, sticky="w")
        graph.grid()
        scatter_chart.get_tk_widget().grid(row=1, column=0, columnspan=4)

        # Grid data frame
        self.lbl_cover_image.grid(row=0, column=0, rowspan=4, sticky="w", padx=15)
        self.lbl_episodes.grid(row=0, column=1)
        self.lbl_seasons.grid(row=1, column=1)
        self.lbl_movies.grid(row=2, column=1)
        self.lbl_unaired_seasons.grid(row=3, column=1)
        self.frm_series_info.grid(row=1, column=1)
        self.frm_series_info.rowconfigure((0, 1, 2, 3), minsize=90)
        self.frm_series_info.columnconfigure(0, minsize=270)

        # Grid tags frame
        self.frm_tags.grid(row=2, column=0, sticky="n")
        lbl_genres.grid(row=0, column=0, sticky="n")
        self.frm_tags.rowconfigure(1, minsize=50)
        self.lbl_genres_list.grid(row=1, column=0)
        lbl_tags.grid(row=2, column=0, sticky="n")
        self.frm_tags.rowconfigure(3, minsize=115)
        self.lbl_tags_list.grid(row=3, column=0)
        lbl_warnings.grid(row=4, column=0)
        self.frm_tags.rowconfigure(5, minsize=50)
        self.lbl_warnings_list.grid(row=5, column=0)
        self.cbox_spoiler_tags.grid(row=6, column=0)
        self.frm_tags.rowconfigure(7, minsize=70)

        # Grid synopsis frame
        self.frm_description.grid(row=2, column=1, padx=15)
        self.frm_description.columnconfigure(0, minsize=450)
        self.frm_description.rowconfigure(0, minsize=330)
        self.txt_description.grid(row=0, column=0)
        self.sbar.grid(row=0, column=1, sticky="ns")

    def add_options(self):

        dlg_selection = SelectionWindow(self.parent)
        dlg_selection.title("Option Selector")
        dlg_selection.transient(self.parent)
        dlg_selection.grab_set()
        dlg_selection.wait_window()

    def update_page_display(self, *ignore):
        self.show = options[self.lbox_options.curselection()[0]]
        seenby = 0
        total_house_score = 0
        content_warnings[0] = 0
        content_warnings[1] = 0
        content_warnings[2] = 0
        normal_tags, warning_tags, spoiler_tags = self.sort_tags()
        self.plot_graph()

        # Get average household score
        for rating in (self.show["houseScores"]):
            if rating[1]:
                seenby += 1
                total_house_score += rating[1]
        if seenby > 0:
            avg_house_score = total_house_score / seenby
            dc.getcontext().rounding = dc.ROUND_HALF_UP
            avg_house_score = int(dc.Decimal(str(avg_house_score)).quantize(dc.Decimal("1")))
        else:
            avg_house_score = 0

        # Set stars to correct colors
        if self.show["score"] >= 85:
            self.lbl_public_star.config(fg="purple")
        elif self.show["score"] >= 70:
            self.lbl_public_star.config(fg="blue")
        elif self.show["score"] >= 55:
            self.lbl_public_star.config(fg="orange")
        elif self.show["score"] >= 1:
            self.lbl_public_star.config(fg="red")
        else:
            self.lbl_public_star.config(fg="black")

        if avg_house_score >= 85:
            self.lbl_house_star.config(fg="purple")
        elif avg_house_score >= 70:
            self.lbl_house_star.config(fg="blue")
        elif avg_house_score >= 55:
            self.lbl_house_star.config(fg="orange")
        elif avg_house_score >= 1:
            self.lbl_house_star.config(fg="red")
        else:
            self.lbl_house_star.config(fg="black")

        # Toggle display
        if self.show["unairedSeasons"] == 0:
            self.lbl_unaired_seasons["text"] = ""
        else:
            self.lbl_unaired_seasons["text"] = f"Unfinished Seasons: {self.show['unairedSeasons']}"

        if self.spoiler_state.get() == 1:
            self.cbox_spoiler_tags[
                "text"] = f"\u25BC Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"
        else:
            self.cbox_spoiler_tags[
                "text"] = f"\u25B6 Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"

        # Update display values
        self.lbl_title["text"] = f"{self.show['romajiTitle']} \u2022 {self.show['englishTitle']} \u2022 {self.show['nativeTitle']}"
        self.lbl_avg_rating["text"] = f"Public score: {self.show['score']}/100"
        self.lbl_house_rating["text"] = f"House score: {avg_house_score}/100"
        self.lbl_cover_image["image"] = convert_image(self.show["coverMed"])
        self.lbl_episodes["text"] = f"Total episodes: {self.show['episodes']}"
        self.lbl_seasons["text"] = f"Seasons: {self.show['seasons']}"
        self.lbl_movies["text"] = f"Movies: {self.show['movies']}"
        self.txt_description["state"] = "normal"
        self.txt_description.delete("1.0", tk.END)
        self.txt_description.insert("1.0", self.show["description"])
        self.txt_description["state"] = "disabled"
        self.lbl_genres_list["text"] = f"{', '.join(self.show['genres'])}"
        self.lbl_tags_list["text"] = f"{', '.join(normal_tags)}"
        self.lbl_warnings_list["text"] = f"{', '.join(warning_tags)}"
        self.lbl_spoiler_tags["text"] = f"{', '.join(spoiler_tags)}"

    def plot_graph(self):
        self.frm_ratings.grid_slaves(row=1, column=0)[0].grid_remove()
        scores = [rating for rating in self.show["houseScores"]]
        ratings = [score_list[1] for score_list in scores]
        pacing_scores = []
        drama_scores = []
        for idx, score in enumerate(ratings):
            if score > 0:
                pacing_scores.append(scores[idx][2])
                drama_scores.append(scores[idx][3])

        graph_location = {
            "pacing": pacing_scores,
            "comedy": drama_scores
        }
        data_sorting = pandas.DataFrame(graph_location, columns=["pacing", "comedy"])
        graph_frame = plt.Figure(figsize=(5, 4), dpi=100)
        graph = graph_frame.add_subplot(111)
        graph.grid()
        graph.scatter([50, -50], [50, -50], s=[0, 0])
        scatter_chart = FigureCanvasTkAgg(graph_frame, self.frm_ratings)
        scatter_chart.get_tk_widget().grid(row=1, column=0, columnspan=4)
        graph.set_ylabel("< Drama \u2022 Comedy >")
        graph.set_xlabel("< Low Energy/Slow Pacing \u2022 Fast Pacing/High Energy >")
        graph.scatter(data_sorting["pacing"], data_sorting["comedy"], color="g")

    def toggle_spoilers(self):
        if self.spoiler_state.get() == 1:
            self.lbl_spoiler_tags.grid(row=7, column=0)
            self.cbox_spoiler_tags[
                "text"] = f"\u25BC Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"
        else:
            self.lbl_spoiler_tags.grid_remove()
            self.cbox_spoiler_tags[
                "text"] = f"\u25B6 Spoiler Tags: ({content_warnings[0]}, {content_warnings[1]}, {content_warnings[2]})"

    def sort_tags(self):
        normal_tags = []
        warning_tags = []
        spoiler_tags = []
        for tag in self.show["tags"]:
            if tag["isMediaSpoiler"]:
                spoiler_tags.append(f"{tag['name']} ({tag['rank']}%)")
                if tag["name"] in extreme_warnings:
                    content_warnings[2] += 1
                elif tag["name"] in mild_warnings:
                    content_warnings[1] += 1
                else:
                    content_warnings[0] += 1
            elif tag["name"] in mild_warnings or tag["name"] in extreme_warnings:
                warning_tags.append(f"{tag['name']} ({tag['rank']}%)")
            else:
                normal_tags.append(f"{tag['name']} ({tag['rank']}%)")

        return normal_tags, warning_tags, spoiler_tags


class SelectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selection_frame = tk.Frame(self)
        self.library_var = tk.StringVar(value=library_titles)
        self.options_var = tk.StringVar(value=option_titles)
        self.btn_confirm = tk.Button(self.selection_frame, text="Confirm choices", command=lambda: self.dismiss_window())
        self.lbox_library = tk.Listbox(self.selection_frame, listvariable=self.library_var)
        self.lbox_selected = tk.Listbox(self.selection_frame, listvariable=self.options_var)
        self.btn_add_option = tk.Button(self.selection_frame, text="Add", command=self.add_to_list)
        self.lbox_library.bind("<Double-1>", lambda x: self.add_to_list())
        self.btn_remove_option = tk.Button(self.selection_frame, text="Remove",
                                           command=lambda: self.remove_from_list(options))
        self.lbox_selected.bind("<Double-1>", lambda x: self.remove_from_list(options))
        self.btn_edit_library = tk.Button(self.selection_frame, text="Edit Entry", command=self.add_to_library)

        self.lbox_library.grid(row=1, column=0, rowspan=4)
        self.lbox_selected.grid(row=1, column=2, rowspan=4)
        self.btn_add_option.grid(row=2, column=1, padx=7, pady=3, sticky="ew")
        self.btn_remove_option.grid(row=3, column=1, padx=7, pady=3, sticky="ew")
        self.btn_confirm.grid(row=5, column=1, padx=3, pady=3)
        self.btn_edit_library.grid(row=5, column=0, padx=3, pady=3)
        self.selection_frame.grid()

    def add_to_library(self):
        dlg_addition = EditWindow(self.parent)
        dlg_addition.title("Library Editor")
        dlg_addition.transient(self.parent)
        dlg_addition.grab_set()
        dlg_addition.wait_window()

    def add_to_list(self):
        selected = self.lbox_library.curselection()[0]

        if library_titles[selected] not in option_titles:
            options.append(library[selected])
            option_titles.append(library_titles[selected])

        options_var = tk.StringVar(value=option_titles)
        self.lbox_selected["listvariable"] = options_var

    def remove_from_list(self, options_list):
        options_list.pop(self.lbox_selected.curselection()[0])
        option_titles.pop(self.lbox_selected.curselection()[0])

        options_list_var = tk.StringVar(value=option_titles)
        self.lbox_selected["listvariable"] = options_list_var

    def dismiss_window(self):
        self.grab_release()
        self.destroy()
        options_var = tk.StringVar(value=option_titles)
        window.lbox_options["listvariable"] = options_var


class EditWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.edit_frame = tk.Frame(self)
        self.current_show = {}

        self.lbl_id_no = tk.Label(self.edit_frame, text="ID no.")
        self.ent_id_no = tk.Entry(self.edit_frame, width=15)
        self.btn_confirm_id = tk.Button(self.edit_frame, text="Confirm", command=self.update_series)
        self.bind("<Return>", self.update_series)
        self.lbl_show_name = tk.Label(self.edit_frame)
        self.frm_user_ratings = tk.Frame(self.edit_frame)
        lbl_name = tk.Label(self.frm_user_ratings, text="Name")
        lbl_score = tk.Label(self.frm_user_ratings, text="Score")
        lbl_energy = tk.Label(self.frm_user_ratings, text="Energy")
        lbl_drama = tk.Label(self.frm_user_ratings, text="Tone")

        self.adjust_rows()

        btn_confirm_scores = tk.Button(self.edit_frame, text="Confirm", command=self.enter_ratings)
        btn_add_user = tk.Button(self.edit_frame, text="Add User", command=self.add_user)

        self.lbl_id_no.grid(row=0, column=0)
        self.ent_id_no.grid(row=0, column=1, columnspan=2)
        self.btn_confirm_id.grid(row=0, column=3, padx=3, pady=3)
        self.edit_frame.rowconfigure(1, minsize=15)
        self.lbl_show_name.grid(row=1, column=0, columnspan=4)
        self.frm_user_ratings.grid(row=2, column=0, columnspan=4)
        lbl_name.grid(row=0, column=0)
        lbl_score.grid(row=0, column=1)
        lbl_energy.grid(row=0, column=2)
        lbl_drama.grid(row=0, column=3)
        btn_confirm_scores.grid(row=3, column=2, padx=3, pady=3)
        btn_add_user.grid(row=3, column=1, padx=3, pady=3)
        self.edit_frame.grid()

    def update_series(self, *ignore):
        media_id = self.ent_id_no.get()
        self.get_series(media_id)
        if self.current_show["englishTitle"]:
            self.lbl_show_name["text"] = self.current_show["englishTitle"]
        else:
            self.lbl_show_name["text"] = self.current_show["romajiTitle"]
        user_reviews = [rating for rating in self.current_show["houseScores"]]

        self.adjust_rows()

        for row, user in enumerate(user_reviews):
            for col in range(4):
                for widget in self.frm_user_ratings.grid_slaves(row=row+1, column=col):
                    widget["state"] = "normal"
                    widget.delete(0, tk.END)
                    widget.insert(0, user[col])

    def get_series(self, media_id):
        id_var = {"id": media_id}
        request = rq.post(collection.url, json={"query": collection.query, "variables": id_var}).json()['data']["Media"]
        if request["format"] == "MOVIE":
            seasonal_data = {
                "total_episodes": 0,
                "seasons": 0,
                "unaired_seasons": 0,
                "movies": 1,
                "sequel": None
            }
        else:
            seasonal_data = {
                "total_episodes": request["episodes"],
                "seasons": 1,
                "unaired_seasons": 0,
                "movies": 0,
                "sequel": None
            }

        seasonal_data = collection.collect_seasonal_data(
            media_id,
            episodes=seasonal_data["total_episodes"],
            seasons=seasonal_data["seasons"],
            movies=seasonal_data["movies"])

        if request["title"]["english"]:
            title = request["title"]["english"]
        else:
            title = request["title"]["romaji"]

        entry = {
            "id": media_id,
            "romajiTitle": request["title"]["romaji"],
            "englishTitle": request["title"]["english"],
            "nativeTitle": request["title"]["native"],
            "format": request["format"],
            "description": request["description"],
            "episodes": seasonal_data["total_episodes"],
            "seasons": seasonal_data["seasons"],
            "unairedSeasons": seasonal_data["unaired_seasons"],
            "movies": seasonal_data["movies"],
            "coverLarge": request["coverImage"]["extraLarge"],
            "coverMed": request["coverImage"]["large"],
            "coverSmall": request["coverImage"]["medium"],
            "genres": request["genres"],
            "tags": request["tags"],
            "score": request["averageScore"],
            "defaultTitle": title,
            "houseScores": [["", 0, 0, 0]]
        }

        for show in library:
            if media_id == show["id"]:
                entry["houseScores"] = show["houseScores"]

        self.current_show = entry

    def enter_ratings(self):
        rows = count_rows(self.frm_user_ratings.grid_slaves())
        # user_scores = [score for score in self.current_show["houseScores"]]
        for row in range(rows):
            for col in range(4):
                for widget in self.frm_user_ratings.grid_slaves(row=row, column=col):
                    if row != 0:
                        if row-1 == len(self.current_show["houseScores"]):
                            self.current_show["houseScores"].append(["", 0, 0, 0])
                        if col == 0:
                            self.current_show["houseScores"][row-1][col] = widget.get()
                            widget["state"] = "disabled"
                        else:
                            self.current_show["houseScores"][row-1][col] = int(widget.get())
                            widget["state"] = "disabled"

        match_found = False
        lib_clone = library.copy()
        for idx, show in enumerate(lib_clone):
            if self.current_show["id"] == show["id"]:
                library[idx] = self.current_show
                match_found = True

        if not match_found:  # FIXME: Local library doesn't update properly when adding new shows
            alphabetize.insert_alphabetically(self.current_show, library)
            library_titles[0:-1] = []
            for show in library:
                library_titles.append(show["defaultTitle"])

        self.lbl_show_name["text"] = "Data Confirmed!"

    def add_user(self):
        rows = count_rows(self.frm_user_ratings.grid_slaves())
        # rows = 0
        # for idx in range(len(self.frm_user_ratings.grid_slaves())):
        #     if idx % 4 == 0:
        #         rows += 1

        ent_user = tk.Entry(self.frm_user_ratings)
        ent_user.grid(row=rows, column=0, padx=3)
        for col in range(3):
            ent_score = tk.Entry(self.frm_user_ratings, width=5)
            ent_score.grid(row=rows, column=col+1, padx=3)

    def adjust_rows(self):
        for idx, widget in enumerate(self.frm_user_ratings.grid_slaves()):
            if idx < (len(self.frm_user_ratings.grid_slaves()) - 4):
                widget.destroy()
        if self.current_show:
            users = self.current_show["houseScores"]
        else:
            users = []
        for row, user in enumerate(users):
            # lbl_user = tk.Label(self.frm_user_ratings, text=f"{user}: ")
            # lbl_user.grid(row=row + 1, column=0)
            ent_user = tk.Entry(self.frm_user_ratings)
            ent_user.grid(row=row + 1, column=0, padx=3)
            for col in range(3):
                ent_score = tk.Entry(self.frm_user_ratings, width=5)
                ent_score.grid(row=row + 1, column=col + 1, padx=3)


def convert_image(url):
    raw_url = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    raw_image = urllib.request.urlopen(raw_url).read()
    image_data = Image.open(io.BytesIO(raw_image))
    image = ImageTk.PhotoImage(image_data)
    if image not in cover_image:
        cover_image.append(image)

    return image


def count_rows(item):
    rows = 0
    for idx in range(len(item)):
        if idx % 4 == 0:
            rows += 1

    return rows


if __name__ == "__main__":
    application = tk.Tk()
    default_font = fnt.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window = Root(application)

    application.mainloop()

    with open("anime_data.json", "w") as anime_data:
        json.dump(library, anime_data, indent=4)
