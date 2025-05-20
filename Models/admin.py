from DB.connection import get_connection
from datetime import datetime


def view_all_matches():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT m.MatchTitle,m.MatchDate,m.Start_time,g.GroundName,g.location
                       FROM matches m, ground g
                       WHERE m.Ground_id = g.Ground_id""")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Title = {row[0]} | Date = {row[1]} | Time = {row[2]} | Ground = {row[3]} | Location = {row[4]}")
        cursor.close()


def add_match(title, organizer_id, ground_id, match_date, start_time, end_time, team_a, team_b):
    input_date = datetime.strptime(match_date, "%Y-%m-%d").date()
    if input_date <= datetime.now().date():
        print("Error: Match date must be in the future")
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 1 FROM users
                WHERE userID = :1
                AND Role = Organizer
            """,organizer_id)
        if not cursor.fetchone():
            print("Organizer not found")
            return

        cursor.execute("""
                        SELECT 1 FROM Ground
                        WHERE GroundID = :1
                    """, ground_id)
        if not cursor.fetchone():
            print("ground not found")
            return

        cursor.execute("""
                        INSERT INTO CricketMatches (
                            MatchTitle, 
                            OrganizerID, 
                            GroundID, 
                            MatchDate, 
                            StartTime, 
                            EndTime, 
                            TeamA, 
                            TeamB
                        ) VALUES (
                            :1,
                            :2,
                            :3,
                            TO_DATE(:4, 'YYYY-MM-DD'),
                            :5,
                            :6,
                            :7,
                            :8
                        )
                        """,
                            (title,
                            organizer_id,
                            ground_id,
                            match_date,
                            start_time,
                            end_time,
                            team_a,
                            team_b)
                        )


def delete_match(delete):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM matches
                       WHERE m.match_id = :1""",delete)
        rows = cursor.fetchall()
        cursor.close()


def view_grounds():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ground")
        print("\n-- Grounds --")
        for row in cursor:
            print(f"ID: {row[0]} | Name: {row[1]} | Location: {row[2]}")
        cursor.close()


def add_ground():
    name = input("Enter ground name: ").strip()
    location = input("Enter location: ").strip()
    capacity = int(input("Enter capacity: "))
    rate = float(input("Enter hourly rate: "))

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Ground
            WHERE LOWER(GroundName) = LOWER(:1) AND LOWER(Location) = LOWER(:2)
        """, (name, location))

        count = cursor.fetchone()[0]
        if count > 0:
            print(" Ground already exists in this location. Not adding duplicate.")
        else:
            cursor.execute("""
                INSERT INTO Ground (GroundName, Location, Capacity, HourlyRate)
                VALUES (:1, :2, :3, :4)
            """, (name, location, capacity, rate))
            conn.commit()
            print(" Ground added successfully.")

        cursor.close()


def update_ground():
    ground_id = input("Enter the Ground ID to update: ")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ground WHERE GroundID = :1", (ground_id,))
        ground = cursor.fetchone()

        if not ground:
            print(" No ground found with the provided ID.")
            cursor.close()
            return

        print(
            f"\nCurrent Details:\nName: {ground[1]} | Location: {ground[2]} | Capacity: {ground[3]} | HourlyRate: {ground[4]}")

        name = input("Enter new name (leave blank to keep current): ") or ground[1]
        location = input("Enter new location (leave blank to keep current): ") or ground[2]
        capacity_input = input("Enter new capacity (leave blank to keep current): ")
        rate_input = input("Enter new hourly rate (leave blank to keep current): ")

        capacity = int(capacity_input) if capacity_input else ground[3]
        rate = float(rate_input) if rate_input else ground[4]

        cursor.execute("""
            UPDATE Ground
            SET GroundName = :1,
                Location = :2,
                Capacity = :3,
                HourlyRate = :4
            WHERE GroundID = :5
        """, (name, location, capacity, rate, ground_id))

        conn.commit()
        print(" Ground updated successfully.")
        cursor.close()


def delete_ground():
    ground_id = input("Enter the Ground ID to update: ")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ground WHERE GroundID = :1", (ground_id,))
        ground = cursor.fetchone()

        if not ground:
            print(" No ground found with the provided ID.")
            cursor.close()
            return

        cursor.execute("""
            DELETE FROM Ground
            WHERE GroundID = :1
        """, ground_id)


def view_bookings():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bookings")
        rows = cursor.fetchall()
        print("\n-- All Bookings --")
        for row in rows:
            print(row)
        cursor.close()


def view_payments():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payments")
        rows = cursor.fetchall()
        print("\n-- All Payments --")
        for row in rows:
            print(row)
        cursor.close()
