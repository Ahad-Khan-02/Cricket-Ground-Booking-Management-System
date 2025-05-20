import customtkinter as ctk
from UI.voucher_generator import generate_voucher
from CTkMessagebox import CTkMessagebox  
from tkinter import messagebox


def calculate_ticket_price(start_time,end_time,capcaity,hourly_rate,seat_category=0):
        start_time=int(start_time[:2])
        end_time=int(end_time[:2])
        ticket_price = ((abs(end_time - start_time) * hourly_rate ) / capcaity ) + 1000
        if seat_category == 'First Class':
            ticket_price+=500
        elif seat_category == 'Premium':
            ticket_price+=1000
        return ticket_price

    
def payment_window(match_info,matchID,audienceID):
    from UI.audience_dashboard import audience_dashboard_window
    from Models.booking import insert_audience_booking_and_payment
    from Models.seats import get_available_seats


    payment_app = ctk.CTk()
    payment_app.attributes("-fullscreen", True)
    payment_app.bind("<Escape>", lambda e: payment_app.attributes("-fullscreen", False))    
    payment_app.title("Payment")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    payment_app.configure(fg_color="#0D1B2A")

    def confirm_payment(match_info,quantity,ticket_price):
        try:
            print(seat_category.get()[0])
            quantity = int(quantity)
            if type(quantity)!=type(1):
                messagebox.showerror("Error",'Please Enter a valid quantity')
            elif not 1<=quantity<=10:
                messagebox.showerror("Error","Tickets quantity must be between 1-10")  
            else:
                total_amount = quantity * ticket_price
                seats_available = get_available_seats(matchID,seat_category.get())
                print(seats_available)
                if seats_available < quantity:
                    messagebox.showerror('Error',f"{quantity} {seat_category.get()} seats not available.\n Only {seats_available} {seat_category.get()} seats available")
                else:
                    # Show confirmation box
                    confirm = CTkMessagebox(
                        title="Confirm Payment",
                        message=f"You are about to pay Rs. {total_amount:.2f} for {quantity} ticket(s).\nDo you want to continue?",
                        icon="question",
                        option_1="Yes",
                        option_2="Cancel"
                    )

                    if confirm.get() == "Yes":
                        success,msg=insert_audience_booking_and_payment(audienceID,matchID,quantity,total_amount,seat_category.get())
                        if success:
                            filename = generate_voucher(match_info, quantity, ticket_price, seat_category.get(), audienceID, matchID)
                            if filename:
                                CTkMessagebox(
                                    title="Voucher Generated",
                                    message=f"Voucher saved in Downloads:\n{filename}",
                                    icon="check"
                                )
                                payment_app.destroy()
                        else:
                            print(msg)
                            messagebox.showerror("Error", f"Database Error: {msg}")
        except ValueError:
            messagebox.showerror("Error",'Please Enter a valid quantity')
            return

    def update_price_label(choice):
        updated_price = calculate_ticket_price(
            match_info[0][2],
            match_info[0][3],
            match_info[0][8],
            match_info[0][9],
            choice
        )
        price_label.configure(text=f"Ticket Price: Rs. {updated_price:.2f}")
        # Also update global ticket_price used in confirm & calculateTotal
        nonlocal ticket_price
        ticket_price = updated_price

    frame = ctk.CTkFrame(payment_app, fg_color="#1A1A2E")
    frame.pack(pady=30, padx=30, fill="both", expand=True)

    back_button = ctk.CTkButton(payment_app, text="← Back", width=80, command= lambda: (payment_app.destroy()))
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

    seat_label = ctk.CTkLabel(frame, text="Select Seat Category", font=("Arial", 16), text_color="white")
    seat_label.pack(pady=(20, 5))

    seat_category = ctk.CTkOptionMenu(frame, values=["General", "First Class", "Premium"])
    seat_category.set("General")
    seat_category.configure(command=update_price_label)  
    seat_category.pack(pady=5)

    ticket_price = calculate_ticket_price(match_info[0][2],match_info[0][3],match_info[0][8],match_info[0][9],seat_category.get())

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
            quantity=int(quantity)
            if not 1<=quantity<=10:
                total_price_label.configure(text="Tickets quantity must be between 1-10")
            else:
                total_price_label.configure(text=f"Total Amount: Rs. {(quantity * price):.2f}")   
        except ValueError:
            total_price_label.configure(text="Please enter a valid quantity.")
        

    cal_total_price_button = ctk.CTkButton(frame, text="Calculate Total",command= lambda: (calculateTotal(ticket_entry.get(),ticket_price)))
    cal_total_price_button.pack(pady=5)

    

    confirm_btn = ctk.CTkButton(frame, text="Confirm Payment",command= lambda: (confirm_payment(match_info,ticket_entry.get(),ticket_price)))
    confirm_btn.pack(pady=30)



    payment_app.mainloop()
