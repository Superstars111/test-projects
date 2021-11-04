import tkinter as tk

window = tk.Tk()
window.title("Address Entry Form")

frm_data_collection = tk.Frame(relief=tk.SUNKEN, borderwidth=3)

frm_data_collection.rowconfigure([i for i in range(8)], minsize=20)
frm_data_collection.columnconfigure(0, minsize=50)
frm_data_collection.columnconfigure(1, minsize=100)

lbl_f_name = tk.Label(master=frm_data_collection, text="First Name:")
ent_f_name = tk.Entry(master=frm_data_collection, width=50)
lbl_l_name = tk.Label(master=frm_data_collection, text="Last Name:")
ent_l_name = tk.Entry(master=frm_data_collection, width=50)
lbl_address1 = tk.Label(master=frm_data_collection, text="Address Line 1:")
ent_address1 = tk.Entry(master=frm_data_collection, width=50)
lbl_address2 = tk.Label(master=frm_data_collection, text="Address Line 2:")
ent_address2 = tk.Entry(master=frm_data_collection, width=50)
lbl_city = tk.Label(master=frm_data_collection, text="City:")
ent_city = tk.Entry(master=frm_data_collection, width=50)
lbl_state = tk.Label(master=frm_data_collection, text="State/Province:")
ent_state = tk.Entry(master=frm_data_collection, width=50)
lbl_postal_code = tk.Label(master=frm_data_collection, text="Postal Code:")
ent_postal_code = tk.Entry(master=frm_data_collection, width=50)
lbl_country = tk.Label(master=frm_data_collection, text="Country:")
ent_country = tk.Entry(master=frm_data_collection, width=50)

lbl_f_name.grid(row=0, column=0, sticky="e")
ent_f_name.grid(row=0, column=1)
lbl_l_name.grid(row=1, column=0, sticky="e")
ent_l_name.grid(row=1, column=1)
lbl_address1.grid(row=2, column=0, sticky="e")
ent_address1.grid(row=2, column=1)
lbl_address2.grid(row=3, column=0, sticky="e")
ent_address2.grid(row=3, column=1)
lbl_city.grid(row=4, column=0, sticky="e")
ent_city.grid(row=4, column=1)
lbl_state.grid(row=5, column=0, sticky="e")
ent_state.grid(row=5, column=1)
lbl_postal_code.grid(row=6, column=0, sticky="e")
ent_postal_code.grid(row=6, column=1)
lbl_country.grid(row=7, column=0, sticky="e")
ent_country.grid(row=7, column=1)


frm_confirmation = tk.Frame()

btn_clear = tk.Button(master=frm_confirmation, text="Clear")
btn_submit = tk.Button(master=frm_confirmation, text="Submit")

btn_clear.grid(row=0, column=0, sticky="e", padx=0, pady=5, ipadx=8)
btn_submit.grid(row=0, column=1, sticky="e", padx=8, pady=5, ipadx=8)

frm_data_collection.grid()
frm_confirmation.grid(sticky="e")

window.mainloop()
