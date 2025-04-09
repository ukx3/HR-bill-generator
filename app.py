import base64
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from reportlab.lib.utils import ImageReader
import datetime
import io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Hotel Bill PDF Generator")
st.title("Hotel Rameshwar Inn - Bill Generator")

# Inputs
name = st.text_input("Customer Name")
room_no = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")

checkin_date = st.date_input("Check-in Date")
checkin_time = st.time_input("Check-in Time")
checkout_date = st.date_input("Check-out Date")
checkout_time = st.time_input("Check-out Time")

template_path = "image.png"  # Stylish template in your app directory

if st.button("Generate Bill"):
    # === STEP 1: PIL Image Preview ===
    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_big = ImageFont.truetype(font_path, 26)
    font_mid = ImageFont.truetype(font_path, 22)
    font_small = ImageFont.truetype(font_path, 18)

    today_str = datetime.date.today().strftime("%d %B, %Y")
    ci_str = checkin_date.strftime("%d %b %Y") + f" @ {checkin_time.strftime('%I:%M %p')}"
    co_str = checkout_date.strftime("%d %b %Y") + f" @ {checkout_time.strftime('%I:%M %p')}"

     # === Draw Details on Bill Table Row ===
    y_row = 470  # vertical Y position for the row inside the table

    draw_wrapped_text_centered(draw, name, font_bold, x_left=145, max_width=225, y=800, fill="blue") # Name
    draw.text((440, 800), room_no, fill="cornflowerblue", font=font_light)  # Room No.
    draw.text((580, 800), ci_str, fill="cornflowerblue", font=font_mini)  # Check-in
    draw.text((783, 800), co_str, fill="cornflowerblue", font=font_mini)  # Check-out
    draw.text((990, 800), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Amount

    # === Subtotal and Total at Bottom Right ===
    draw.text((990, 1300), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Subtotal
    draw.text((990, 1415), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Total

    st.image(image, caption="🧾 Bill Preview", use_column_width=True)

    # === STEP 2: Generate PDF from Template ===
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    try:
        bg = ImageReader(template_path)
        c.drawImage(bg, 0, 0, width=width, height=height)
    except:
        st.error("❌ Failed to load background template. Make sure 'image.png' is uploaded.")

    # Draw same data
    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    c.drawRightString(950, 790, today_str)
    c.drawString(200, 800, name)
    c.drawString(439, 800, room_no)
    c.drawString(580, 800, ci_str)
    c.drawString(783, 800, co_str)
    c.drawString(990, 800, f"Rs. {amount} /-")
    c.drawString(990, 1300, f"Rs. {amount} /-")
    c.drawString(990, 1415, f"Rs. {amount} /-")

    c.save()
    buffer.seek(0)

    # === STEP 3: Show Download Button + Optional Preview ===
    st.download_button("📥 Download PDF", data=buffer.getvalue(), file_name="hotel_bill.pdf", mime="application/pdf")
