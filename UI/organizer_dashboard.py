import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import re
from Models.organizer import get_all_grounds, is_ground_available, insert_organizer_booking_and_payment, get_organizer_id, get_ground_id, get_match_id
from UI.organizer_voucher import generate_organizer_voucher
from Models.seats import populate_seats

selected_ground = None
booking_data = {}
ground_info = {}

def is_english(text):
    """Check if text contains only English characters and spaces"""
    return bool(re.match('^[a-zA-Z ]+$', text))

def heading(parent, text):
    label = ctk.CTkLabel(parent, text=text, font=("Arial Bold", 28), text_color="#FFD700")
    label.pack(pady=20)

def open_payment_window(userID):
    global booking_data
    global ground_info

    payment_win = ctk.CTkToplevel()
    payment_win.title("Payment Confirmation")
    payment_win.geometry("550x700")
    payment_win.configure(fg_color="#1A1A1A")

    payment_win.geometry("{0}x{1}+0+0".format(payment_win.winfo_screenwidth(), payment_win.winfo_screenheight()))
    payment_win.configure(fg_color="#0D1B2A")

    heading(payment_win, "Confirm & Pay")

    scroll_frame = ctk.CTkScrollableFrame(payment_win, fg_color="#2A2A2A")
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    total_amount = booking_data['total_hours'] * booking_data['hourly_rate']

    entries = [
        ("Ground Name", booking_data['ground_name']),
        ("Booking Date", booking_data['booking_date'].strftime('%Y-%m-%d')),
        ("Total Hours", str(booking_data['total_hours'])),
        ("Amount", f"Rs {total_amount:.2f}"),
        ("Match Title", booking_data['match_title']),
        ("Match Date", booking_data['match_date'].strftime('%Y-%m-%d')),
        ("Start Time", booking_data['start_time'].strftime('%H:%M')),
        ("End Time", booking_data['end_time'].strftime('%H:%M')),
        ("Team A", booking_data['team_a']),
        ("Team B", booking_data['team_b'])
    ]

    for label, value in entries:
        ctk.CTkLabel(scroll_frame, text=label, font=("Arial Bold", 14)).pack(anchor="w", padx=10, pady=4)
        entry = ctk.CTkEntry(scroll_frame)
        entry.insert(0, value)
        entry.configure(state="disabled")
        entry.pack(fill="x", padx=20, pady=2)

    def confirm_and_pay(organizerID):
        ground_name = booking_data['ground_name']
        success, result = insert_organizer_booking_and_payment(
            organizerID,
            ground_id=get_ground_id(ground_name),
            booking_date=booking_data['booking_date'],
            total_hours=booking_data['total_hours'],
            match_title=booking_data['match_title'],
            match_date=booking_data['match_date'],
            start_time=booking_data['start_time'],
            team_a=booking_data['team_a'],
            team_b=booking_data['team_b'],
            hourly_rate=booking_data['hourly_rate']
        )
        if success:
            voucher_path = generate_organizer_voucher(booking_data, ground_info)
            messagebox.showinfo(
                "Success", 
                f"Payment successful!\n"
                f"Voucher saved to:\n{voucher_path}"
            )
            matchID=get_match_id(booking_data['match_title'],booking_data['match_date'])
            populate_seats(matchID,ground_info['capacity'])
            payment_win.destroy()
            organizer_dashboard_window(organizerID)
        else:
            messagebox.showerror("Error", f"Payment failed: {result}")
        # payment_win.destroy()
        # organizer_dashboard_window(organizerID)

    ctk.CTkButton(payment_win, text="Confirm & Pay", command=lambda: (confirm_and_pay(userID))).pack(pady=20)

