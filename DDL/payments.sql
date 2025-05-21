CREATE TABLE Payments (
    PaymentID NUMBER PRIMARY KEY,
    UserID NUMBER REFERENCES Users(UserID),
    PaymentType VARCHAR2(20) CHECK (PaymentType IN ('Organizer', 'Audience')),
    RelatedID NUMBER,  
    Amount NUMBER,
    PaymentDate DATE,
    Status VARCHAR2(20) CHECK (Status IN ('Paid', 'Pending', 'Failed'))
);

CREATE SEQUENCE seq_payment_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_payment_id
BEFORE INSERT ON Payments
FOR EACH ROW
BEGIN
    SELECT seq_payment_id.NEXTVAL INTO :NEW.PaymentID FROM dual;
END;
