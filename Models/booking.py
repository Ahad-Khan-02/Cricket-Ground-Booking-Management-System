from DB.connection import get_connection
from Models.seats import book_seat
import datetime


def insert_audience_booking_and_payment(user_id, match_id,num_tickets,total_amount,seat_category):
    conn = get_connection()
    cursor = conn.cursor()

    try:

        audience_booking_id_var = cursor.var(int)
        cursor.execute("""
            INSERT INTO AudienceBookings (AudienceID, MatchID, NumOfTickets, BookingDate, TotalAmount)
            VALUES (:1, :2, :3, :4, :5)
            RETURNING AudienceBookingID INTO :6
        """, (user_id, match_id, num_tickets, datetime.date.today(), total_amount, audience_booking_id_var))

        audience_booking_id = audience_booking_id_var.getvalue()[0]


        cursor.execute("""
            INSERT INTO Payments (UserID, PaymentType, RelatedID, Amount, PaymentDate, Status)
            VALUES (:1, 'Audience', :2, :3, :4, 'Paid')
        """, (user_id, audience_booking_id, total_amount, datetime.date.today()))
        
 
        book_seat(seat_category,user_id,num_tickets,match_id)


        conn.commit()
        return True, 'Booking Successfully done' 

    except Exception as e:
        conn.rollback()
        return False, str(e)  

    finally:
        cursor.close()
        conn.close()