def open_booking_window(ground, app,userID):
    global ground_info
    global selected_ground
    selected_ground = ground
    ground_id, name, location, capacity, rate = ground
    ground_info = {
        'ground_id': ground_id,
        'ground_name': name,
        'location': location,
        'capacity': capacity,
        'hourly_rate': rate
    }
    app.withdraw()

    win = ctk.CTkToplevel()
    win.title("Booking Details")
    win.geometry("550x850")
    win.configure(fg_color="#1A1A1A")

    win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
    win.configure(fg_color="#0D1B2A")

    heading(win, "Booking Details")

    scroll_frame = ctk.CTkScrollableFrame(win, fg_color="#2A2A2A")
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Ground Info Section
    ctk.CTkLabel(scroll_frame, text="Ground Name", font=("Arial Bold", 14)).pack(pady=2)
    gn = ctk.CTkEntry(scroll_frame)
    gn.insert(0, name)
    gn.configure(state="disabled")
    gn.pack(pady=2)

    ctk.CTkLabel(scroll_frame, text="Location", font=("Arial Bold", 14)).pack(pady=2)
    gl = ctk.CTkEntry(scroll_frame)
    gl.insert(0, location)
    gl.configure(state="disabled")
    gl.pack(pady=2)

    ctk.CTkLabel(scroll_frame, text="Capacity", font=("Arial Bold", 14)).pack(pady=2)
    gc = ctk.CTkEntry(scroll_frame)
    gc.insert(0, str(capacity))
    gc.configure(state="disabled")
    gc.pack(pady=2)

    ctk.CTkLabel(scroll_frame, text="Hourly Rate", font=("Arial Bold", 14)).pack(pady=2)
    gr = ctk.CTkEntry(scroll_frame)
    gr.insert(0, f"Rs {rate}/hr")
    gr.configure(state="disabled")
    gr.pack(pady=2)

    entries = {}
    today = datetime.today().date()
    today_str = today.strftime('%Y-%m-%d')

    ctk.CTkLabel(scroll_frame, text="Booking Date", font=("Arial Bold", 14)).pack(pady=5)
    booking_date_entry = ctk.CTkEntry(scroll_frame)
    booking_date_entry.insert(0, today_str)
    booking_date_entry.configure(state="disabled")
    booking_date_entry.pack(pady=5)

    labels = [
        ("Total Hours", "total_hours"),
        ("Match Title", "match_title"),
        ("Match Date (YYYY-MM-DD)", "match_date"),
        ("Start Time (HH:MM)", "start_time"),
        ("Team A", "team_a"),
        ("Team B", "team_b")
    ]

    for label, key in labels:
        ctk.CTkLabel(scroll_frame, text=label, font=("Arial Bold", 14)).pack(pady=5)
        entry = ctk.CTkEntry(scroll_frame)
        entry.pack(pady=5)
        entries[key] = entry

    ctk.CTkLabel(scroll_frame, text="End Time", font=("Arial Bold", 14)).pack(pady=5)
    end_time_entry = ctk.CTkEntry(scroll_frame)
    end_time_entry.configure(state="disabled")
    end_time_entry.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Total Cost", font=("Arial Bold", 14)).pack(pady=5)
    total_cost_entry = ctk.CTkEntry(scroll_frame)
    total_cost_entry.configure(state="disabled")
    total_cost_entry.pack(pady=5)

    def update_details():
        try:
            hrs = int(entries['total_hours'].get())
            total_cost = hrs * rate
            total_cost_entry.configure(state="normal")
            total_cost_entry.delete(0, 'end')
            total_cost_entry.insert(0, f"Rs {total_cost:.2f}")
            total_cost_entry.configure(state="disabled")

            m_date = datetime.strptime(entries['match_date'].get(), '%Y-%m-%d').date()
            s_time = datetime.strptime(entries['start_time'].get(), '%H:%M').time()
            e_time = (datetime.combine(m_date, s_time) + timedelta(hours=hrs)).time()
            end_time_entry.configure(state="normal")
            end_time_entry.delete(0, 'end')
            end_time_entry.insert(0, e_time.strftime('%H:%M'))
            end_time_entry.configure(state="disabled")
        except:
            end_time_entry.configure(state="normal")
            end_time_entry.delete(0, 'end')
            end_time_entry.configure(state="disabled")
            total_cost_entry.configure(state="normal")
            total_cost_entry.delete(0, 'end')
            total_cost_entry.configure(state="disabled")

    entries['total_hours'].bind("<KeyRelease>", lambda e: update_details())
    entries['match_date'].bind("<KeyRelease>", lambda e: update_details())
    entries['start_time'].bind("<KeyRelease>", lambda e: update_details())

    def confirm_booking():
        required_fields = {
            'total_hours': "Total Hours",
            'match_title': "Match Title",
            'match_date': "Match Date",
            'start_time': "Start Time",
            'team_a': "Team A",
            'team_b': "Team B"
        }
        
        missing_fields = []
        for field_key, field_name in required_fields.items():
            if not entries[field_key].get().strip():
                missing_fields.append(field_name)
        
        if missing_fields:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields:\n\n• " + "\n• ".join(missing_fields)
            )
            return

        try:
            b_date = today
            hrs = int(entries['total_hours'].get())
            m_title = entries['match_title'].get()
            m_date = datetime.strptime(entries['match_date'].get(), '%Y-%m-%d').date()
            s_time = datetime.strptime(entries['start_time'].get(), '%H:%M').time()
            t_a = entries['team_a'].get()
            t_b = entries['team_b'].get()

            # Validation 1: Total hours <= 10
            if hrs > 10:
                messagebox.showerror("Invalid Input", "Total hours cannot be more than 10 hours")
                return

            # Validation 2: Match title in English only
            if not is_english(m_title):
                messagebox.showerror("Invalid Input", "Match title must contain only English characters")
                return

            # Validation 3: Match date not before current date
            if m_date < today:
                messagebox.showerror("Invalid Date", "Match date cannot be before today's date")
                return

            # Validation 4: Team names in English only
            if not is_english(t_a) or not is_english(t_b):
                messagebox.showerror("Invalid Input", "Team names must contain only English characters")
                return
            
            # Check if ground is already booked for selected match date
            if not is_ground_available(ground_id, m_date):
                messagebox.showerror("Already Booked", 
                                   f"'{name}' is already booked for {m_date.strftime('%Y-%m-%d')}!\n"
                                   "Please choose a different date or ground.")
                return

            e_time = (datetime.combine(m_date, s_time) + timedelta(hours=hrs)).time()

            global booking_data
            booking_data = {
                'ground_id': ground_id,
                'ground_name': name,
                'booking_date': b_date,
                'total_hours': hrs,
                'hourly_rate': rate,
                'match_title': m_title,
                'match_date': m_date,
                'start_time': s_time,
                'end_time': e_time,
                'team_a': t_a,
                'team_b': t_b
            }

            win.destroy()
            open_payment_window(userID)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def back_to_dashboard():
        try:
            win.destroy()
            app.deiconify()
        except:
            app.destroy()
            organizer_dashboard_window(userID)

    ctk.CTkButton(scroll_frame, 
                 text="← Back to Dashboard",
                 fg_color="transparent",
                 hover_color="#2A2A2A",
                 command=back_to_dashboard).pack(pady=10)

    ctk.CTkButton(scroll_frame, text="Confirm Booking", command=confirm_booking).pack(pady=20)

