CREATE TABLE CricketMatches (
    MatchID NUMBER PRIMARY KEY,
    MatchTitle VARCHAR2(100),
    OrganizerID NUMBER REFERENCES Users(UserID),
    GroundID NUMBER REFERENCES Ground(GroundID),
    MatchDate DATE,
    StartTime VARCHAR2(10),
    EndTime VARCHAR2(10),
    TeamA VARCHAR2(50),
    TeamB VARCHAR2(50)
);

CREATE SEQUENCE seq_cricketmatch_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_match_id
BEFORE INSERT ON Matches
FOR EACH ROW
BEGIN
    SELECT seq_match_id.NEXTVAL INTO :NEW.MatchID FROM dual;
END;
