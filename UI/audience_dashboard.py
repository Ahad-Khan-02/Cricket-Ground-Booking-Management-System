import customtkinter as ctk

def audience_dashboard_window(audienceID):

    from Models.matches import get_upcoming_matches,get_match_info
    from UI.login import login_window
    from UI.heading import heading
    from UI.payment import booking_window   

    matches=get_upcoming_matches()
    
    def book_ticket(matchID):
        match_info=get_match_info(matchID)
        app.destroy()
        booking_window(match_info,matchID,audienceID)


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk(fg_color="#0D1B2A")
    app.title("Audience Dashboard - Upcoming Matches")
    app.attributes("-fullscreen", True)
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))

    heading(app, 'UPCOMMING MATCHES')

    main_frame = ctk.CTkScrollableFrame(app, width=950, fg_color="#000000")
    main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
    main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
    main_frame.grid_rowconfigure(0, weight=0)  
    main_frame.grid_rowconfigure(1, weight=1) 

    back_button = ctk.CTkButton(app, text="← Back", width=80, command= lambda: (app.destroy(),login_window()))
    back_button.place(x=40, y=40)  

    if not matches:
        no_match_label = ctk.CTkLabel(
            main_frame,
            text="No upcoming matches available.",
            font=("Arial", 16),
            text_color="red"
        )
        no_match_label.grid(row=1, column=0, columnspan=4, pady=20)
        return

    header_labels = ["Date", "Match", "Venue"]
    header_font = ("Montserrat", 18)
    header_fg_color = "#FFD700"  

    for i, header in enumerate(header_labels):
        label = ctk.CTkLabel(
            main_frame, 
            text=header, 
            font=header_font, 
            text_color=header_fg_color, 
            corner_radius=5,
            width=200,
            height=40,
            anchor="center"
        )
        label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

    for idx, match in enumerate(matches, start=1):
        ctk.CTkLabel(main_frame, text=match[2], font=("Arial", 16)).grid(row=idx, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(main_frame, text=match[1], font=("Arial", 14)).grid(row=idx, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(main_frame, text=f"{match[4]},{match[5]}", font=("Arial", 14)).grid(row=idx, column=2, padx=20, pady=10, sticky="w")
        button = ctk.CTkButton(
            main_frame,
            text="Book Ticket",
            command=lambda matchID=match[0]: book_ticket(matchID)
        )
        button.grid(row=idx, column=3, padx=20, pady=10)

    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)

    app.mainloop()
    


