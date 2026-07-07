from database import cursor


# ==========================================
# LOGIN
# ==========================================

def login():

    print("\n========== LOGIN ==========")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    cursor.execute("""
    SELECT username, password, role
    FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user is None:
        print("Invalid username.")
        return None

    if password != user[1]:
        print("Incorrect password.")
        return None

    print(f"\nWelcome {user[0]}!")
    print("Logged in as:", user[2])

    return {
        "username": user[0],
        "role": user[2]
    }


# ==========================================
# ADMIN CHECK
# ==========================================

def is_admin(user):

    if user is None:
        return False

    return user["role"] == "Admin"


# ==========================================
# THERAPIST CHECK
# ==========================================

def is_therapist(user):

    if user is None:
        return False

    return user["role"] == "Therapist"


# ==========================================
# CHANGE PASSWORD
# ==========================================

def change_password(user):

    if user is None:
        print("You must login first.")
        return

    old_password = input("Current Password: ")

    cursor.execute("""
    SELECT password
    FROM users
    WHERE username = ?
    """, (user["username"],))

    stored_password = cursor.fetchone()[0]

    if old_password != stored_password:
        print("Current password is incorrect.")
        return

    new_password = input("New Password: ").strip()

    if len(new_password) < 4:
        print("Password must be at least 4 characters.")
        return

    confirm = input("Confirm Password: ").strip()

    if new_password != confirm:
        print("Passwords do not match.")
        return

    cursor.execute("""
    UPDATE users
    SET password = ?
    WHERE username = ?
    """, (new_password, user["username"]))

    from database import conn
    conn.commit()

    print("Password changed successfully.")


# ==========================================
# LOGOUT
# ==========================================

def logout():

    print("\nYou have logged out successfully.")
    return None