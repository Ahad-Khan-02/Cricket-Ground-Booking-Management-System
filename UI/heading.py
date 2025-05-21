import customtkinter as ctk

def heading(parent, text):
    label = ctk.CTkLabel(parent, text=text, font=("Bebas Neue", 44, "bold"))
    label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="n")
