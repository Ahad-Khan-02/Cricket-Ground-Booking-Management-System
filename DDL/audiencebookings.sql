CREATE TABLE AudienceBookings (
    AudienceBookingID NUMBER PRIMARY KEY,
    AudienceID NUMBER REFERENCES Users(UserID),
    MatchID NUMBER REFERENCES Matches(MatchID),
    NumOfTickets NUMBER,
    BookingDate DATE,
    TotalAmount NUMBER
);

CREATE SEQUENCE seq_audience_booking_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_audience_booking_id
BEFORE INSERT ON AudienceBookings
FOR EACH ROW
BEGIN
    SELECT seq_audience_booking_id.NEXTVAL INTO :NEW.AudienceBookingID FROM dual;
END;
