import streamlit as st
from database import cursor, conn  # Ensure your database setup is in a 'database.py' file

# Initialize session state for user session tracking
if "user" not in st.session_state:
    st.session_state.user = None

# ==========================================
# AUTHENTICATION & ROLE CHECKS
# ==========================================
def is_admin():
    return st.session_state.user is not None and st.session_state.user["role"] == "Admin"

def is_therapist():
    return st.session_state.user is not None and st.session_state.user["role"] == "Therapist"

# ==========================================
# STREAMLIT UI SCREENS
# ==========================================

def login_screen():
    st.subheader("Login")
    
    # Form prevents page from reloading until user clicks Submit
    with st.form("login_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user is None:
                st.error("Invalid username.")
            elif password != user[1]:
                st.error("Incorrect password.")
            else:
                # Save user info into session state
                st.session_state.user = {
                    "username": user[0],
                    "role": user[2]
                }
                st.success(f"Welcome {user[0]}! Logged in as: {user[2]}")
                st.rerun()  # Refresh app to load the logged-in state

def change_password_screen():
    st.subheader("Change Password")
    
    with st.form("change_password_form"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password").strip()
        confirm = st.text_input("Confirm Password", type="password").strip()
        submit_button = st.form_submit_button("Update Password")
        
        if submit_button:
            # Fetch current password from DB
            cursor.execute("SELECT password FROM users WHERE username = ?", (st.session_state.user["username"],))
            stored_password = cursor.fetchone()[0]
            
            if old_password != stored_password:
                st.error("Current password is incorrect.")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters.")
            elif new_password != confirm:
                st.error("Passwords do not match.")
            else:
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, st.session_state.user["username"]))
                conn.commit()
                st.success("Password changed successfully.")

def logout_user():
    st.session_state.user = None
    st.success("You have logged out successfully.")
    st.rerun()

# ==========================================
# APP MAIN NAVIGATION & LAYOUT
# ==========================================

st.title("User Portal")

# Scenario 1: User is not logged in
if st.session_state.user is None:
    login_screen()

# Scenario 2: User is logged in
else:
    # Sidebar navigation dashboard
    st.sidebar.title(f"Hello, {st.session_state.user['username']}")
    st.sidebar.write(f"Role: **{st.session_state.user['role']}**")
    
    # Render different menu options based on Roles
    menu_options = ["Dashboard", "Change Password"]
    if is_admin():
        menu_options.append("Admin Panel")
    if is_therapist():
        menu_options.append("Therapist Tools")
        
    choice = st.sidebar.radio("Navigation", menu_options)
    
    # Logout button at the bottom of sidebar
    if st.sidebar.button("Logout"):
        logout_user()

    # App Routing based on sidebar selection
    if choice == "Dashboard":
        st.write("Welcome to your dashboard main page.")
        
    elif choice == "Change Password":
        change_password_screen()
        
    elif choice == "Admin Panel":
        st.write("### Welcome Admin")
        st.info("This section is only visible to users with the 'Admin' role.")
        
    elif choice == "Therapist Tools":
        st.write("### Welcome Therapist")
        st.info("This section is only visible to users with the 'Therapist' role.")