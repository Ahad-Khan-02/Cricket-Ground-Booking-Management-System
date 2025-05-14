import customtkinter as ctk

def calculate_ticket_price(start_time,end_time,capcaity,hourly_rate):
        start_time=int(start_time[:2])
        end_time=int(end_time[:2])
        ticket_price = ((abs(end_time - start_time) * hourly_rate ) / capcaity ) + 1000
        return ticket_price
    
def payment_window(match_info):
    from UI.audience_dashboard import audience_dashboard_window
    payment_app = ctk.CTk()
    payment_app.attributes("-fullscreen", True)
    payment_app.bind("<Escape>", lambda e: payment_app.attributes("-fullscreen", False))    
    payment_app.title("Payment")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    payment_app.configure(fg_color="#0D1B2A")

    frame = ctk.CTkFrame(payment_app, fg_color="#1A1A2E")
    frame.pack(pady=30, padx=30, fill="both", expand=True)

    back_button = ctk.CTkButton(payment_app, text="← Back", width=80, command= lambda: (payment_app.destroy(),audience_dashboard_window(),))
    back_button.place(x=40, y=40)  

    heading_ = ctk.CTkLabel(frame, text="Payment", font=("Arial", 28, "bold"), text_color="white")
    heading_.pack(pady=20)

    match_label = ctk.CTkLabel(frame, text=f"Match: {match_info[0][0]}", font=("Arial", 18), text_color="white")
    match_label.pack(pady=5)

    date_label = ctk.CTkLabel(frame, text=f"Date: {match_info[0][1]}", font=("Arial", 16), text_color="white")
    date_label.pack(pady=5)

    start_time_label = ctk.CTkLabel(frame, text=f"Start Time: {match_info[0][2]}", font=("Arial", 16), text_color="white")
    start_time_label.pack(pady=5)

    teams_label = ctk.CTkLabel(frame, text=f"{match_info[0][4]} vs {match_info[0][5]}", font=("Arial", 16), text_color="white")
    teams_label.pack(pady=5)

    venue_label = ctk.CTkLabel(frame, text=f"Venue: {match_info[0][6]}", font=("Arial", 16), text_color="white")
    venue_label.pack(pady=5)

    loc_label = ctk.CTkLabel(frame, text=f"Location: {match_info[0][7]}", font=("Arial", 16), text_color="white")
    loc_label.pack(pady=5)

    ticket_price = calculate_ticket_price(match_info[0][2],match_info[0][3],match_info[0][8],match_info[0][9])

    price_label = ctk.CTkLabel(frame, text=f"Ticket Price: {ticket_price}", font=("Arial", 16), text_color="white")
    price_label.pack(pady=5)
        
    ticket_label = ctk.CTkLabel(frame, text="Number of Tickets", font=("Arial", 16), text_color="white")
    ticket_label.pack(pady=(30, 5))

    ticket_entry = ctk.CTkEntry(frame, placeholder_text="Enter quantity")
    ticket_entry.pack(pady=5)

    total_price_label = ctk.CTkLabel(frame, text=f"Total Amount: Rs. 0", font=("Arial", 16), text_color="#00FFAA")
    total_price_label.pack(pady=10)
    
    def calculateTotal(quantity,price):
        try:
            quantity = int(ticket_entry.get())
            total_price_label.configure(text=f"Total Amount: Rs. {quantity * price}")
        except ValueError:
            total_price_label.configure(text="Please enter a valid number.")
        

    cal_total_price_button = ctk.CTkButton(frame, text="Calculate Total",command= lambda: (calculateTotal(int(ticket_entry.get()),ticket_price)))
    cal_total_price_button.pack(pady=5)

    
    method_label = ctk.CTkLabel(frame, text="Payment Method", font=("Arial", 16), text_color="white")
    method_label.pack(pady=(20, 5))

    payment_method = ctk.CTkOptionMenu(frame, values=["Credit Card", "UPI", "Bank Transfer"])
    payment_method.pack(pady=5)

    confirm_btn = ctk.CTkButton(frame, text="Confirm Payment")
    confirm_btn.pack(pady=30)

    payment_app.mainloop()
