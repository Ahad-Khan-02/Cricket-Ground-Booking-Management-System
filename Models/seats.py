# Models/seats.py
from DB.connection import get_connection



def populate_seats(match_id, capacity):
    conn = get_connection()
    cursor = conn.cursor()
    general_seats = int(capacity * 0.50)
    first_class_seats = int(capacity * 0.30)
    premium_seats = int(capacity * 0.20)
    try:
        for i in range(1, general_seats+1):
            cursor.execute("""
                INSERT INTO Seats (MatchID, SeatNumber, AudienceID, Status)
                VALUES (:1, :2, NULL, 'Available')
            """, (match_id, f"G-{i}"))
        for i in range(1, first_class_seats+1):
            cursor.execute("""
                INSERT INTO Seats (MatchID, SeatNumber, AudienceID, Status)
                VALUES (:1, :2, NULL, 'Available')
            """, (match_id, f"F-{i}"))
        for i in range(1, premium_seats+1):
            cursor.execute("""
                INSERT INTO Seats (MatchID, SeatNumber, AudienceID, Status)
                VALUES (:1, :2, NULL, 'Available')
            """, (match_id, f"P-{i}"))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_available_seats(match_id, seat_category):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(SeatID)
            FROM Seats
            WHERE MatchID = :1 AND Status = 'Available' AND SeatNumber LIKE :2
        """, (match_id, f"{seat_category[0]}-%"))
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def book_seat(seat_category, audience_id,quantity,matchID):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"""
            SELECT SeatID FROM Seats
            WHERE MatchID = :1 AND Status = 'Available' AND SeatNumber LIKE :2
            AND ROWNUM <= {quantity}
        """
        cursor.execute(query, (matchID, f"{seat_category[0]}-%"))
        
        result=cursor.fetchall()
        seat_ids=[]
        for row in result:
            seat_ids.append(row[0])

        for seat_id in seat_ids:
            cursor.execute("""
                UPDATE Seats
                SET AudienceID = :1, Status = 'Booked'
                WHERE SeatID = :2
            """, (audience_id, seat_id))
        conn.commit()
        return True,'success'
    except Exception as e:
        conn.rollback()
        return False,str(e)
    finally:
        cursor.close()
        conn.close()

