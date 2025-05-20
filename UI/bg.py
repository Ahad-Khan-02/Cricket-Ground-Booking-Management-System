import customtkinter as ctk
from PIL import Image, ImageTk
import os

def start_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Welcome")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Load background image
    image_path = "bg1.jpg"  # Ensure image exists at this path
    bg_image = Image.open(image_path).resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Create a dark frame (no transparency)
    frame = ctk.CTkFrame(master=root, fg_color="#000000", corner_radius=20)
    frame.place(relx=0.5, rely=0.6, anchor="center")

    # Login Button
    login_btn = ctk.CTkButton(master=frame, text="Login", width=200)
    login_btn.pack(pady=10)

    # Signup Button
    signup_btn = ctk.CTkButton(master=frame, text="Signup", width=200)
    signup_btn.pack(pady=10)

    root.mainloop()

start_screen()
