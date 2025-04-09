
import streamlit as st
from fpdf import FPDF
from datetime import date

# Constants
HOTEL_NAME = "Hotel Rameshwar Inn"
ADDRESS = "2/2, Rambagh, Prayagraj"
PHONE = "751-008-3444"

# Streamlit UI
st.set_page_config(page_title="Hotel Bill Generator", layout="centered")
st.title("🧾 Hotel Bill Generator")
st.markdown("Generate hotel bills in the same layout as your printed receipts.")

# Inputs
name = st.text_input("Guest Name")
room_no = st.text_input("Room Number")
amount = st.text_input("Amount (Rs)", value="1000")

# Dates
invoice_date = st.date_input("Invoice Date", value=date.today())
check_in_date = st.date_input("Check-In Date")
check_in_time = st.time_input("Check-In Time")
check_out_date = st.date_input("Check-Out Date")
check_out_time = st.time_input("Check-Out Time")

# Generate PDF
if st.button("Generate Bill"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Hotel info
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, HOTEL_NAME, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, ADDRESS + " | " + PHONE, ln=True, align='C')
    pdf.ln(10)

    # Invoice info
    pdf.cell(100, 10, f"Invoice Date: {invoice_date.strftime('%d %B, %Y')}", ln=True)
    pdf.cell(100, 10, f"Room No.: {room_no}    Name: {name}", ln=True)
    pdf.ln(10)

    # Check-in/out
    pdf.cell(100, 10, f"Check-In: {check_in_date.strftime('%d %B, %Y')} @ {check_in_time.strftime('%I:%M %p')}", ln=True)
    pdf.cell(100, 10, f"Check-Out: {check_out_date.strftime('%d %B, %Y')} @ {check_out_time.strftime('%I:%M %p')}", ln=True)
    pdf.ln(10)

    # Amount
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(100, 10, f"Total Amount: Rs. {amount} /-", ln=True)
    pdf.ln(20)

    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, "Thank You! Visit again.", ln=True, align='C')

    # Save PDF
    file_path = f"Hotel_Bill_{name.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    with open(file_path, "rb") as f:
        st.download_button(label="📥 Download Bill PDF", data=f, file_name=file_path, mime="application/pdf")
