CREATE TABLE Seats (
    SeatID NUMBER PRIMARY KEY,
    MatchID NUMBER REFERENCES Matches(MatchID),
    SeatNumber VARCHAR2(10),
    AudienceID NUMBER REFERENCES Users(UserID), -- NULL if unbooked
    Status VARCHAR2(20) CHECK (Status IN ('Available', 'Booked'))
);

CREATE SEQUENCE seq_seat_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_seat_id
BEFORE INSERT ON Seats
FOR EACH ROW
BEGIN
    SELECT seq_seat_id.NEXTVAL INTO :NEW.SeatID FROM dual;
END;
