import streamlit as st
from database import cursor, conn

# ==========================================
# LOGIN
# ==========================================

def login(username, password):

    cursor.execute("""
        SELECT username, password, role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user is None:
        return None

    # Plain-text password comparison
    # Replace with bcrypt.checkpw() if using hashed passwords
    if password != user[1]:
        return None

    return {
        "username": user[0],
        "role": user[2]
    }


# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state.user = None


# ==========================================
# CHANGE PASSWORD
# ==========================================

def change_password(user):

    st.subheader("Change Password")

    with st.form("change_password"):

        old_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Update Password"
        )

    if submit:

        cursor.execute("""
            SELECT password
            FROM users
            WHERE username=?
        """, (user["username"],))

        current_password = cursor.fetchone()[0]

        if old_password != current_password:

            st.error("Current password is incorrect.")

            return

        if len(new_password) < 4:

            st.error("Password must be at least 4 characters.")

            return

        if new_password != confirm_password:

            st.error("Passwords do not match.")

            return

        cursor.execute("""
            UPDATE users
            SET password=?
            WHERE username=?
        """, (
            new_password,
            user["username"]
        ))

        conn.commit()

        st.success("Password changed successfully.")