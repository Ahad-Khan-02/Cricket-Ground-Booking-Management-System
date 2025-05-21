from DB.connection import get_connection
import datetime


def get_all_grounds():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT GroundID, GroundName, Location, Capacity, HourlyRate FROM Ground")
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching grounds: {e}")
        

def is_ground_available(ground_id, match_date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM CricketMatches 
            WHERE GroundID = :1 AND MatchDate = TO_DATE(:2, 'YYYY-MM-DD')
        """, (ground_id, match_date.strftime('%Y-%m-%d')))
        conflict = cursor.fetchone()
        conn.close()
        return conflict is None
    except Exception as e:
        print(f"Check availability error: {e}")
        return False

def insert_organizer_booking_and_payment(organizer_id, ground_id, booking_date, total_hours, match_title,
                                         match_date, start_time, team_a, team_b, hourly_rate,):
    conn = get_connection()
    cursor = conn.cursor()

    try:

        start_dt = datetime.datetime.combine(match_date, start_time)
        end_dt = start_dt + datetime.timedelta(hours=total_hours)
        end_time = end_dt.time()


        match_id_var = cursor.var(int)
        cursor.execute("""
            INSERT INTO CricketMatches (MatchTitle, OrganizerID, GroundID, MatchDate, StartTime, EndTime, TeamA, TeamB)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8)
            RETURNING MatchID INTO :9
        """, (
            match_title, organizer_id, ground_id, match_date.strftime('%Y-%m-%d'),
            start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), team_a, team_b, match_id_var
        ))
        conn.commit()

        match_id = get_match_id(match_title,match_date)

        total_amount = total_hours * hourly_rate


        cursor.execute("""
            INSERT INTO Bookings (OrganizerID, GroundID, BookingDate, TotalHours, TotalCost,MatchID)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)
        """, (organizer_id, ground_id, booking_date.strftime('%Y-%m-%d'), total_hours, total_amount,match_id))

        conn.commit()
        booking_id = get_booking_id(organizer_id,ground_id)

        cursor.execute("""
            INSERT INTO Payments (UserID, PaymentType, RelatedID, Amount, PaymentDate, Status)
            VALUES (:1, 'Organizer', :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), 'Paid')
        """, (
            organizer_id, booking_id, total_amount, datetime.date.today().strftime('%Y-%m-%d')
        ))

        conn.commit()
        return True, f"Booking and payment successful. MatchID: {match_id}"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()


def get_organizer_id(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT UserID FROM Users
            WHERE Email = :1 AND Role = 'Organizer'
        """, (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting organizer ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_ground_id(ground_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT GroundID FROM Ground
            WHERE GroundName = :1
        """, (ground_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting ground ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_booking_id(organizer_id, ground_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT BookingID FROM Bookings
            WHERE OrganizerID = :1 AND GroundID = :2
        """, (organizer_id, ground_id))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting booking ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_match_id(match_title, match_date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MatchID FROM CricketMatches
            WHERE MatchTitle = :1 AND MatchDate = TO_DATE(:2, 'YYYY-MM-DD')
        """, (match_title, match_date.strftime('%Y-%m-%d')))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting match ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
