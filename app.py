import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Constants
HOTEL_NAME = "Hotel Rameshwar Inn"
HOTEL_ADDRESS = "2/2, Rambagh, Prayagraj"
TEMPLATE_PATH = "template_bg.png"  # make sure this image is in your repo

# Define custom PDF class
class CustomPDF(FPDF):
    def header(self):
        # Set background image
        self.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)

    def add_bill_details(self, name, bill_date, checkin, checkout, amount):
        self.set_font("Helvetica", size=12)

        # Name
        self.set_xy(30, 60)
        self.cell(0, 10, f"Name: {name}", ln=False)

        # Date
        self.set_xy(30, 70)
        self.cell(0, 10, f"Date: {bill_date}", ln=False)

        # Check-in
        self.set_xy(30, 80)
        self.cell(0, 10, f"Check-in: {checkin}", ln=False)

        # Check-out
        self.set_xy(30, 90)
        self.cell(0, 10, f"Check-out: {checkout}", ln=False)

        # Amount
        self.set_xy(30, 100)
        self.cell(0, 10, f"Amount: ₹{amount}", ln=False)

# Streamlit UI
st.title("Hotel Bill Generator")
st.markdown(f"**{HOTEL_NAME}**")
st.text(HOTEL_ADDRESS)

name = st.text_input("Customer Name")
bill_date = st.date_input("Bill Date")
checkin = st.text_input("Check-in (dd-mm-yyyy hh:mm AM/PM)")
checkout = st.text_input("Check-out (dd-mm-yyyy hh:mm AM/PM)")
amount = st.text_input("Total Amount (in ₹)")

if st.button("Generate PDF"):
    if not os.path.exists(TEMPLATE_PATH):
        st.error("Template background image not found. Please upload it.")
    else:
        pdf = CustomPDF()
        pdf.add_page()
        pdf.add_bill_details(name, bill_date.strftime('%d-%m-%Y'), checkin, checkout, amount)

        output_path = "hotel_bill.pdf"
        pdf.output(output_path)

        with open(output_path, "rb") as f:
            st.download_button("Download Bill", f, file_name="hotel_bill.pdf")