def organizer_dashboard_window(userID):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Organizer Dashboard")
    app.geometry("1100x600")
    app.configure(fg_color="#0D1B2A")

    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
    app.configure(fg_color="#0D1B2A")

    heading_frame = ctk.CTkFrame(app, fg_color="transparent")
    heading_frame.pack(pady=20)
    
    ctk.CTkLabel(heading_frame, 
                text="Available Grounds", 
                font=("Arial Bold", 28), 
                text_color="#FFD700").pack()

    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    scroll_frame = ctk.CTkScrollableFrame(main_frame)
    scroll_frame.pack(fill="both", expand=True)

    for i in range(5):
        scroll_frame.grid_columnconfigure(i, weight=1)

    headers = ["Name", "Capacity", "Hourly Rate", "Location", "Action"]
    for col, header in enumerate(headers):
        ctk.CTkLabel(scroll_frame, 
                    text=header, 
                    font=("Arial Bold", 16), 
                    text_color="#FFD700").grid(row=0, column=col, padx=10, pady=10, sticky="ew")

    today = datetime.today().date()
    all_grounds = get_all_grounds()

    for row, ground in enumerate(all_grounds, start=1):
        ground_id, name, location, capacity, rate = ground
        
        ctk.CTkLabel(scroll_frame, 
                    text=name, 
                    font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(scroll_frame, 
                    text=str(capacity), 
                    font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll_frame, 
                    text=f"Rs {rate}/hr", 
                    font=("Arial", 14)).grid(row=row, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(scroll_frame, 
                    text=location, 
                    font=("Arial", 14)).grid(row=row, column=3, padx=10, pady=5)
        
        btn = ctk.CTkButton(scroll_frame, 
                           text="Book", 
                           command=lambda g=ground: open_booking_window(g, app,userID))
        btn.grid(row=row, column=4, padx=10, pady=5)

    app.mainloop()

