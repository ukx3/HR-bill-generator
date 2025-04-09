import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

# Load background template
TEMPLATE_PATH = "image.png"  # Make sure this is uploaded in the same directory

# Helper function to convert time
def format_datetime(date, time, am_pm):
    hour, minute = map(int, time.split(':'))
    if am_pm == 'PM' and hour != 12:
        hour += 12
    elif am_pm == 'AM' and hour == 12:
        hour = 0
    return datetime.datetime.combine(date, datetime.time(hour, minute))

# Time dropdown options
def get_time_options():
    return [f"{h:02d}:{m:02d}" for h in range(1, 13) for m in (0, 15, 30, 45)]

st.title("Hotel Rameshwar Inn Bill Generator")

# Input fields
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

if generate:
    # Open template
    image = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Load a basic font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_bold = ImageFont.truetype(font_path, 26)
    font_light = ImageFont.truetype(font_path, 22)
    font_mini = ImageFont.truetype(font_path, 20)

    # Date formatting
    today_str = datetime.date.today().strftime("%B %d, %Y")
    draw.text((550, 260), today_str, fill="blue", font=font_mini)

       # Format check-in/check-out
    ci = format_datetime(checkin_date, checkin_time, checkin_ampm)
    co = format_datetime(checkout_date, checkout_time, checkout_ampm)

    ci_str = ci.strftime("%d %B, %Y\n@ %I:%M %p").replace("AM", "A.M.").replace("PM", "P.M.")
    co_str = co.strftime("%d %B, %Y\n@ %I:%M %p").replace("AM", "A.M.").replace("PM", "P.M.")

    # 🟦 Corrected positions to align with the table
    y_row = 470  # vertical position of the first table row

    draw.text((90, y_row), name, fill="blue", font=font_bold)  # NAME
    draw.text((230, y_row), room_no, fill="cornflowerblue", font=font_light)  # ROOM NO.
    draw.text((340, y_row), ci_str, fill="cornflowerblue", font=font_mini)  # CHECK IN
    draw.text((500, y_row), co_str, fill="cornflowerblue", font=font_mini)  # CHECK OUT
    draw.text((670, y_row), f"Rs. {amount} /-", fill="blue", font=font_mini)  # AMOUNT

    # SUBTOTAL and TOTAL (bottom right)
    draw.text((670, 715), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Subtotal
    draw.text((670, 765), f"Rs. {amount} /-", fill="blue", font=font_mini)  # Total


    # Show and download
    st.image(image, caption="Generated Bill", use_column_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    st.download_button("Download Bill", data=img_bytes.getvalue(), file_name="hotel_bill.png", mime="image/png")
