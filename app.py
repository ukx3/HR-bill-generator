import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from reportlab.lib.utils import ImageReader
import datetime
import io
from PIL import Image

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

# Use fixed template
template_path = "image.png"  # Ensure this file is in your app directory

generate = st.button("Generate PDF Bill")

if generate:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw background image
    try:
        bg = ImageReader(template_path)
        c.drawImage(bg, 0, 0, width=width, height=height)
    except:
        st.error("❌ Failed to load background template. Make sure 'image.png' is uploaded.")

    # Fonts and colors
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor("#1F4E79"))
    

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

    c.drawString(50, 800, name)
    c.drawString(440, 500, room_no)
    c.drawString(580, 800, ci_str)
    c.drawString(783, 800, co_str)
    c.drawString(800, 990, f"Rs. {amount} /-")

    # Totals section
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 990, 1300, f"Rs. {amount} /-")
    c.drawRightString(width - 990, 1415, f"Rs. {amount} /-")

    # Save PDF
    c.showPage()
    c.save()
    buffer.seek(0)

    st.success("✅ PDF Generated Successfully!")
    st.download_button("📥 Download PDF", data=buffer.getvalue(), file_name="hotel_bill.pdf", mime="application/pdf")
