# ==========================================
# REHABILITATION MANAGEMENT SYSTEM - APP.PY
# ==========================================

import streamlit as st
from auth import login, logout, change_password
from client import ( add_client, view_clients, update_client, delete_client, view_progress )
from therapist import ( add_therapist, view_therapists, update_therapist, delete_therapist )
from appointment import ( book_appointment, view_appointments, cancel_appointment, complete_appointment, delete_appointment )
from notes import ( add_note, view_notes, search_notes, update_note, delete_note, export_notes_csv, count_notes )
from database import close_database

# Initialize session state for user authentication
if "user" not in st.session_state:
    st.session_state.user = None

def main():

    
    # Handle Login Flow
    if st.session_state.user is None:
        st.title("🔐 Login - Rehabilitation Management System")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                # Replace with your actual auth logic
                user = login(username, password) 
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        return

    # Application Menu (Visible when logged in)
    user = st.session_state.user
    role = user.get("role")
    
    st.sidebar.title(f"Navigation ({role})")
    
    # Define role-based menu options using selectbox
    if role == "Admin":
        options = [
            "Add Client", "View Clients", "Update Client", "Delete Client",
            "Add Therapist", "View Therapists", "Update Therapist", "Delete Therapist",
            "Book Appointment", "View Appointments", "Cancel Appointment", 
            "Complete Appointment", "Delete Appointment", "Add Therapy Note", 
            "View Therapy Notes", "Search Therapy Notes", "Update Therapy Note", 
            "Delete Therapy Note", "Export Therapy Notes", "Count Therapy Notes", 
            "View Client Progress", "Change Password", "Logout"
        ]
    elif role == "Therapist":
        options = [
            "View Clients", "View Therapists", "Book Appointment", 
            "View Appointments", "Cancel Appointment", "Complete Appointment", 
            "Add Therapy Note", "View Therapy Notes", "Search Therapy Notes", 
            "Export Therapy Notes", "Count Therapy Notes", "View Client Progress", 
            "Change Password", "Logout"
        ]
    else:
        st.error("Unknown user role.")
        return

    choice = st.sidebar.selectbox("Choose an action", options)
    
    # Route the user's choice to the corresponding function
    render_view(choice, user)

def render_view(choice, user):
    """Maps the Streamlit sidebar selection to the corresponding function."""
    
    # ---------- CLIENTS ----------
    if choice == "Add Client":
        add_client()
    elif choice == "View Clients":
        view_clients()
    elif choice == "Update Client":
        update_client()
    elif choice == "Delete Client":
        delete_client()

    # ---------- THERAPISTS ----------
    elif choice == "Add Therapist":
        add_therapist()
    elif choice == "View Therapists":
        view_therapists()
    elif choice == "Update Therapist":
        update_therapist()
    elif choice == "Delete Therapist":
        delete_therapist()

    # ---------- APPOINTMENTS ----------
    elif choice == "Book Appointment":
        book_appointment()
    elif choice == "View Appointments":
        view_appointments()
    elif choice == "Cancel Appointment":
        cancel_appointment()
    elif choice == "Complete Appointment":
        complete_appointment()
    elif choice == "Delete Appointment":
        delete_appointment()

    # ---------- THERAPY NOTES ----------
    elif choice == "Add Therapy Note":
        add_note()
    elif choice == "View Therapy Notes":
        view_notes()
    elif choice == "Search Therapy Notes":
        search_notes()
    elif choice == "Update Therapy Note":
        update_note()
    elif choice == "Delete Therapy Note":
        delete_note()
    elif choice == "Export Therapy Notes":
        export_notes_csv()
    elif choice == "Count Therapy Notes":
        count_notes()

    # ---------- CLIENT PROGRESS ----------
    elif choice == "View Client Progress":
        view_progress()

    # ---------- PASSWORD & LOGOUT ----------
    elif choice == "Change Password":
        change_password(user)
    elif choice == "Logout":
        logout()
        st.session_state.user = None
        st.rerun()

if __name__ == "__main__":
    main()