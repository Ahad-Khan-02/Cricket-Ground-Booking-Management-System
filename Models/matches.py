from DB.connection import get_connection

def get_upcoming_matches():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT M.MatchID,
               M.MatchTitle,
               TO_CHAR(M.MatchDate, 'DD-MON-YYYY'),
               M.StartTime,
               G.GroundName,
               G.Location
        FROM CricketMatches M, Ground G
        WHERE M.MatchDate >= SYSDATE 
          AND M.GroundID = G.GroundID
        ORDER BY M.MatchDate
    """)

    result = cursor.fetchall()  

    cursor.close()
    conn.close()

    return result

def get_match_info(matchID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT M.MatchTitle,
           TO_CHAR(M.MatchDate, 'DD-MON-YYYY'),
           M.StartTime,
           M.EndTime,
           M.TeamA,
           M.TeamB,
           G.GroundName,
           G.Location,
           G.Capacity,
           G.HourlyRate                           
    FROM CricketMatches M, Ground G 
    WHERE M.GroundID = G.GroundID AND M.MatchID = :1
""", (matchID,))


    result = cursor.fetchall()  

    cursor.close()
    conn.close()

    return result
    

