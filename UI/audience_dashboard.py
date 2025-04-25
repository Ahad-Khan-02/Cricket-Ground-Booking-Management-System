from Models.matches import get_upcoming_matches,get_match_info

matches_data=get_upcoming_matches()

def book_ticket(matchID):
    match_info=get_match_info(matchID)
    print(match_info)
    

