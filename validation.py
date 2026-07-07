import re
from datetime import datetime


# ==============================
# NAME VALIDATION
# ==============================

def validate_name(name):
    """Name cannot be empty and must contain only letters and spaces."""
    if not name.strip():
        return False, "Name cannot be empty."

    if not all(char.isalpha() or char.isspace() for char in name):
        return False, "Name should contain only letters and spaces."

    return True, ""


# ==============================
# AGE VALIDATION
# ==============================

def validate_age(age):
    """Age must be between 1 and 120."""
    try:
        age = int(age)

        if age < 1 or age > 120:
            return False, "Age must be between 1 and 120."

        return True, ""

    except ValueError:
        return False, "Age must be a number."


# ==============================
# GENDER VALIDATION
# ==============================

def validate_gender(gender):
    """Only Male, Female, or Other are allowed."""
    gender = gender.strip().capitalize()

    if gender not in ["Male", "Female", "Other"]:
        return False, "Gender must be Male, Female, or Other."

    return True, ""


# ==============================
# EMAIL VALIDATION
# ==============================

def validate_email(email):
    """Validate email format."""
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not re.match(pattern, email):
        return False, "Invalid email address."

    return True, ""


# ==============================
# PHONE VALIDATION
# ==============================

def validate_phone(phone):
    """Phone number must contain 10-15 digits."""
    phone = phone.strip()

    if not phone.isdigit():
        return False, "Phone number must contain only digits."

    if len(phone) < 10 or len(phone) > 15:
        return False, "Phone number must contain 10 to 15 digits."

    return True, ""


# ==============================
# DATE VALIDATION
# ==============================

def validate_date(date):
    """Date must be in YYYY-MM-DD format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."


# ==============================
# POSITIVE INTEGER VALIDATION
# ==============================

def validate_sessions(value):
    """Validate completed and total sessions."""
    try:
        value = int(value)

        if value < 0:
            return False, "Value cannot be negative."

        return True, ""

    except ValueError:
        return False, "Value must be a whole number."


# ==============================
# APPOINTMENT STATUS VALIDATION
# ==============================

def validate_status(status):
    """Validate appointment status."""
    allowed = ["Booked", "Completed", "Cancelled"]

    if status.capitalize() not in allowed:
        return False, "Status must be Booked, Completed, or Cancelled."

    return True, ""