import streamlit as st
from fpdf import FPDF
from PIL import Image
import datetime

# Page settings
st.set_page_config(page_title="Hotel Rameshwar Inn - Bill Generator", layout="centered")

# Background template path
TEMPLATE_PATH = "template_bg.png"

# Title
st.title("Hotel Rameshwar Inn 🏨")
st.subheader("Generate Stylish Hotel Bill")

# User input fields
name = st.text_input("Customer Name")
room_number = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")

# Date pickers
checkin_date = st.date_input("Check-in Date", value=datetime.date.today())
checkout_date = st.date_input("Check-out Date", value=datetime.date.today())

# Time dropdowns in 12-hour format
hours = [f"{h}:00" for h in range(1, 13)]
period = ["AM", "PM"]

checkin_hour = st.selectbox("Check-in Time", hours)
checkin_period = st.selectbox("Check-in Period", period)

checkout_hour = st.selectbox("Check-out Time", hours)
checkout_period = st.selectbox("Check-out Period", period)

# Generate PDF
if st.button("Generate PDF"):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Add the background template
    pdf.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)

    # Set font
    pdf.set_font("Arial", size=12)

    # Add content on top of the background at correct positions
    pdf.set_xy(42, 70)
    pdf.cell(0, 10, f"Customer: {name}", ln=False)

    pdf.set_xy(42, 75)
    pdf.cell(0, 10, f"Room No: {room_number}", ln=False)

    pdf.set_xy(42, 80)
    pdf.cell(0, 10, f"Check-in: {checkin_date.strftime('%d-%m-%Y')} at {checkin_hour} {checkin_period}", ln=False)

    pdf.set_xy(42, 85)
    pdf.cell(0, 10, f"Check-out: {checkout_date.strftime('%d-%m-%Y')} at {checkout_hour} {checkout_period}", ln=False)

    pdf.set_xy(42, 95)
    pdf.cell(0, 10, f"Total Amount: Rs. {amount}", ln=False)

    # Save the PDF
    file_path = f"hotel_bill_{name.replace(' ', '_')}.pdf"
    try:
        pdf.output(file_path)
        with open(file_path, "rb") as f:
            st.success("🎉 PDF Generated Successfully!")
            st.download_button("📥 Download PDF", f, file_name=file_path)
    except Exception as e:
        st.error(f"Error: {str(e)}")
