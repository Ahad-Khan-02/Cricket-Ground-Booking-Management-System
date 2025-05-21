import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from UI.organizer_dashboard import organizer_dashboard_window
from Models.user import get_user_info

def signUp_window():
    
    from UI.heading import heading
    from UI.admin_confirmation import authenticate_admin_window
    from Models.user import register_user,validate_registration
    from UI.login import login_window
    from UI.audience_dashboard import audience_dashboard_window
    
    def signUp(name,email,phone,password,confirm_password,role):

        validation_msg, is_valid = validate_registration(name, email, password, phone, role,confirm_password)
        if not is_valid:
            messagebox.showerror("Validation Error", validation_msg)
            return

        if role == "Admin":
            app.destroy()
            authenticate_admin_window(name,email,password,phone,role)
            return
        else:
            msg, inserted = register_user(name, email, password, phone, role)
            if inserted:
                messagebox.showinfo("Success", msg)
                user_info = get_user_info(email)
                userID=user_info[0]

                if role == 'Audience':
                    app.destroy()
                    audience_dashboard_window(userID)
                else:
                    app.destroy()
                    organizer_dashboard_window(userID)  
            else:
                messagebox.showerror("Database Error", msg)
        


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.attributes("-fullscreen", True)
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))
    app.title("Crickzone - Sign Up")

    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1, minsize=400)  
    app.grid_columnconfigure(0, weight=1)
    
    heading(app, 'Crickzone')

    main_frame = ctk.CTkFrame(master=app)
    main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure((0, 1), weight=1)

    left_frame = ctk.CTkFrame(master=main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    image_path = "Images/image.jpg"
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


    right_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(master=right_frame, text="Sign Up", font=("Montserrat", 24))
    title.grid(row=0, column=0, pady=(20, 10))

    username_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Username")
    username_entry.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

    email_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Gmail")
    email_entry.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    phone_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Phone")
    phone_entry.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

    password_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Password", show="*")
    password_entry.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

    confirm_password_entry = ctk.CTkEntry(master=right_frame, placeholder_text="Confirm Password", show="*")
    confirm_password_entry.grid(row=5, column=0, pady=10, padx=20, sticky="ew")

    checkbox_frame = ctk.CTkFrame(master=right_frame)
    checkbox_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
    checkbox_frame_title = ctk.CTkLabel(master=checkbox_frame, text="Login as", font=("Arial",12))
    checkbox_frame_title.grid(row=0, column=0,padx=0,pady=(0, 10))

    role_var = ctk.StringVar(value="")  

    admin_radio = ctk.CTkRadioButton(checkbox_frame, text="Admin", variable=role_var, value="Admin")
    admin_radio.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    organizer_radio = ctk.CTkRadioButton(checkbox_frame, text="Organizer", variable=role_var, value="Organizer")
    organizer_radio.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    audience_radio = ctk.CTkRadioButton(checkbox_frame, text="Audience", variable=role_var, value="Audience")
    audience_radio.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    signup_button = ctk.CTkButton(master=right_frame, text="Sign Up",command=lambda: signUp(username_entry.get(),email_entry.get(),phone_entry.get(), password_entry.get(),confirm_password_entry.get(),role_var.get()))
    signup_button.grid(row=9, column=0, pady=20, padx=20, sticky="ew")

    login_label = ctk.CTkLabel(master=right_frame, text="Already have an account?")
    login_label.grid(row=10, column=0, pady=(10, 5))

    login_button = ctk.CTkButton(master=right_frame, text="Login",command= lambda: (app.destroy(),login_window()))
    login_button.grid(row=11, column=0, pady=(5, 20), padx=20, sticky="ew")

    app.mainloop()
    


