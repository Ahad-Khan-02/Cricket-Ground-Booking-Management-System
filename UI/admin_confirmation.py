import customtkinter as ctk
from tkinter import messagebox
from UI.admin_dashboard import admin_dashboard_window


def authenticate_admin_window(name,email,password,phone,role):
    
    from UI.sign_up import signUp_window
    from Models.user import register_user

    def authenticate_admin(adminid, adminpassword):
            id='admin'
            pw='cricket123'
            if adminid == id and adminpassword == pw:
                messagebox.showinfo("Authenticated", "Admin Confirmed")
                msg, inserted = register_user(name, email, password, phone, role)
                if inserted:
                    messagebox.showinfo("Success", msg)
                    win.destroy()
                    admin_dashboard_window()         
                else:
                    messagebox.showerror("Database Error", msg)
                    signUp_window()
            else:
                messagebox.showerror("Error", "Invalid ID and Password")
    

    win = ctk.CTk()
    win.attributes("-fullscreen", True)
    win.bind("<Escape>", lambda e: win.attributes("-fullscreen", False))
    win.title("Admin Authentication")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    win.configure(fg_color="#0D1B2A")

    frame = ctk.CTkFrame(win, fg_color="#1A1A2E")
    frame.pack(pady=30, padx=30, fill="both", expand=True)

    heading_ = ctk.CTkLabel(frame, text="ADMIN AUTHENTICATION", font=("Montserrat", 28, "bold"), text_color="white")
    heading_.pack(pady=20)

    adminID_entry = ctk.CTkEntry(frame, placeholder_text="Enter Admin ID")
    adminID_entry.pack(pady=5)

    adminPassword_entry = ctk.CTkEntry(frame, placeholder_text="Enter Admin Password", show="*")
    adminPassword_entry.pack(pady=5)

    confirm_btn = ctk.CTkButton(frame, text="Confirm",
                                command=lambda: authenticate_admin(adminID_entry.get(), adminPassword_entry.get()))
    confirm_btn.pack(pady=30)
    
    back_btn = ctk.CTkButton(frame, text="Back",
                                command=lambda: (win.destroy(),signUp_window()))
    back_btn.pack(pady=30)

    win.mainloop()

