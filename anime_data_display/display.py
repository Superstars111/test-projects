import tkinter as tk
from tkinter import ttk


if __name__ == "__main__":
    window = tk.Tk()
    frm_anime_display = tk.Frame(window)
    lbl_title = tk.Label(frm_anime_display, text="Anime Title Here")
    lbl_avg_rating = tk.Label(frm_anime_display, text="Avg Rating Here")
    lbl_house_rating = tk.Label(frm_anime_display, text="House Rating Here")
    cnvs_graph = tk.Canvas(frm_anime_display)
    lbl_cover_image = tk.Label(frm_anime_display)
    lbl_episodes = tk.Label(frm_anime_display, text="Ep Count Here")
    lbl_seasons = tk.Label(frm_anime_display, text="Season Count Here")
    frm_description = tk.Frame(frm_anime_display, width=300, height=300, borderwidth=2, relief="solid")
    lbl_genres = tk.Label(frm_anime_display, text="Genre List Here")
    lbl_spoiler_genres = tk.Label(frm_anime_display, text="Spoiler Genres Hidden")
    lbl_tags = tk.Label(frm_anime_display, text="Tag List Here")
    lbl_spoiler_tags = tk.Label(frm_anime_display, text="Spoiler Tags Hidden")
    lbox_options = tk.Listbox(window)

    lbl_title.grid(row=0, column=0, columnspan=4)
    lbl_avg_rating.grid(row=1, column=0)
    lbl_house_rating.grid(row=1, column=1)
    cnvs_graph.grid(row=2, column=0, rowspan=3, columnspan=2)
    lbl_cover_image.grid(row=2, column=2)
    lbl_episodes.grid(row=2, column=3)
    lbl_seasons.grid(row=3, column=3)
    frm_description.grid(row=5, column=2, rowspan=4, columnspan=2)
    lbl_genres.grid(row=5, column=0)
    lbl_spoiler_genres.grid(row=6, column=0)
    lbl_tags.grid(row=7, column=0)
    lbl_spoiler_tags.grid(row=8, column=0)

    frm_anime_display.grid()

    window.mainloop()