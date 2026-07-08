import streamlit as st

from auth import login, logout, change_password

from client import (
    add_client,
    view_clients,
    update_client,
    delete_client,
    view_progress
)

from therapist import (
    add_therapist,
    view_therapists,
    update_therapist,
    delete_therapist
)

from appointment import (
    book_appointment,
    view_appointments,
    cancel_appointment,
    complete_appointment,
    delete_appointment
)

from notes import (
    add_note,
    view_notes,
    search_notes,
    update_note,
    delete_note,
    export_notes_csv,
    count_notes
)

from database import close_database


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Rehabilitation Management System",
    page_icon="🏥",
    layout="wide"
)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------------------------------------------
# Login Screen
# ---------------------------------------------------

if st.session_state.user is None:

    st.title("🏥 Rehabilitation Management System")

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login(username, password)

        if user:

            st.session_state.user = user
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid username or password")

    st.stop()


# ---------------------------------------------------
# Logged In User
# ---------------------------------------------------

user = st.session_state.user

st.sidebar.title("Navigation")
st.sidebar.write(f"Logged in as **{user['username']}**")
st.sidebar.write(f"Role: **{user['role']}**")


# ---------------------------------------------------
# ADMIN MENU
# ---------------------------------------------------

if user["role"] == "Admin":

    menu = st.sidebar.radio(

        "Menu",

        (

            "Add Client",
            "View Clients",
            "Update Client",
            "Delete Client",

            "Add Therapist",
            "View Therapists",
            "Update Therapist",
            "Delete Therapist",

            "Book Appointment",
            "View Appointments",
            "Cancel Appointment",
            "Complete Appointment",
            "Delete Appointment",

            "Add Therapy Note",
            "View Therapy Notes",
            "Search Therapy Notes",
            "Update Therapy Note",
            "Delete Therapy Note",
            "Export Therapy Notes",
            "Count Therapy Notes",

            "View Client Progress",

            "Change Password"

        )

    )


# ---------------------------------------------------
# THERAPIST MENU
# ---------------------------------------------------

else:

    menu = st.sidebar.radio(

        "Menu",

        (

            "View Clients",
            "View Therapists",

            "Book Appointment",
            "View Appointments",
            "Cancel Appointment",
            "Complete Appointment",

            "Add Therapy Note",
            "View Therapy Notes",
            "Search Therapy Notes",
            "Export Therapy Notes",
            "Count Therapy Notes",

            "View Client Progress",

            "Change Password"

        )

    )


# ---------------------------------------------------
# CLIENTS
# ---------------------------------------------------

if menu == "Add Client":
    add_client()

elif menu == "View Clients":
    view_clients()

elif menu == "Update Client":
    update_client()

elif menu == "Delete Client":
    delete_client()


# ---------------------------------------------------
# THERAPISTS
# ---------------------------------------------------

elif menu == "Add Therapist":
    add_therapist()

elif menu == "View Therapists":
    view_therapists()

elif menu == "Update Therapist":
    update_therapist()

elif menu == "Delete Therapist":
    delete_therapist()


# ---------------------------------------------------
# APPOINTMENTS
# ---------------------------------------------------

elif menu == "Book Appointment":
    book_appointment()

elif menu == "View Appointments":
    view_appointments()

elif menu == "Cancel Appointment":
    cancel_appointment()

elif menu == "Complete Appointment":
    complete_appointment()

elif menu == "Delete Appointment":
    delete_appointment()


# ---------------------------------------------------
# THERAPY NOTES
# ---------------------------------------------------

elif menu == "Add Therapy Note":
    add_note()

elif menu == "View Therapy Notes":
    view_notes()

elif menu == "Search Therapy Notes":
    search_notes()

elif menu == "Update Therapy Note":
    update_note()

elif menu == "Delete Therapy Note":
    delete_note()

elif menu == "Export Therapy Notes":
    export_notes_csv()

elif menu == "Count Therapy Notes":
    count_notes()


# ---------------------------------------------------
# CLIENT PROGRESS
# ---------------------------------------------------

elif menu == "View Client Progress":
    view_progress()


# ---------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------

elif menu == "Change Password":
    change_password(user)


# ---------------------------------------------------
# Logout
# ---------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("Logout"):

    logout()

    st.rerun()