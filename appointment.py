from database import conn, cursor
from validation import validate_date

# ==========================================
# BOOK APPOINTMENT
# ==========================================

def book_appointment():

    print("\n===== BOOK APPOINTMENT =====")

    client_id = input("Enter Client ID: ")

    cursor.execute("""
    SELECT * FROM clients
    WHERE client_id=?
    """, (client_id,))

    client = cursor.fetchone()

    if client is None:
        print("Client not found.")
        return

    therapist_id = input("Enter Therapist ID: ")

    cursor.execute("""
    SELECT * FROM therapists
    WHERE therapist_id=?
    """, (therapist_id,))

    therapist = cursor.fetchone()

    if therapist is None:
        print("Therapist not found.")
        return

    appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")

    valid, message = validate_date(appointment_date)

    if not valid:
        print(message)
        return

    cursor.execute("""
    INSERT INTO appointments
    (client_id, therapist_id, appointment_date, status)

    VALUES(?,?,?,?)
    """,
    (
        client_id,
        therapist_id,
        appointment_date,
        "Booked"
    ))

    conn.commit()

    print("Appointment booked successfully.")


# ==========================================
# VIEW APPOINTMENTS
# ==========================================

def view_appointments():

    cursor.execute("""
    SELECT
        appointments.appointment_id,
        clients.name,
        therapists.name,
        appointments.appointment_date,
        appointments.status

    FROM appointments

    JOIN clients
    ON appointments.client_id = clients.client_id

    JOIN therapists
    ON appointments.therapist_id = therapists.therapist_id

    ORDER BY appointments.appointment_date
    """)

    appointments = cursor.fetchall()

    if len(appointments) == 0:
        print("\nNo appointments found.")
        return

    print("\n========== APPOINTMENTS ==========")

    for appointment in appointments:

        print(f"""
Appointment ID : {appointment[0]}
Client         : {appointment[1]}
Therapist      : {appointment[2]}
Date           : {appointment[3]}
Status         : {appointment[4]}
---------------------------------------
""")


# ==========================================
# CANCEL APPOINTMENT
# ==========================================

def cancel_appointment():

    appointment_id = input("Enter Appointment ID: ")

    cursor.execute("""
    SELECT * FROM appointments
    WHERE appointment_id=?
    """, (appointment_id,))

    appointment = cursor.fetchone()

    if appointment is None:
        print("Appointment not found.")
        return

    cursor.execute("""
    UPDATE appointments

    SET status='Cancelled'

    WHERE appointment_id=?
    """, (appointment_id,))

    conn.commit()

    print("Appointment cancelled successfully.")


# ==========================================
# COMPLETE APPOINTMENT
# ==========================================

def complete_appointment():

    appointment_id = input("Enter Appointment ID: ")

    cursor.execute("""
    SELECT client_id,status

    FROM appointments

    WHERE appointment_id=?
    """, (appointment_id,))

    appointment = cursor.fetchone()

    if appointment is None:
        print("Appointment not found.")
        return

    if appointment[1] == "Cancelled":
        print("Cancelled appointments cannot be completed.")
        return

    cursor.execute("""
    UPDATE appointments

    SET status='Completed'

    WHERE appointment_id=?
    """, (appointment_id,))

    cursor.execute("""
    UPDATE clients

    SET completed_sessions = completed_sessions + 1

    WHERE client_id=?
    AND completed_sessions < total_sessions
    """, (appointment[0],))

    conn.commit()

    print("Appointment marked as completed.")


# ==========================================
# DELETE APPOINTMENT
# ==========================================

def delete_appointment():

    appointment_id = input("Enter Appointment ID: ")

    cursor.execute("""
    SELECT * FROM appointments
    WHERE appointment_id=?
    """, (appointment_id,))

    if cursor.fetchone() is None:
        print("Appointment not found.")
        return

    cursor.execute("""
    DELETE FROM appointments
    WHERE appointment_id=?
    """, (appointment_id,))

    conn.commit()

    print("Appointment deleted successfully.")