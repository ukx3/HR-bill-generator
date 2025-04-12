import base64
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
import datetime
import io
from PIL import Image, ImageDraw, ImageFont

# === Function: Draw wrapped & centered text for image preview ===
def draw_wrapped_text_centered(draw, text, font, x_left, max_width, y, fill="black", line_spacing=5):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    for i, line in enumerate(lines):
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        start_x = x_left + (max_width - line_width) / 2
        draw.text((start_x, y + i * (font.size + line_spacing)), line, font=font, fill=fill)

# === Function: Draw wrapped & centered text for PDF ===
def draw_centered_text_pdf(c, text, font_name, font_size, x_left, max_width, y_start, line_spacing=2):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        line_width = stringWidth(test_line, font_name, font_size)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    for i, line in enumerate(lines):
        line_width = stringWidth(line, font_name, font_size)
        x = x_left + (max_width - line_width) / 2
        y = y_start - i * (font_size + line_spacing)
        c.setFont(font_name, font_size)
        c.drawString(x, y, line)

# === Streamlit UI ===
st.set_page_config(page_title="Hotel Bill PDF Generator")
st.title("Hotel Rameshwar Inn - Bill Generator")

name = st.text_input("Customer Name")
room_no = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")
invoice_date = st.date_input("Invoice Date", value=datetime.date.today())
checkin_date = st.date_input("Check-in Date")
#Time dropdowns: hour:minute + AM/PM separately
time_options = [f"{h:02d}:{m:02d}" for h in range(1, 13) for m in (0, 15, 30, 45)]
checkin_time_str = st.selectbox("Check-in Time", time_options, index=32)  # default 08:00
checkin_ampm = st.selectbox("Check-in AM/PM", ["AM", "PM"])

checkin_hour, checkin_minute = map(int, checkin_time_str.split(":"))
checkin_hour_24 = checkin_hour % 12 + (12 if checkin_ampm == "PM" else 0)
checkin_time = datetime.time(checkin_hour_24, checkin_minute)

checkout_date = st.date_input("Check-out Date")
# Check-out
checkout_time_str = st.selectbox("Check-out Time", time_options, index=36)  # default 09:00
checkout_ampm = st.selectbox("Check-out AM/PM", ["AM", "PM"])

checkout_hour, checkout_minute = map(int, checkout_time_str.split(":"))
checkout_hour_24 = checkout_hour % 12 + (12 if checkout_ampm == "PM" else 0)
checkout_time = datetime.time(checkout_hour_24, checkout_minute)

template_path = "image.png"  # Ensure this image is in your app folder

if st.button("Generate Bill"):
    # === STEP 1: PIL Image Preview ===
    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_bold = ImageFont.truetype(font_path, 26)
    font_light = ImageFont.truetype(font_path, 22)
    font_mini = ImageFont.truetype(font_path, 18)

    invoice_str = invoice_date.strftime("%d %B, %Y")
    draw.text((530, 620), invoice_str, fill="blue", font=font_mini)
    ci_str = checkin_date.strftime("%d %B, %Y") + f"\n@ {checkin_time.strftime('%I:%M %p')}".replace("AM", "A.M.").replace("PM", "P.M.")
    co_str = checkout_date.strftime("%d %B, %Y") + f"\n@ {checkout_time.strftime('%I:%M %p')}".replace("AM", "A.M.").replace("PM", "P.M.")

    # Draw on image
    draw_wrapped_text_centered(draw, name, font_bold, x_left=145, max_width=225, y=800, fill="blue")
    draw.text((440, 800), room_no, fill="cornflowerblue", font=font_light)
    draw.text((580, 800), ci_str, fill="cornflowerblue", font=font_mini)
    draw.text((783, 800), co_str, fill="cornflowerblue", font=font_mini)
    draw.text((990, 800), f"Rs. {amount} /-", fill="blue", font=font_mini)
    draw.text((990, 1300), f"Rs. {amount} /-", fill="blue", font=font_mini)
    draw.text((990, 1415), f"Rs. {amount} /-", fill="blue", font=font_mini)

    st.image(image, caption="🧾 Bill Preview", use_column_width=True)

    # === STEP 2: Generate PDF ===
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    try:
        bg = ImageReader(template_path)
        c.drawImage(bg, 0, 0, width=width, height=height)
    except:
        st.error("❌ Failed to load background template. Make sure 'image.png' is uploaded.")

    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.setFont("Helvetica", 10)
    c.drawRightString(530, 620, invoice_str)

    draw_centered_text_pdf(c, name, "Helvetica", 10, x_left=70, max_width=110, y_start=480)
    c.drawString(210, 480, room_no)
    # Break check-in and check-out into two lines
    ci_date_str = checkin_date.strftime("%d %B, %Y")
    ci_time_str = f"@ {checkin_time.strftime('%I:%M %p')}".replace("AM", "A.M.").replace("PM", "P.M.")

    co_date_str = checkout_date.strftime("%d %B, %Y")
    co_time_str = f"@ {checkout_time.strftime('%I:%M %p')}".replace("AM", "A.M.").replace("PM", "P.M.")

    # Check-in
    c.drawString(270, 485, ci_date_str)
    c.drawString(270, 470, ci_time_str)

    # Check-out
    c.drawString(370, 485, co_date_str)
    c.drawString(370, 470, co_time_str)

    c.drawString(470, 480, f"Rs. {amount} /-")
    c.drawString(470, 165, f"Rs. {amount} /-")
    c.drawString(470, 220, f"Rs. {amount} /-")

    c.save()
    buffer.seek(0)

    # === STEP 3: Download PDF ===
    st.download_button("📥 Download PDF", data=buffer.getvalue(), file_name="hotel_bill.pdf", mime="application/pdf")
