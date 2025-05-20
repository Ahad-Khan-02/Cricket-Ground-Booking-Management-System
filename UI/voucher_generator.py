import os
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def generate_voucher(match_info, quantity, ticket_price, seat_category="General", audience_id=None, match_id=None):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = f"Cricket_Ticket_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(downloads_path, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 70, "Cricket Match Entry Voucher")

    # Draw separator
    c.setStrokeColor(colors.grey)
    c.line(40, height - 90, width - 40, height - 90)

    # Match Info
    y = height - 130
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(50, y, "Match Information")
    c.setFont("Helvetica", 13)
    y -= 20
    c.drawString(50, y, f"Match Title: {match_info[0][0]}")
    y -= 18
    c.drawString(50, y, f"Match ID: {match_id if match_id else 'N/A'}")
    y -= 18
    c.drawString(50, y, f"Date: {match_info[0][1]}")
    y -= 18
    c.drawString(50, y, f"Time: {match_info[0][2]} - {match_info[0][3]}")
    y -= 18
    c.drawString(50, y, f"Teams: {match_info[0][4]} vs {match_info[0][5]}")
    y -= 18
    c.drawString(50, y, f"Venue: {match_info[0][6]}")
    y -= 18
    c.drawString(50, y, f"Location: {match_info[0][7]}")

    # Booking Info
    y -= 35
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Booking Details")
    y -= 20
    c.setFont("Helvetica", 13)
    c.drawString(50, y, f"Audience ID: {audience_id if audience_id else 'N/A'}")
    y -= 18
    c.drawString(50, y, f"Seat Category: {seat_category}")
    y -= 18
    c.drawString(50, y, f"Tickets Booked: {quantity}")
    y -= 18
    c.drawString(50, y, f"Ticket Price (each): Rs. {ticket_price:.2f}")
    total_amount = quantity * ticket_price
    y -= 18
    c.drawString(50, y, f"Total Amount Paid: Rs. {total_amount:.2f}")

    # Voucher Generation Time
    y -= 35
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(colors.darkgrey)
    c.drawString(50, y, f"Voucher Generated On: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    # Footer Notes
    y -= 30
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(50, y, "Note: Please carry this voucher and a valid ID for entry.")
    y -= 14
    c.drawString(50, y, "No refunds or exchanges. Entry closes 30 minutes after match start time.")

    c.save()
    return filepath
