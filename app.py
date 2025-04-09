import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue, black, HexColor
import datetime
import io

st.set_page_config(page_title="Hotel Bill PDF Generator")
st.title("Hotel Rameshwar Inn - PDF Bill Generator")

# Inputs
name = st.text_input("Customer Name")
room_no = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")

checkin_date = st.date_input("Check-in Date")
checkin_time = st.time_input("Check-in Time")
checkout_date = st.date_input("Check-out Date")
checkout_time = st.time_input("Check-out Time")

generate = st.button("Generate PDF Bill")

if generate:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Fonts
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor("#1F4E79"))
    c.drawString(50, height - 50, "Hotel Rameshwar Inn")

    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawString(50, height - 80, "Civil Lines, Prayagraj - 211001")
    c.drawString(50, height - 95, "Phone: +91 9336448018")

    # Top right current date
    today_str = datetime.date.today().strftime("%d %B, %Y")
    c.drawRightString(width - 50, height - 50, f"Date: {today_str}")

    # Table headings
    y_start = height - 150
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_start, "Customer Name")
    c.drawString(200, y_start, "Room No.")
    c.drawString(300, y_start, "Check-In")
    c.drawString(430, y_start, "Check-Out")
    c.drawString(550, y_start, "Amount")

    # Draw the values
    y_data = y_start - 25
    c.setFont("Helvetica", 11)

    # Convert datetime to string
    ci_str = checkin_date.strftime("%d %b %Y") + f" @ {checkin_time.strftime('%I:%M %p')}"
    co_str = checkout_date.strftime("%d %b %Y") + f" @ {checkout_time.strftime('%I:%M %p')}"

    c.drawString(50, y_data, name)
    c.drawString(200, y_data, room_no)
    c.drawString(300, y_data, ci_str)
    c.drawString(430, y_data, co_str)
    c.drawString(550, y_data, f"Rs. {amount} /-")

    # Totals section
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 50, 100, f"Subtotal: Rs. {amount} /-")
    c.drawRightString(width - 50, 80, f"Total: Rs. {amount} /-")

    # Save PDF
    c.showPage()
    c.save()
    buffer.seek(0)

    st.success("✅ PDF Generated Successfully!")
    st.download_button("📥 Download PDF", data=buffer.getvalue(), file_name="hotel_bill.pdf", mime="application/pdf")
