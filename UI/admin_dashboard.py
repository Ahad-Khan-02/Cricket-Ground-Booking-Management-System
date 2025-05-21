import customtkinter as ctk
from DB.connection import get_connection
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AdminApp:
    def __init__(self ,root=None):
        self.root = root if root else ctk.CTk()
        self.root.title("Cricketer - Admin Dashboard")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.sidebar = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=10)

        self.content = ctk.CTkFrame(self.main_frame)
        self.content.pack(side="right", fill="both", expand=True, pady=10)

        self.create_sidebar()
        self.create_welcome_content()

    def create_sidebar(self):
        logo_label = ctk.CTkLabel(self.sidebar, text="CRICKZONE", font=("Bebas Neue", 44, "bold"))
        logo_label.pack(pady=(20, 40))

        buttons = [
            ("Matches", self.show_matches),
            ("Seats",self.show_seats),
            ("Grounds", self.show_grounds),
            ("Add Ground", self.show_add_ground),
            ("Update Ground", self.show_update_ground),
            ("Delete Ground", self.show_delete_ground),
            ("Audiences",self.show_users),
            ("Admins",self.show_admins),
            ("Organizers", self.show_organizers),
            ("Bookings", self.show_bookings),
            ("Payments", self.show_payments)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command,
                                fg_color="transparent", border_width=1, border_color="#1f6aa5")
            btn.pack(pady=5, padx=10, fill="x")

        logout_btn = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout,hover_color="#c9302c")
        logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")

    def create_welcome_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        welcome_label = ctk.CTkLabel(self.content, text="Admin Dashboard",
                                     font=("Arial", 24, "bold"))
        welcome_label.pack(pady=50)

        desc_label = ctk.CTkLabel(self.content,
                                  text="Manage matches, grounds, bookings and payments from this dashboard",
                                  font=("Arial", 14))
        desc_label.pack(pady=10)

    def show_matches(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Matches",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID","Title", "Date", "Time", "Ground", "Location"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Ground", text="Ground")
        tree.heading("Location", text="Location")

        tree.column("ID", width=100)
        tree.column("Title", width=200)
        tree.column("Date", width=100)
        tree.column("Time", width=100)
        tree.column("Ground", width=150)
        tree.column("Location", width=150)

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT m.MATCHID, m.MATCHTITLE, m.MATCHDATE, m.STARTTIME, m.GROUNDID, g.LOCATION
                                FROM CRICKETMATCHES m, GROUND g
                               WHERE m.GROUNDID = g.GROUNDID""")
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", "end", values=row)

                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch matches: {str(e)}")

    def show_seats(self):
        """Display seat information for a specific match"""
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="View Seats by Match",
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        input_frame = ctk.CTkFrame(self.content)
        input_frame.pack(pady=10)

        match_id_label = ctk.CTkLabel(input_frame, text="Enter Match ID:")
        match_id_label.pack(side="left", padx=5)

        self.seats_match_id_entry = ctk.CTkEntry(input_frame)
        self.seats_match_id_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(input_frame, text="Search", command=self.display_seats)
        search_btn.pack(side="left", padx=5)

        self.seats_table_frame = ctk.CTkFrame(self.content)
        self.seats_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def display_seats(self):
        """Display the seats for the entered match ID"""
        match_id = self.seats_match_id_entry.get()

        if not match_id:
            messagebox.showerror("Error", "Please enter a Match ID")
            return

        for widget in self.seats_table_frame.winfo_children():
            widget.destroy()

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT 1 FROM CricketMatches WHERE MatchID = :1", [match_id])
                if not cursor.fetchone():
                    messagebox.showerror("Error", "No match found with this ID")
                    return
                
                cursor.execute("""
                SELECT s.SEATID, s.MATCHID, s.AUDIENCEID, s.STATUS
                FROM SEATS s
                WHERE s.MATCHID = :1
                """, [match_id])
                
                rows = cursor.fetchall()
                
                if not rows:
                    messagebox.showinfo("Info", "No seats found for this match")
                    return

                tree = ttk.Treeview(self.seats_table_frame, 
                                   columns=("SEATID", "MATCHID", "AUDIENCE", "STATUS"), 
                                   show="headings")

                tree.heading("SEATID", text="Seat ID")
                tree.heading("MATCHID", text="Match ID")
                tree.heading("AUDIENCE", text="Audience")
                tree.heading("STATUS", text="Status")
               

                tree.column("SEATID", width=80)
                tree.column("MATCHID", width=80)
                tree.column("AUDIENCE", width=150)
                tree.column("STATUS", width=100)


                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch seat information: {str(e)}")

    def show_grounds(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Grounds",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Location", "Capacity", "Hourly Rate"),
                               show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Capacity", text="Capacity")
        tree.heading("Hourly Rate", text="Hourly Rate")

        tree.column("ID", width=50)
        tree.column("Name", width=200)
        tree.column("Location", width=150)
        tree.column("Capacity", width=100)
        tree.column("Hourly Rate", width=100)

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Ground")
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", "end", values=row)

                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch grounds: {str(e)}")

    def show_add_ground(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="Add New Ground",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.content)
        form_frame.pack(pady=20)

        fields = [
            ("Ground Name", "entry"),
            ("Location", "entry"),
            ("Capacity", "entry"),
            ("Hourly Rate", "entry")
        ]

        self.add_ground_entries = {}

        for i, (label, field_type) in enumerate(fields):
            frame = ctk.CTkFrame(form_frame)
            frame.grid(row=i, column=0, pady=5, padx=10, sticky="ew")

            lbl = ctk.CTkLabel(frame, text=label)
            lbl.pack(side="left", padx=5)

            if field_type == "entry":
                entry = ctk.CTkEntry(frame)
                entry.pack(side="right", fill="x", expand=True, padx=5)
                self.add_ground_entries[label.split(" ")[0].lower() + "_" + label.split(" ")[
                    1].lower() if " " in label else label.lower()] = entry

        submit_btn = ctk.CTkButton(self.content, text="Add Ground", command=self.add_ground)
        submit_btn.pack(pady=20)

    def add_ground(self):
        try:
            name = self.add_ground_entries["ground_name"].get().strip()
            location = self.add_ground_entries["location"].get().strip()
            capacity_str = self.add_ground_entries["capacity"].get().strip()
            rate_str = self.add_ground_entries["hourly_rate"].get().strip()

            if not name:
                messagebox.showerror("Validation Error", "Ground Name is required.")
                return
            if not location:
                messagebox.showerror("Validation Error", "Location is required.")
                return
            if not capacity_str:
                messagebox.showerror("Validation Error", "Capacity is required.")
                return
            if not rate_str:
                messagebox.showerror("Validation Error", "Hourly Rate is required.")
                return

            if len(name) < 3 or not all(char.isalpha() or char.isspace() for char in name):
                messagebox.showerror("Validation Error", "Ground Name must be at least 3 characters and contain only letters/spaces.")
                return

            if len(location) < 3:
                messagebox.showerror("Validation Error", "Location must be at least 3 characters.")
                return

            try:
                capacity = int(capacity_str)
                if capacity <= 0 or capacity > 100000:
                    messagebox.showerror("Validation Error", "Capacity must be a positive number under 100,000.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Capacity must be a valid integer.")
                return

            try:
                rate = float(rate_str)
                if rate <= 0 or rate > 10000:
                    messagebox.showerror("Validation Error", "Hourly Rate must be a positive number under 10,000.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Hourly Rate must be a valid number.")
                return

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM Ground
                    WHERE LOWER(GroundName) = LOWER(:1) AND LOWER(Location) = LOWER(:2)
                """, (name, location))
                count = cursor.fetchone()[0]

                if count > 0:
                    messagebox.showerror("Error", "Ground already exists in this location.")
                else:
                    cursor.execute("""
                        INSERT INTO Ground (GroundName, Location, Capacity, HourlyRate)
                        VALUES (:1, :2, :3, :4)
                    """, (name, location, capacity, rate))
                    conn.commit()
                    messagebox.showinfo("Success", "Ground added successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add ground: {str(e)}")


    def show_update_ground(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="Update Ground",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.content)
        form_frame.pack(pady=20)

        ground_id_frame = ctk.CTkFrame(form_frame)
        ground_id_frame.pack(pady=10)

        ground_id_label = ctk.CTkLabel(ground_id_frame, text="Ground ID:")
        ground_id_label.pack(side="left", padx=5)

        self.ground_id_entry = ctk.CTkEntry(ground_id_frame)
        self.ground_id_entry.pack(side="right", padx=5)

        search_btn = ctk.CTkButton(form_frame, text="Search", command=self.load_ground_details)
        search_btn.pack(pady=10)

        self.details_frame = ctk.CTkFrame(self.content)
        self.details_frame.pack(pady=20, fill="x", padx=20)

    def load_ground_details(self):
        ground_id = self.ground_id_entry.get()

        if not ground_id:
            messagebox.showerror("Error", "Please enter a Ground ID")
            return
        
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Ground WHERE GroundID = :1", (ground_id,))
                ground = cursor.fetchone()

                if not ground:
                    messagebox.showerror("Error", "No ground found with the provided ID")
                    return

                for widget in self.details_frame.winfo_children():
                    widget.destroy()

                current_label = ctk.CTkLabel(self.details_frame, text="Current Details:",
                                             font=("Arial", 14, "bold"))
                current_label.pack(pady=5, anchor="w")

                details_text = f"Name: {ground[1]} | Location: {ground[2]} | Capacity: {ground[3]} | Hourly Rate: {ground[4]}"
                details_label = ctk.CTkLabel(self.details_frame, text=details_text)
                details_label.pack(pady=5, anchor="w")

                update_label = ctk.CTkLabel(self.details_frame, text="Update Details:",
                                            font=("Arial", 14, "bold"))
                update_label.pack(pady=(10, 5), anchor="w")

                fields = [
                    ("New Name", "entry", ground[1], "name"),
                    ("New Location", "entry", ground[2], "location"),
                    ("New Capacity", "entry", ground[3], "capacity"),
                    ("New Hourly Rate", "entry", ground[4], "rate")
                ]

                self.update_ground_entries = {}

                for label, field_type, default_value, key in fields:
                    frame = ctk.CTkFrame(self.details_frame)
                    frame.pack(pady=5, fill="x")

                    lbl = ctk.CTkLabel(frame, text=label)
                    lbl.pack(side="left", padx=5)

                    if field_type == "entry":
                        entry = ctk.CTkEntry(frame)
                        entry.insert(0, str(default_value))
                        entry.pack(side="right", fill="x", expand=True, padx=5)
                        self.update_ground_entries[key] = entry

                update_btn = ctk.CTkButton(self.details_frame, text="Update Ground",
                                           command=lambda: self.update_ground(ground_id))
                update_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ground details: {str(e)}")

    def update_ground(self, ground_id):
        try:
            name = self.update_ground_entries["name"].get().strip()
            location = self.update_ground_entries["location"].get().strip()
            capacity_str = self.update_ground_entries["capacity"].get().strip()
            rate_str = self.update_ground_entries["rate"].get().strip()

            name = name if name else None
            location = location if location else None

            capacity = int(capacity_str) if capacity_str else None
            rate = float(rate_str) if rate_str else None

            if not name:
                messagebox.showerror("Validation Error", "Ground Name is required.")
                return
            if not location:
                messagebox.showerror("Validation Error", "Location is required.")
                return
            if not capacity_str:
                messagebox.showerror("Validation Error", "Capacity is required.")
                return
            if not rate_str:
                messagebox.showerror("Validation Error", "Hourly Rate is required.")
                return

            if len(name) < 3 or not all(char.isalpha() or char.isspace() for char in name):
                messagebox.showerror("Validation Error", "Ground Name must be at least 3 characters and contain only letters/spaces.")
                return

            if len(location) < 3:
                messagebox.showerror("Validation Error", "Location must be at least 3 characters.")
                return

            try:
                capacity = int(capacity_str)
                if capacity <= 0 or capacity > 100000:
                    messagebox.showerror("Validation Error", "Capacity must be a positive number under 100,000.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Capacity must be a valid integer.")
                return

            with get_connection() as conn:
                print("befor query")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Ground
                    SET GroundName = NVL(:1, GroundName),
                        Location = NVL(:2, Location),
                        Capacity = NVL(:3, Capacity),
                        HourlyRate = NVL(:4, HourlyRate)
                    WHERE GroundID = :5
                """, (name, location, capacity, rate, ground_id))

                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Ground ID not found or no changes made.")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Ground updated successfully")
                    self.load_ground_details()

        except ValueError:
            messagebox.showerror("Error", "Invalid input for capacity or hourly rate")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update ground: {str(e)}")

    def show_delete_ground(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="Delete Ground",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.content)
        form_frame.pack(pady=20)

        ground_id_frame = ctk.CTkFrame(form_frame)
        ground_id_frame.pack(pady=10)

        ground_id_label = ctk.CTkLabel(ground_id_frame, text="Ground ID:")
        ground_id_label.pack(side="left", padx=5)

        self.delete_ground_id_entry = ctk.CTkEntry(ground_id_frame)
        self.delete_ground_id_entry.pack(side="right", padx=5)

        delete_btn = ctk.CTkButton(self.content, text="Delete Ground", command=self.delete_ground,
                                   fg_color="#d9534f", hover_color="#c9302c")
        delete_btn.pack(pady=20)

    def delete_ground(self):
        ground_id = self.delete_ground_id_entry.get()
        if not ground_id:
            messagebox.showerror("Error", "Please enter a Ground ID")
            return
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Ground WHERE GroundID = :1", [ground_id])
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "No ground found with the provided ID")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Ground deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete ground: {str(e)}")
    
    def show_admins(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Admins", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")

        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=100)

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" 
                    SELECT UserID, name, Email, phone 
                    FROM Users 
                    WHERE Role = 'Admin' 
                    ORDER BY UserID 
                """)
                rows = cursor.fetchall()
                for row in rows:
                    tree.insert("", "end", values=row)
                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch admins: {str(e)}")

    def show_users(self):
        """Display all users in the system"""
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Users", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Email", "Phone", "Role"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("Role", text="Role")

        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=100)
        tree.column("Role", width=100)

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" 
                    SELECT UserID, name, Email, phone, Role 
                    FROM Users 
                    WHERE Role = 'Audience' 
                    ORDER BY UserID 
                """)
                rows = cursor.fetchall()
                for row in rows:
                    tree.insert("", "end", values=row)
                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch users: {str(e)}")

    def show_bookings(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Bookings",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID", "Match ID", "User ID", "Seats", "Booking Date"),
                               show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Match ID", text="Match ID")
        tree.heading("User ID", text="User ID")
        tree.heading("Seats", text="Seats")
        tree.heading("Booking Date", text="Booking Date")

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Bookings")
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", "end", values=row)

                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch bookings: {str(e)}")

    def show_payments(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Payments",
                                   font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=("ID", "Booking ID", "Amount", "Payment Date", "Status"),
                               show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Booking ID", text="Booking ID")
        tree.heading("Amount", text="Amount")
        tree.heading("Payment Date", text="Payment Date")
        tree.heading("Status", text="Status")

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Payments")
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", "end", values=row)

                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch payments: {str(e)}")

    def show_organizers(self):
        """Display all organizers in the system"""
        for widget in self.content.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.content, text="All Organizers",
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, 
                           columns=("ID", "Name", "Email", "Phone"), 
                           show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")

        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=100)

        tree.pack(fill="both", expand=True)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT UserID, name, Email, phone 
                    FROM Users 
                    WHERE Role = 'Organizer'
                    ORDER BY UserID
                """)
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", "end", values=row)

                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch organizers: {str(e)}")

    def logout(self):
        self.root.destroy()
        from UI.login import login_window
        login_window()
        

def admin_dashboard_window():
    app = AdminApp()
    app.root.mainloop() 