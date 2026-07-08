import re
from datetime import datetime
import streamlit as range_ts # Common alias is 'st', adjusted here for clean rendering

import streamlit as st

# Set up page configuration
st.set_page_config(page_title="User Registration & Appointment Form", page_icon="📝")
st.title("📝 Registration & Appointment Form")
st.write("Please fill out the form below. The system will validate your inputs automatically.")

# ==============================
# VALIDATION FUNCTIONS (Optimized)
# ==============================
def validate_name(name):
    if not name.strip():
        return False, "Name cannot be empty."
    if not all(char.isalpha() or char.isspace() for char in name):
        return False, "Name should contain only letters and spaces."
    return True, ""

def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email address."
    return True, ""

def validate_phone(phone):
    phone = phone.strip()
    if not phone.isdigit():
        return False, "Phone number must contain only digits."
    if len(phone) < 10 or len(phone) > 15:
        return False, "Phone number must contain 10 to 15 digits."
    return True, ""

# ==============================
# STREAMLIT FORM UI
# ==============================
with st.form("user_form", clear_on_submit=False):
    st.subheader("Personal Information")
    
    # Text input for Name
    name = st.text_input("Full Name", placeholder="John Doe")
    
    # Number input automatically restricts values between 1 and 120
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    
    # Selectbox restricts choices to valid genders
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    # Text inputs for Email and Phone
    email = st.text_input("Email Address", placeholder="johndoe@example.com")
    phone = st.text_input("Phone Number", placeholder="1234567890")
    
    st.divider()
    st.subheader("Appointment Details")
    
    # Date input handles formatting and prevents invalid dates natively
    appointment_date = st.date_input("Appointment Date", value=datetime.today())
    
    # Number inputs ensure non-negative whole numbers
    total_sessions = st.number_input("Total Sessions", min_value=0, value=1, step=1)
    completed_sessions = st.number_input("Completed Sessions", min_value=0, value=0, step=1)
    
    # Selectbox restricts status options
    status = st.selectbox("Appointment Status", ["Booked", "Completed", "Cancelled"])
    
    # Form Submit Button
    submitted = st.form_submit_button("Submit Form")

# ==============================
# FORM SUBMISSION & VALIDATION
# ==============================
if submitted:
    is_valid = True
    errors = []

    # Run custom validations for text inputs
    name_ok, name_msg = validate_name(name)
    if not name_ok:
        errors.append(name_msg)
        is_valid = False

    email_ok, email_msg = validate_email(email)
    if not email_ok:
        errors.append(email_msg)
        is_valid = False

    phone_ok, phone_msg = validate_phone(phone)
    if not phone_ok:
        errors.append(phone_msg)
        is_valid = False
        
    # Cross-field logic validation
    if completed_sessions > total_sessions:
        errors.append("Completed sessions cannot be greater than total sessions.")
        is_valid = False

    # Display Results
    if is_valid:
        st.success("🎉 Form submitted successfully! All data is valid.")
        
        # Display submitted data summary
        st.write("### Submitted Summary:")
        st.json({
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Email": email,
            "Phone": phone,
            "Date": str(appointment_date),
            "Total Sessions": total_sessions,
            "Completed Sessions": completed_sessions,
            "Status": status
        })
    else:
        st.error("⚠️ Please fix the following errors before submitting:")
        for error in errors:
            st.write(f"- {error}")