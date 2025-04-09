import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# Constants
HOTEL_NAME = "Hotel Rameshwar Inn"
TEMPLATE_IMAGE = "template_bg.png"

# Time options for dropdown (AM/PM format)
TIME_OPTIONS = [f"{h} {'AM' if h < 12 else 'PM'}" for h in range(1, 13)] + [f"{h%12 if h%12 != 0 else 12}:30 {'AM' if h < 12 else 'PM'}" for h in range(1, 13)]

# Input fields
st.title("Hotel Bill Generator")

customer_name = st.text_input("Customer Name")
check_in = st.date_input("Check-in Date")
check_out = st.date_input("Check-out Date")
check_in_time = st.selectbox("Check-in Time", TIME_OPTIONS)
check_out_time = st.selectbox("Check-out Time", TIME_OPTIONS)
room_number = st.text_input("Room Number")
amount = st.text_input("Amount (in Rs.)")

if st.button("Generate PDF"):
    pdf = FPDF()
    pdf.add_page()

    # Set background image
    if os.path.exists(TEMPLATE_IMAGE):
        pdf.image(TEMPLATE_IMAGE, x=0, y=0, w=210, h=297)
    else:
        st.error("Template image not found!")

    pdf.set_font("Arial", size=12)

    # Overlay user data at specific coordinates (adjust to your template)
    pdf.set_xy(40, 70)
    pdf.cell(0, 10, f"Customer: {customer_name}", ln=True)

    pdf.set_xy(40, 80)
    pdf.cell(0, 10, f"Room No: {room_number}", ln=True)

    pdf.set_xy(40, 90)
    pdf.cell(0, 10, f"Check-in: {check_in.strftime('%d-%m-%Y')} at {check_in_time}", ln=True)

    pdf.set_xy(40, 100)
    pdf.cell(0, 10, f"Check-out: {check_out.strftime('%d-%m-%Y')} at {check_out_time}", ln=True)

    pdf.set_xy(40, 110)
    pdf.cell(0, 10, f"Total Amount: Rs. {amount}", ln=True)

    # Output PDF
    pdf_path = "hotel_bill.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("Download Bill", f, file_name=pdf_path)
