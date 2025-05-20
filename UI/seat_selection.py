import customtkinter as ctk
from tkinter import messagebox
from DB.connection import get_connection

def seat_selection_window(matchID, audienceID):
    conn = get_connection()
    cursor = conn.cursor()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Select Your Seat")
    app.geometry("800x600")

    frame = ctk.CTkFrame(app, fg_color="#1A1A2E")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkLabel(frame, text="Select Your Seats", font=("Arial", 24, "bold"), text_color="white")
    header.pack(pady=10)

    seat_frame = ctk.CTkFrame(frame)
    seat_frame.pack(pady=20)

    # Fetch available seats for the match
    cursor.execute("""
        SELECT SeatID, SeatNumber FROM Seats
        WHERE MatchID = :1 AND Status = 'Available'
    """, (matchID,))
    available_seats = cursor.fetchall()

    selected_seats = []

    def toggle_seat(seat_id, btn):
        if seat_id in selected_seats:
            selected_seats.remove(seat_id)
            btn.configure(fg_color="#2F4F4F")
        else:
            if len(selected_seats) >= 10:
                messagebox.showwarning("Limit", "You can select up to 10 seats only.")
                return
            selected_seats.append(seat_id)
            btn.configure(fg_color="#00A8E8")

    # Display seats in grid
    for idx, (seat_id, seat_number) in enumerate(available_seats):
        btn = ctk.CTkButton(
            seat_frame, text=seat_number, width=80, height=40,
            fg_color="#2F4F4F", hover_color="#0077B6",
            command=lambda s=seat_id, b=None: toggle_seat(s, b)
        )
        btn.grid(row=idx // 8, column=idx % 8, padx=5, pady=5)
        btn._command = lambda s=seat_id, b=btn: toggle_seat(s, b)  # Bind button to itself

    def confirm_booking():
        if not selected_seats:
            messagebox.showwarning("No Seats", "Please select at least one seat.")
            return
        try:
            for seat_id in selected_seats:
                cursor.execute("""
                    UPDATE Seats
                    SET AudienceID = :1, Status = 'Booked'
                    WHERE SeatID = :2 AND Status = 'Available'
                """, (audienceID, seat_id))
            conn.commit()
            messagebox.showinfo("Success", f"Successfully booked {len(selected_seats)} seat(s).")
            app.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Booking failed: {e}")

    confirm_btn = ctk.CTkButton(frame, text="Confirm Booking", command=confirm_booking)
    confirm_btn.pack(pady=20)

    app.mainloop()

    cursor.close()
    conn.close()
