from database import conn, cursor
from validation import (
    validate_name,
    validate_age,
    validate_gender,
    validate_email,
    validate_sessions
)

# ==========================================
# ADD CLIENT
# ==========================================

def add_client():

    print("\n===== ADD CLIENT =====")

    name = input("Enter Name: ")

    valid, message = validate_name(name)
    if not valid:
        print(message)
        return

    age = input("Enter Age: ")

    valid, message = validate_age(age)
    if not valid:
        print(message)
        return

    gender = input("Enter Gender (Male/Female/Other): ")

    valid, message = validate_gender(gender)
    if not valid:
        print(message)
        return

    email = input("Enter Email: ")

    valid, message = validate_email(email)
    if not valid:
        print(message)
        return

    condition = input("Enter Rehabilitation Condition: ")

    if condition.strip() == "":
        print("Condition cannot be empty.")
        return

    total = input("Total Therapy Sessions: ")

    valid, message = validate_sessions(total)
    if not valid:
        print(message)
        return

    completed = input("Completed Sessions: ")

    valid, message = validate_sessions(completed)
    if not valid:
        print(message)
        return

    if int(completed) > int(total):
        print("Completed sessions cannot exceed total sessions.")
        return

    try:
        cursor.execute("""
        INSERT INTO clients
        (name, age, gender, email, condition,
         completed_sessions, total_sessions)

        VALUES(?,?,?,?,?,?,?)
        """,
        (
            name,
            int(age),
            gender,
            email,
            condition,
            int(completed),
            int(total)
        ))

        conn.commit()

        print("Client added successfully.")

    except Exception as e:
        print("Error:", e)


# ==========================================
# VIEW CLIENTS
# ==========================================

def view_clients():

    cursor.execute("""
    SELECT * FROM clients
    """)

    clients = cursor.fetchall()

    if len(clients) == 0:
        print("\nNo clients found.")
        return

    print("\n================ CLIENTS ================")

    for client in clients:

        progress = calculate_progress(
            client[6],
            client[7]
        )

        print(f"""
Client ID : {client[0]}
Name      : {client[1]}
Age       : {client[2]}
Gender    : {client[3]}
Email     : {client[4]}
Condition : {client[5]}
Completed : {client[6]}
Total     : {client[7]}
Progress  : {progress:.2f}%
-----------------------------------------
""")


# ==========================================
# UPDATE CLIENT
# ==========================================

def update_client():

    client_id = input("Enter Client ID: ")

    cursor.execute("""
    SELECT * FROM clients
    WHERE client_id=?
    """,(client_id,))

    client = cursor.fetchone()

    if client is None:
        print("Client not found.")
        return

    name = input("New Name: ")

    valid, message = validate_name(name)
    if not valid:
        print(message)
        return

    age = input("New Age: ")

    valid, message = validate_age(age)
    if not valid:
        print(message)
        return

    gender = input("New Gender: ")

    valid, message = validate_gender(gender)
    if not valid:
        print(message)
        return

    email = input("New Email: ")

    valid, message = validate_email(email)
    if not valid:
        print(message)
        return

    condition = input("New Condition: ")

    total = input("Total Sessions: ")

    valid, message = validate_sessions(total)
    if not valid:
        print(message)
        return

    completed = input("Completed Sessions: ")

    valid, message = validate_sessions(completed)
    if not valid:
        print(message)
        return

    if int(completed) > int(total):
        print("Completed sessions cannot exceed total sessions.")
        return

    try:

        cursor.execute("""
        UPDATE clients

        SET
        name=?,
        age=?,
        gender=?,
        email=?,
        condition=?,
        completed_sessions=?,
        total_sessions=?

        WHERE client_id=?
        """,
        (
            name,
            int(age),
            gender,
            email,
            condition,
            int(completed),
            int(total),
            client_id
        ))

        conn.commit()

        print("Client updated successfully.")

    except Exception as e:
        print("Error:", e)


# ==========================================
# DELETE CLIENT
# ==========================================

def delete_client():

    client_id = input("Enter Client ID to delete: ")

    cursor.execute("""
    SELECT * FROM clients
    WHERE client_id=?
    """,(client_id,))

    if cursor.fetchone() is None:
        print("Client not found.")
        return

    cursor.execute("""
    DELETE FROM clients
    WHERE client_id=?
    """,(client_id,))

    conn.commit()

    print("Client deleted successfully.")


# ==========================================
# CALCULATE PROGRESS
# ==========================================

def calculate_progress(completed, total):

    if total == 0:
        return 0

    return (completed / total) * 100


# ==========================================
# VIEW SINGLE CLIENT PROGRESS
# ==========================================

def view_progress():

    client_id = input("Enter Client ID: ")

    cursor.execute("""
    SELECT name,
           completed_sessions,
           total_sessions

    FROM clients

    WHERE client_id=?
    """,(client_id,))

    client = cursor.fetchone()

    if client is None:
        print("Client not found.")
        return

    progress = calculate_progress(client[1], client[2])

    print("\n========== CLIENT PROGRESS ==========")
    print("Name:", client[0])
    print("Completed Sessions:", client[1])
    print("Total Sessions:", client[2])
    print("Treatment Progress: {:.2f}%".format(progress))