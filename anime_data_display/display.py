import json
import tkinter as tk
from tkinter import ttk

with open("anime_data.json", "r") as anime_data:
    library = json.load(anime_data)
options = []
option_titles = []
library_titles = []

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
    btn_remove_option = tk.Button(dlg_selection, text="Remove", command=lambda: remove_from_list(options, lbox_selected))

    lbox_library.grid(row=1, column=0, rowspan=4)
    lbox_selected.grid(row=1, column=2, rowspan=4)
    btn_add_option.grid(row=2, column=1)
    btn_remove_option.grid(row=3, column=1)
    btn_confirm.grid(row=5, column=1)
    dlg_selection.wait_window()


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


def update_page_display(test):
    show = options[lbox_options.curselection()[0]]
    seenby = 0
    for rating in (show["jaredScore"][0], show["simonScore"][0], show["kenanScore"][0]):
        if rating > 0:
            seenby += 1

    lbl_title["text"] = f"{show['romajiTitle']} \u2022 {show['englishTitle']} \u2022 {show['nativeTitle']}"
    lbl_avg_rating["text"] = f"Public rating: {show['score']}/100 \u2605"
    lbl_house_rating["text"] = f"House rating: {(show['jaredScore'][0] + show['simonScore'][0] + show['kenanScore'][0])//seenby}/100 \u2605"


if __name__ == "__main__":
    window = tk.Tk()
    frm_anime_display = tk.Frame(window)
    lbl_title = tk.Label(frm_anime_display, text="Anime Title Here", font=("Arial", 15))
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
    lbox_options = tk.Listbox(window, height=35)
    btn_options = tk.Button(window, text="Add Options", command=add_options)

    lbox_options.bind("<<ListboxSelect>>", update_page_display)

    lbl_title.grid(row=0, column=0, columnspan=4, pady=8)
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
    lbox_options.grid(row=0, column=1)
    btn_options.grid(row=1, column=1)

    window.mainloop()
