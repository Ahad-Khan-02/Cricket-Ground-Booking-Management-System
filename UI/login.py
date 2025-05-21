import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from UI.admin_dashboard import admin_dashboard_window
from UI.organizer_dashboard import organizer_dashboard_window


def login_window():

    from Models.user import authenticate_user,get_user_info
    from UI.sign_up import signUp_window
    from UI.audience_dashboard import audience_dashboard_window
    from UI.heading import heading
    
    def login(email,password):
        if not email or not password:
            messagebox.showerror("Login Failed", "Both email and password are required to log in.")
            return
        data=authenticate_user(email,password)
        if data:
            messagebox.showinfo("Login Successful", "You have successfully logged in.")
            user_info=get_user_info(email)
            role=user_info[3]
            userID=user_info[0]
            if role == 'Audience':
                app.destroy()
                audience_dashboard_window(userID)
            elif role == 'Organizer':
                app.destroy()
                organizer_dashboard_window(userID)
            else:
                app.destroy()
                admin_dashboard_window()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.attributes("-fullscreen", True)
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))
    app.title("CrickZone - Login")

    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    heading(app, 'CrickZone')

    main_frame = ctk.CTkFrame(master=app)
    main_frame.grid(row=1, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure((0, 1), weight=1) 

    left_frame = ctk.CTkFrame(master=main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        image_path = os.path.join(script_dir, "..", "Images", "image.jpg")
        image_path = os.path.abspath(image_path)
        original_image = Image.open(image_path)
        resized_image = original_image.resize((800, 650), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label = ctk.CTkLabel(master=left_frame, text="", image=tk_image)
        image_label.image = tk_image
    except Exception as e:
        image_label = ctk.CTkLabel(master=left_frame, text="Image not found", font=("Arial", 20))
    image_label.grid(row=0, column=0, padx=10, pady=10)

    right_frame = ctk.CTkFrame(master=main_frame, fg_color="#000000")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    right_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(master=right_frame, text="Login", font=("Montserrat", 24))
    title.grid(row=0, column=0, pady=(20, 10))

    email_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Gmail")
    email_entry.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
    email_entry.focus()


    password_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Password", show="*")
    password_entry.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    login_button = ctk.CTkButton(master=right_frame, text="Login",command=lambda: login(email_entry.get(), password_entry.get()))
    login_button.grid(row=4, column=0, pady=20, padx=20, sticky="ew")

    signup_label = ctk.CTkLabel(master=right_frame, text="Don't have an account?")
    signup_label.grid(row=5, column=0, pady=(10, 5))

    signup_button = ctk.CTkButton(master=right_frame, text="Sign Up",command=lambda: (app.destroy(),signUp_window()))
    signup_button.grid(row=6, column=0, pady=(5, 20), padx=20, sticky="ew")

    app.mainloop()
    
   
