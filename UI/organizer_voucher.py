import os
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def generate_organizer_voucher(booking_data,ground_info):
    
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = f"Ground_Booking_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(downloads_path, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 70, "🏟️ Ground Booking Confirmation")

    # Separator line
    c.setStrokeColor(colors.grey)
    c.line(40, height - 90, width - 40, height - 90)

    # Booking Details
    c.setFillColor(colors.black)
    y = height - 130
    
    # Ground Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Ground: {booking_data['ground_name']}")
    y -= 25
    c.setFont("Helvetica", 14)
    c.drawString(50, y, f"Booking Date: {booking_data['booking_date'].strftime('%Y-%m-%d')}")
    y -= 20
    c.drawString(50, y, f"Location: {ground_info['location']}")
    y -= 20
    c.drawString(50, y, f"Capacity: {ground_info['capacity']}")
    y -= 20
    c.drawString(50, y, f"Hourly Rate: Rs. {booking_data['hourly_rate']:.2f}")
    y -= 20

    # Match Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Match Details:")
    y -= 25
    c.setFont("Helvetica", 14)
    c.drawString(50, y, f"Title: {booking_data['match_title']}")
    y -= 20
    c.drawString(50, y, f"Date: {booking_data['match_date'].strftime('%Y-%m-%d')}")
    y -= 20
    c.drawString(50, y, f"Time: {booking_data['start_time'].strftime('%H:%M')} to {booking_data['end_time'].strftime('%H:%M')}")
    y -= 20
    c.drawString(50, y, f"Teams: {booking_data['team_a']} vs {booking_data['team_b']}")
    y -= 30

    # Payment Box
    c.setStrokeColor(colors.black)
    c.rect(45, y - 80, width - 90, 100, stroke=1, fill=0)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, y + 10, "Payment Summary")
    c.setFont("Helvetica", 13)
    c.drawString(60, y - 10, f"Total Hours Booked: {booking_data['total_hours']}")
    total_amount = booking_data['total_hours'] * booking_data['hourly_rate']
    c.drawString(60, y - 30, f"Total Amount: Rs. {total_amount:.2f}")

    # Footer Notes
    y -= 100
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(colors.grey)
    c.drawString(50, y, "Note: This voucher serves as your official booking confirmation.")
    y -= 15
    c.drawString(50, y, "Please present this document when accessing the ground facilities.")
 

    c.save()
    return filepath