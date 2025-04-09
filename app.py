import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

# Path to your background image template
TEMPLATE_PATH = "image.png"

# Convert selected time to datetime
def format_datetime(date, time, am_pm):
    hour, minute = map(int, time.split(':'))
    if am_pm == 'PM' and hour != 12:
        hour += 12
    elif am_pm == 'AM' and hour == 12:
        hour = 0
    return datetime.datetime.combine(date, datetime.time(hour, minute))

# Dropdown for time selection
def get_time_options():
    return [f"{h:02d}:{m:02d}" for h in range(1, 13) for m in (0, 15, 30, 45)]

# Streamlit UI
st.title("Hotel Rameshwar Inn Bill Generator")

name = st.text_input("Customer Name")
room_no = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")

checkin_date = st.date_input("Check-in Date")
checkin_time = st.selectbox("Check-in Time", get_time_options(), index=8)
checkin_ampm = st.selectbox("Check-in AM/PM", ["AM", "PM"], key="in")

checkout_date = st.date_input("Check-out Date")
checkout_time = st.selectbox("Check-out Time", get_time_options(), index=8)
checkout_ampm = st.selectbox("Check-out AM/PM", ["AM", "PM"], key="out")

generate = st.button("Generate Bill")

import textwrap

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

if generate:
    # Load and prepare image
    image = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Fonts
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_bold = ImageFont.truetype(font_path, 26)
    font_light = ImageFont.truetype(font_path, 22)
    font_mini = ImageFont.truetype(font_path, 20)

    # Insert top right date
    today_str = datetime.date.today().strftime("%d %B, %Y")
    draw.text((950, 447), today_str, fill="blue", font=font_mini)

    # Format check-in and check-out
    ci = format_datetime(checkin_date, checkin_time, checkin_ampm)
    co = format_datetime(checkout_date, checkout_time, checkout_ampm)
    ci_str = ci.strftime("%d %B, %Y\n@ %I:%M %p").replace("AM", "A.M.").replace("PM", "P.M.")
    co_str = co.strftime("%d %B, %Y\n@ %I:%M %p").replace("AM", "A.M.").replace("PM", "P.M.")

    # === Draw Details on Bill Table Row ===
    y_row = 470  # vertical Y position for the row inside the table

    draw_wrapped_text_centered(draw, name, font_bold, x_left=200, max_width=220, y=800, fill="blue") # Name
    draw.text((387, 800), room_no, fill="cornflowerblue", font=font_light)  # Room No.
    draw.text((580, 800), ci_str, fill="cornflowerblue", font=font_mini)  # Check-in
    draw.text((783, 800), co_str, fill="cornflowerblue", font=font_mini)  # Check-out
    draw.text((990, 800), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Amount

    # === Subtotal and Total at Bottom Right ===
    draw.text((990, 1300), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Subtotal
    draw.text((990, 1415), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Total

    # Show generated image
    st.image(image, caption="Generated Bill", use_column_width=True)

    # Download option
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    st.download_button("Download Bill", data=img_bytes.getvalue(), file_name="hotel_bill.png", mime="image/png")
