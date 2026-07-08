import streamlit as st
from database import conn, cursor
from validation import validate_date

# --- PAGE CONFIG ---
st.set_page_config(page_title="Appointment Manager", layout="wide")
st.title("🏥 Appointment Management System")

# --- NAVIGATION ---
st.sidebar.title("Menu")
action = st.sidebar.radio(
    "Choose an action:",
    ["Book Appointment", "View Appointments", "Cancel Appointment", "Complete Appointment", "Delete Appointment"]
)

# ==========================================
# BOOK APPOINTMENT
# ==========================================
if action == "Book Appointment":
    st.subheader("===== BOOK APPOINTMENT =====")
    
    with st.form("book_form"):
        client_id = st.text_input("Enter Client ID:")
        therapist_id = st.text_input("Enter Therapist ID:")
        appointment_date = st.text_input("Enter Appointment Date (YYYY-MM-DD):")
        submit_btn = st.form_submit_button("Book Appointment")
        
        if submit_btn:
            # Check Client
            cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
            if cursor.fetchone() is None:
                st.error("Client not found.")
            # Check Therapist
            elif cursor.execute("SELECT * FROM therapists WHERE therapist_id=?", (therapist_id,)).fetchone() is None:
                st.error("Therapist not found.")
            else:
                valid, message = validate_date(appointment_date)
                if not valid:
                    st.error(message)
                else:
                    cursor.execute("""
                        INSERT INTO appointments (client_id, therapist_id, appointment_date, status) 
                        VALUES(?,?,?,?)
                    """, (client_id, therapist_id, appointment_date, 'Booked'))
                    conn.commit()
                    st.success("Appointment booked successfully.")

# ==========================================
# VIEW APPOINTMENTS
# ==========================================
elif action == "View Appointments":
    st.subheader("========== APPOINTMENTS ==========")
    
    cursor.execute("""
        SELECT appointments.appointment_id, clients.name, therapists.name, 
               appointments.appointment_date, appointments.status 
        FROM appointments 
        JOIN clients ON appointments.client_id = clients.client_id 
        JOIN therapists ON appointments.therapist_id = therapists.therapist_id 
        ORDER BY appointments.appointment_date
    """)
    appointments = cursor.fetchall()
    
    if len(appointments) == 0:
        st.info("No appointments found.")
    else:
        for appt in appointments:
            with st.container():
                st.markdown(f"**Appointment ID:** {appt[0]} | **Date:** {appt[3]}")
                st.markdown(f"**Client:** {appt[1]} | **Therapist:** {appt[2]}")
                st.markdown(f"**Status:** {appt[4]}")
                st.markdown("---")

# ==========================================
# CANCEL APPOINTMENT
# ==========================================
elif action == "Cancel Appointment":
    st.subheader("===== CANCEL APPOINTMENT =====")
    
    with st.form("cancel_form"):
        appointment_id = st.text_input("Enter Appointment ID to Cancel:")
        cancel_btn = st.form_submit_button("Cancel Appointment")
        
        if cancel_btn:
            cursor.execute("SELECT * FROM appointments WHERE appointment_id=?", (appointment_id,))
            if cursor.fetchone() is None:
                st.error("Appointment not found.")
            else:
                cursor.execute("UPDATE appointments SET status='Cancelled' WHERE appointment_id=?", (appointment_id,))
                conn.commit()
                st.success("Appointment cancelled successfully.")

# ==========================================
# COMPLETE APPOINTMENT
# ==========================================
elif action == "Complete Appointment":
    st.subheader("===== COMPLETE APPOINTMENT =====")
    
    with st.form("complete_form"):
        appointment_id = st.text_input("Enter Appointment ID to Complete:")
        complete_btn = st.form_submit_button("Complete Appointment")
        
        if complete_btn:
            cursor.execute("SELECT client_id, status FROM appointments WHERE appointment_id=?", (appointment_id,))
            appointment = cursor.fetchone()
            
            if appointment is None:
                st.error("Appointment not found.")
            elif appointment[1] == 'Cancelled':
                st.error("Cancelled appointments cannot be completed.")
            else:
                cursor.execute("UPDATE appointments SET status='Completed' WHERE appointment_id=?", (appointment_id,))
                cursor.execute("""
                    UPDATE clients SET completed_sessions = completed_sessions + 1 
                    WHERE client_id=? AND completed_sessions < total_sessions
                """, (appointment[0],))
                conn.commit()
                st.success("Appointment marked as completed.")

# ==========================================
# DELETE APPOINTMENT
# ==========================================
elif action == "Delete Appointment":
    st.subheader("===== DELETE APPOINTMENT =====")
    
    with st.form("delete_form"):
        appointment_id = st.text_input("Enter Appointment ID to Delete:")
        delete_btn = st.form_submit_button("Delete Appointment")
        
        if delete_btn:
            cursor.execute("SELECT * FROM appointments WHERE appointment_id=?", (appointment_id,))
            if cursor.fetchone() is None:
                st.error("Appointment not found.")
            else:
                cursor.execute("DELETE FROM appointments WHERE appointment_id=?", (appointment_id,))
                conn.commit()
                st.success("Appointment deleted successfully.")