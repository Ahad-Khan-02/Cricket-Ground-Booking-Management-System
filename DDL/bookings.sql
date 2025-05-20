CREATE TABLE Bookings (
    BookingID NUMBER PRIMARY KEY,
    OrganizerID NUMBER REFERENCES Users(UserID),
    MatchID NUMBER REFERENCES Matches(MatchID),
    GroundID NUMBER REFERENCES Ground(GroundID),
    BookingDate DATE,
    TotalHours NUMBER,
    TotalCost NUMBER
);

CREATE SEQUENCE seq_booking_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_booking_id
BEFORE INSERT ON Bookings
FOR EACH ROW
BEGIN
    SELECT seq_booking_id.NEXTVAL INTO :NEW.BookingID FROM dual;
END;
