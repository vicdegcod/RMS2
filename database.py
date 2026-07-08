import sqlite3
import streamlit as st
import pandas as pd

# ==============================
# DATABASE CONNECTION
# ==============================
# Using Streamlit state to handle connection cleanly across reruns
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect("rehabilitation.db", check_same_thread=False)

conn = st.session_state.conn
cursor = conn.cursor()

# ==============================
# CREATE TABLES & DEFAULT USERS
# ==============================
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        condition TEXT NOT NULL,
        completed_sessions INTEGER DEFAULT 0,
        total_sessions INTEGER DEFAULT 0
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS therapists(
        therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        therapist_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        status TEXT DEFAULT 'Booked',
        FOREIGN KEY(client_id) REFERENCES clients(client_id),
        FOREIGN KEY(therapist_id) REFERENCES therapists(therapist_id)
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS therapy_notes(
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        therapist_id INTEGER NOT NULL,
        session_date TEXT NOT NULL,
        notes TEXT NOT NULL,
        FOREIGN KEY(client_id) REFERENCES clients(client_id),
        FOREIGN KEY(therapist_id) REFERENCES therapists(therapist_id)
    )""")
    conn.commit()

def create_default_users():
    users = [
        ("admin", "admin123", "Admin"),
        ("therapist", "therapy123", "Therapist")
    ]
    for user in users:
        try:
            cursor.execute("INSERT INTO users(username, password, role) VALUES(?,?,?)", user)
        except sqlite3.IntegrityError:
            pass
    conn.commit()

# Initialize Database
create_tables()
create_default_users()

# ==============================
# SESSION STATE MANAGEMENT
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

# ==============================
# HELPER FUNCTIONS
# ==============================
def verify_login(username, password):
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    return result[0] if result else None

def get_as_dataframe(query):
    return pd.read_sql_query(query, conn)

# ==============================
# LOGIN INTERFACE
# ==============================
if not st.session_state.logged_in:
    st.title("🏥 Rehabilitation Center Portal")
    st.subheader("Login to your account")
    
    with st.form("login_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            user_role = verify_login(username_input, password_input)
            if user_role:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = user_role
                st.success(f"Welcome back, {username_input}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    st.stop()

# ==============================
# MAIN APPLICATION INTERFACE
# ==============================
st.sidebar.title(f"👤 {st.session_state.username}")
st.sidebar.write(f"**Role:** {st.session_state.role}")

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.rerun()

# ------------------------------
# ADMIN DASHBOARD
# ------------------------------
if st.session_state.role == "Admin":
    st.title("🛠️ Admin Command Center")
    
    menu = st.tabs(["Manage Therapists", "Manage Clients", "Schedule Appointments", "View Databases"])
    
    with menu[0]:
        st.header("Add New Therapist")
        with st.form("add_therapist"):
            t_name = st.text_input("Full Name")
            t_spec = st.text_input("Specialization")
            t_phone = st.text_input("Phone Number")
            t_email = st.text_input("Email Address")
            if st.form_submit_button("Register Therapist"):
                try:
                    cursor.execute("INSERT INTO therapists (name, specialization, phone, email) VALUES (?,?,?,?)", (t_name, t_spec, t_phone, t_email))
                    conn.commit()
                    st.success("Therapist registered successfully!")
                except sqlite3.IntegrityError:
                    st.error("Email address already exists!")

    with menu[1]:
        st.header("Add New Client")
        with st.form("add_client"):
            c_name = st.text_input("Full Name")
            c_age = st.number_input("Age", min_value=1, max_value=120, value=30)
            c_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            c_email = st.text_input("Email Address")
            c_cond = st.text_input("Medical Condition")
            c_total = st.number_input("Total Prescribed Sessions", min_value=1, value=10)
            if st.form_submit_button("Register Client"):
                try:
                    cursor.execute("INSERT INTO clients (name, age, gender, email, condition, total_sessions) VALUES (?,?,?,?,?,?)", (c_name, c_age, c_gender, c_email, c_cond, c_total))
                    conn.commit()
                    st.success("Client registered successfully!")
                except sqlite3.IntegrityError:
                    st.error("Email address already exists!")

    with menu[2]:
        st.header("Book an Appointment")
        
        # Pull latest records dynamically for dropdown selections
        clients_df = get_as_dataframe("SELECT client_id, name FROM clients")
        therapists_df = get_as_dataframe("SELECT therapist_id, name FROM therapists")
        
        if clients_df.empty or therapists_df.empty:
            st.warning("Please ensure you have registered both clients and therapists before booking appointments.")
        else:
            with st.form("book_appointment"):
                client_option = st.selectbox("Select Client", clients_df['name'].tolist())
                therapist_option = st.selectbox("Select Therapist", therapists_df['name'].tolist())
                app_date = st.date_input("Appointment Date")
                
                # Fetch database IDs based on names selected
                c_id = int(clients_df[clients_df['name'] == client_option]['client_id'].values[0])
                t_id = int(therapists_df[therapists_df['name'] == therapist_option]['therapist_id'].values[0])
                
                if st.form_submit_button("Schedule Session"):
                    cursor.execute("INSERT INTO appointments (client_id, therapist_id, appointment_date) VALUES (?,?,?)", (c_id, t_id, str(app_date)))
                    conn.commit()
                    st.success("Appointment successfully booked!")

    with menu[3]:
        st.header("System Datasets")
        inspect = st.selectbox("Select Table to View", ["Clients", "Therapists", "Appointments"])
        if inspect == "Clients":
            st.dataframe(get_as_dataframe("SELECT * FROM clients"), use_container_width=True)
        elif inspect == "Therapists":
            st.dataframe(get_as_dataframe("SELECT * FROM therapists"), use_container_width=True)
        elif inspect == "Appointments":
            st.dataframe(get_as_dataframe("SELECT * FROM appointments"), use_container_width=True)

# ------------------------------
# THERAPIST DASHBOARD
# ------------------------------
elif st.session_state.role == "Therapist":
    st.title("🩺 Therapist Workspace")
    
    workspace = st.tabs(["My Appointments", "Session Documentation", "Client Medical Notes"])
    
    with workspace[0]:
        st.header("Upcoming Appointments")
        query = """
        SELECT a.appointment_id, c.name AS Client, a.appointment_date, a.status 
        FROM appointments a 
        JOIN clients c ON a.client_id = c.client_id
        """
        st.dataframe(get_as_dataframe(query), use_container_width=True)

    with workspace[1]:
        st.header("Log Session Notes & Progress")
        
        clients_df = get_as_dataframe("SELECT client_id, name FROM clients")
        therapists_df = get_as_dataframe("SELECT therapist_id, name FROM therapists")
        
        if clients_df.empty or therapists_df.empty:
            st.warning("No clients or therapists found in system.")
        else:
            with st.form("session_notes_form"):
                client_sel = st.selectbox("Client Name", clients_df['name'].tolist())
                therapist_sel = st.selectbox("Your Registered Name", therapists_df['name'].tolist())
                session_date = st.date_input("Session Date")
                note_text = st.text_area("Clinical Progress Observations")
                mark_complete = st.checkbox("Increment completed session count for this client?")