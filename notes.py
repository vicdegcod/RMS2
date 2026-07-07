from database import conn, cursor
from validation import validate_date
import csv


# ==========================================
# ADD THERAPY NOTE
# ==========================================

def add_note():

    print("\n===== ADD THERAPY NOTE =====")

    client_id = input("Enter Client ID: ")

    cursor.execute("""
    SELECT * FROM clients
    WHERE client_id=?
    """, (client_id,))

    if cursor.fetchone() is None:
        print("Client not found.")
        return

    therapist_id = input("Enter Therapist ID: ")

    cursor.execute("""
    SELECT * FROM therapists
    WHERE therapist_id=?
    """, (therapist_id,))

    if cursor.fetchone() is None:
        print("Therapist not found.")
        return

    session_date = input("Enter Session Date (YYYY-MM-DD): ")

    valid, message = validate_date(session_date)

    if not valid:
        print(message)
        return

    notes = input("Enter Therapy Notes: ")

    if notes.strip() == "":
        print("Notes cannot be empty.")
        return

    cursor.execute("""
    INSERT INTO therapy_notes
    (client_id, therapist_id, session_date, notes)

    VALUES (?,?,?,?)
    """,
    (
        client_id,
        therapist_id,
        session_date,
        notes
    ))

    conn.commit()

    print("Therapy note saved successfully.")


# ==========================================
# VIEW ALL NOTES
# ==========================================

def view_notes():

    cursor.execute("""
    SELECT
        therapy_notes.note_id,
        clients.name,
        therapists.name,
        therapy_notes.session_date,
        therapy_notes.notes

    FROM therapy_notes

    JOIN clients
    ON therapy_notes.client_id = clients.client_id

    JOIN therapists
    ON therapy_notes.therapist_id = therapists.therapist_id

    ORDER BY therapy_notes.session_date DESC
    """)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("\nNo therapy notes found.")
        return

    print("\n========== THERAPY NOTES ==========")

    for row in rows:

        print(f"""
Note ID    : {row[0]}
Client     : {row[1]}
Therapist  : {row[2]}
Date       : {row[3]}
Notes      : {row[4]}
--------------------------------------------
""")


# ==========================================
# SEARCH NOTES BY CLIENT
# ==========================================

def search_notes():

    client_id = input("Enter Client ID: ")

    cursor.execute("""
    SELECT
        therapy_notes.note_id,
        clients.name,
        therapists.name,
        therapy_notes.session_date,
        therapy_notes.notes

    FROM therapy_notes

    JOIN clients
    ON therapy_notes.client_id = clients.client_id

    JOIN therapists
    ON therapy_notes.therapist_id = therapists.therapist_id

    WHERE therapy_notes.client_id = ?

    ORDER BY therapy_notes.session_date DESC
    """, (client_id,))

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No notes found.")
        return

    for row in rows:

        print(f"""
Note ID    : {row[0]}
Client     : {row[1]}
Therapist  : {row[2]}
Date       : {row[3]}
Notes      : {row[4]}
--------------------------------------------
""")


# ==========================================
# UPDATE NOTE
# ==========================================

def update_note():

    note_id = input("Enter Note ID: ")

    cursor.execute("""
    SELECT *
    FROM therapy_notes
    WHERE note_id=?
    """, (note_id,))

    if cursor.fetchone() is None:
        print("Note not found.")
        return

    session_date = input("New Session Date (YYYY-MM-DD): ")

    valid, message = validate_date(session_date)

    if not valid:
        print(message)
        return

    notes = input("Enter Updated Notes: ")

    if notes.strip() == "":
        print("Notes cannot be empty.")
        return

    cursor.execute("""
    UPDATE therapy_notes

    SET
    session_date=?,
    notes=?

    WHERE note_id=?
    """,
    (
        session_date,
        notes,
        note_id
    ))

    conn.commit()

    print("Therapy note updated successfully.")


# ==========================================
# DELETE NOTE
# ==========================================

def delete_note():

    note_id = input("Enter Note ID: ")

    cursor.execute("""
    SELECT *
    FROM therapy_notes
    WHERE note_id=?
    """, (note_id,))

    if cursor.fetchone() is None:
        print("Note not found.")
        return

    cursor.execute("""
    DELETE FROM therapy_notes
    WHERE note_id=?
    """, (note_id,))

    conn.commit()

    print("Therapy note deleted successfully.")


# ==========================================
# EXPORT NOTES TO CSV
# ==========================================

def export_notes_csv():

    cursor.execute("""
    SELECT
        therapy_notes.note_id,
        clients.name,
        therapists.name,
        therapy_notes.session_date,
        therapy_notes.notes

    FROM therapy_notes

    JOIN clients
    ON therapy_notes.client_id = clients.client_id

    JOIN therapists
    ON therapy_notes.therapist_id = therapists.therapist_id

    ORDER BY therapy_notes.session_date
    """)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No notes available to export.")
        return

    filename = "therapy_notes.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Note ID",
            "Client",
            "Therapist",
            "Session Date",
            "Therapy Notes"
        ])

        writer.writerows(rows)

    print(f"CSV exported successfully as '{filename}'.")


# ==========================================
# COUNT NOTES
# ==========================================

def count_notes():

    cursor.execute("""
    SELECT COUNT(*)
    FROM therapy_notes
    """)

    total = cursor.fetchone()[0]

    print("\nTotal Therapy Notes:", total)