import streamlit as st
from fpdf import FPDF
from datetime import date, time
import os

# Constants
HOTEL_NAME = "Hotel Rameshwar Inn"
HOTEL_ADDRESS = "2/2, Rambagh, Prayagraj"
TEMPLATE_PATH = "template_bg.png"  # Make sure this image is uploaded

# Custom PDF with background
class CustomPDF(FPDF):
    def header(self):
        self.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)

    def add_bill_details(self, name, bill_date, checkin, checkout, amount):
        self.set_font("Helvetica", size=12)

        self.set_xy(30, 60)
        self.cell(0, 10, f"Name: {name}", ln=False)

        self.set_xy(30, 70)
        self.cell(0, 10, f"Date: {bill_date}", ln=False)

        self.set_xy(30, 80)
        self.cell(0, 10, f"Check-in: {checkin}", ln=False)

        self.set_xy(30, 90)
        self.cell(0, 10, f"Check-out: {checkout}", ln=False)

        self.set_xy(30, 100)
        self.cell(0, 10, f"Amount: ₹{amount}", ln=False)

# Streamlit app
st.title("🧾 Hotel Bill Generator")
st.markdown(f"**{HOTEL_NAME}**")
st.text(HOTEL_ADDRESS)

# Inputs
name = st.text_input("Customer Name")
bill_date = st.date_input("Invoice Date", value=date.today())

checkin_date = st.date_input("Check-in Date", key="checkin_date")
checkin_time = st.time_input("Check-in Time", key="checkin_time")

checkout_date = st.date_input("Check-out Date", key="checkout_date")
checkout_time = st.time_input("Check-out Time", key="checkout_time")

amount = st.text_input("Total Amount (in ₹)", value="1000")

if st.button("Generate PDF"):
    if not os.path.exists(TEMPLATE_PATH):
        st.error("Background image not found! Make sure 'template_bg.png' is in the repo.")
    else:
        checkin = f"{checkin_date.strftime('%d-%b-%Y')} @ {checkin_time.strftime('%I:%M %p')}"
        checkout = f"{checkout_date.strftime('%d-%b-%Y')} @ {checkout_time.strftime('%I:%M %p')}"

        pdf = CustomPDF()
        pdf.add_page()
        pdf.add_bill_details(name, bill_date.strftime('%d-%b-%Y'), checkin, checkout, amount)

        file_path = f"Bill_{name.replace(' ', '_')}.pdf"
        pdf.output(file_path)

        with open(file_path, "rb") as f:
            st.download_button("📥 Download Bill", f, file_name=file_path, mime="application/pdf")
