from database import conn, cursor
from validation import (
    validate_name,
    validate_email,
    validate_phone
)

# ==========================================
# ADD THERAPIST
# ==========================================

def add_therapist():

    print("\n===== ADD THERAPIST =====")

    name = input("Enter Therapist Name: ")

    valid, message = validate_name(name)
    if not valid:
        print(message)
        return

    specialization = input("Enter Specialization: ")

    if specialization.strip() == "":
        print("Specialization cannot be empty.")
        return

    phone = input("Enter Phone Number: ")

    valid, message = validate_phone(phone)
    if not valid:
        print(message)
        return

    email = input("Enter Email: ")

    valid, message = validate_email(email)
    if not valid:
        print(message)
        return

    try:

        cursor.execute("""
        INSERT INTO therapists
        (name, specialization, phone, email)

        VALUES (?,?,?,?)
        """,
        (
            name,
            specialization,
            phone,
            email
        ))

        conn.commit()

        print("Therapist added successfully.")

    except Exception as e:
        print("Error:", e)


# ==========================================
# VIEW THERAPISTS
# ==========================================

def view_therapists():

    cursor.execute("""
    SELECT * FROM therapists
    """)

    therapists = cursor.fetchall()

    if len(therapists) == 0:
        print("\nNo therapists found.")
        return

    print("\n========== THERAPISTS ==========")

    for therapist in therapists:

        print(f"""
Therapist ID : {therapist[0]}
Name         : {therapist[1]}
Specialization: {therapist[2]}
Phone        : {therapist[3]}
Email        : {therapist[4]}
----------------------------------------
""")


# ==========================================
# UPDATE THERAPIST
# ==========================================

def update_therapist():

    therapist_id = input("Enter Therapist ID: ")

    cursor.execute("""
    SELECT * FROM therapists
    WHERE therapist_id = ?
    """, (therapist_id,))

    therapist = cursor.fetchone()

    if therapist is None:
        print("Therapist not found.")
        return

    name = input("New Name: ")

    valid, message = validate_name(name)
    if not valid:
        print(message)
        return

    specialization = input("New Specialization: ")

    if specialization.strip() == "":
        print("Specialization cannot be empty.")
        return

    phone = input("New Phone Number: ")

    valid, message = validate_phone(phone)
    if not valid:
        print(message)
        return

    email = input("New Email: ")

    valid, message = validate_email(email)
    if not valid:
        print(message)
        return

    try:

        cursor.execute("""
        UPDATE therapists

        SET
        name=?,
        specialization=?,
        phone=?,
        email=?

        WHERE therapist_id=?
        """,
        (
            name,
            specialization,
            phone,
            email,
            therapist_id
        ))

        conn.commit()

        print("Therapist updated successfully.")

    except Exception as e:
        print("Error:", e)


# ==========================================
# DELETE THERAPIST
# ==========================================

def delete_therapist():

    therapist_id = input("Enter Therapist ID to delete: ")

    cursor.execute("""
    SELECT * FROM therapists
    WHERE therapist_id = ?
    """, (therapist_id,))

    therapist = cursor.fetchone()

    if therapist is None:
        print("Therapist not found.")
        return

    cursor.execute("""
    DELETE FROM therapists
    WHERE therapist_id = ?
    """, (therapist_id,))

    conn.commit()

    print("Therapist deleted successfully.")


# ==========================================
# SEARCH THERAPIST
# ==========================================

def search_therapist():

    therapist_id = input("Enter Therapist ID: ")

    cursor.execute("""
    SELECT * FROM therapists
    WHERE therapist_id = ?
    """, (therapist_id,))

    therapist = cursor.fetchone()

    if therapist is None:
        print("Therapist not found.")
        return

    print("\n========== THERAPIST DETAILS ==========")
    print("Therapist ID :", therapist[0])
    print("Name         :", therapist[1])
    print("Specialization :", therapist[2])
    print("Phone        :", therapist[3])
    print("Email        :", therapist[4])