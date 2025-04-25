from UI.audience_dashboard import book_ticket
from Models.matches import get_upcoming_matches,get_match_info

matches_data=get_upcoming_matches()
print(matches_data)

book_ticket(matches_data[0][0])