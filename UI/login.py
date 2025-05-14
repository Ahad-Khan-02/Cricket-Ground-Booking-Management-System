import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk


def login_window():

    from Models.user import authenticate_user,get_role
    from UI.sign_up import signUp_window
    from UI.audience_dashboard import audience_dashboard_window
    from UI.heading import heading
    
    def login(email,password):
        data=authenticate_user(email,password)
        if data:
            messagebox.showinfo("Login Success")
            role=get_role(email)
            if role == 'Audience':
                app.destroy()
                audience_dashboard_window()
            elif role == 'Organizer':
                app.destroy()
                #organizer_dashnoard_window()
            else:
                app.destroy()
                #admin_dashnoard_window()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.attributes("-fullscreen", True)
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))
    app.title("Cricket Ground Booking - Login")

    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    heading(app, 'Cricketery')

    main_frame = ctk.CTkFrame(master=app)
    main_frame.grid(row=1, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure((0, 1), weight=1) 

    left_frame = ctk.CTkFrame(master=main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    image_path = "bg1.jpg"  
    original_image = Image.open(image_path)

    def resize_image(event):
        frame_width = event.width
        frame_height = event.height

        aspect_ratio = original_image.width / original_image.height

        new_width = frame_width
        new_height = int(new_width / aspect_ratio)

        if new_height > frame_height:
            new_height = frame_height
            new_width = int(new_height * aspect_ratio)

        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=tk_image)
        image_label.image = tk_image

    image_label = ctk.CTkLabel(master=left_frame, text="", image="")
    image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    left_frame.bind("<Configure>", resize_image)

    right_frame = ctk.CTkFrame(master=main_frame, fg_color="#000000")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    right_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(master=right_frame, text="Login", font=("Arial", 24))
    title.grid(row=0, column=0, pady=(20, 10))

    email_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Email")
    email_entry.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

    password_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Password", show="*")
    password_entry.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    login_button = ctk.CTkButton(master=right_frame, text="Login",command=lambda: login(email_entry.get(), password_entry.get()))
    login_button.grid(row=4, column=0, pady=20, padx=20, sticky="ew")

    signup_label = ctk.CTkLabel(master=right_frame, text="Don't have an account?")
    signup_label.grid(row=5, column=0, pady=(10, 5))

    signup_button = ctk.CTkButton(master=right_frame, text="Sign Up",command=lambda: (app.destroy(),signUp_window()))
    signup_button.grid(row=6, column=0, pady=(5, 20), padx=20, sticky="ew")

    app.mainloop()
    
   
