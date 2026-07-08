import streamlit as st
from database import conn, cursor
from validation import (
    validate_name,
    validate_age,
    validate_gender,
    validate_email,
    validate_sessions
)

st.set_page_config(page_title="Rehab Clinic Tracker", layout="wide")

def calculate_progress(completed, total):
    if total == 0:
        return 0
    return (completed / total) * 100

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("Navigation")
action = st.sidebar.radio(
    "Choose Action",
    ["Add Client", "View Clients", "Update Client", "Delete Client", "View Progress"]
)

# ==========================================
# ADD CLIENT
# ==========================================
if action == "Add Client":
    st.subheader("Add New Client")
    with st.form("add_client_form"):
        name = st.text_input("Enter Name:")
        age = st.text_input("Enter Age:")
        gender = st.selectbox("Enter Gender", ["Male", "Female", "Other"])
        email = st.text_input("Enter Email:")
        condition = st.text_input("Enter Rehabilitation Condition:")
        total = st.text_input("Total Therapy Sessions:")
        completed = st.text_input("Completed Sessions:")
        submitted = st.form_submit_button("Add Client")
        
        if submitted:
            # Validations
            valid, msg = validate_name(name)
            if not valid: st.error(msg); st.stop()
            valid, msg = validate_age(age)
            if not valid: st.error(msg); st.stop()
            valid, msg = validate_gender(gender)
            if not valid: st.error(msg); st.stop()
            valid, msg = validate_email(email)
            if not valid: st.error(msg); st.stop()
            
            if not condition.strip():
                st.error("Condition cannot be empty."); st.stop()
                
            valid, msg = validate_sessions(total)
            if not valid: st.error(msg); st.stop()
            valid, msg = validate_sessions(completed)
            if not valid: st.error(msg); st.stop()
            
            if int(completed) > int(total):
                st.error("Completed sessions cannot exceed total sessions."); st.stop()

            try:
                cursor.execute("""
                    INSERT INTO clients (name, age, gender, email, condition, completed_sessions, total_sessions) 
                    VALUES(?,?,?,?,?,?,?)
                """, (name, int(age), gender, email, condition, int(completed), int(total)))
                conn.commit()
                st.success("Client added successfully.")
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# VIEW CLIENTS
# ==========================================
elif action == "View Clients":
    st.subheader("Client Directory")
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    
    if not clients:
        st.info("No clients found.")
    else:
        for client in clients:
            progress = calculate_progress(client[6], client[7])
            with st.expander(f"{client[1]} (ID: {client[0]})"):
                st.write(f"**Age:** {client[2]}")
                st.write(f"**Gender:** {client[3]}")
                st.write(f"**Email:** {client[4]}")
                st.write(f"**Condition:** {client[5]}")
                st.write(f"**Sessions:** {client[6]} / {client[7]} completed")
                st.progress(progress / 100)
                st.write(f"**Progress:** {progress:.2f}%")

# ==========================================
# UPDATE CLIENT
# ==========================================
elif action == "Update Client":
    st.subheader("Update Client Information")
    client_id = st.text_input("Enter Client ID to update:")
    
    if client_id:
        cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
        client = cursor.fetchone()
        
        if client is None:
            st.warning("Client not found.")
        else:
            with st.form("update_client_form"):
                name = st.text_input("New Name", value=client[1])
                age = st.text_input("New Age", value=client[2])
                gender = st.text_input("New Gender", value=client[3])
                email = st.text_input("New Email", value=client[4])
                condition = st.text_input("New Condition", value=client[5])
                total = st.text_input("Total Sessions", value=client[7])
                completed = st.text_input("Completed Sessions", value=client[6])
                updated = st.form_submit_button("Update Client")
                
                if updated:
                    valid, msg = validate_name(name)
                    if not valid: st.error(msg); st.stop()
                    valid, msg = validate_age(age)
                    if not valid: st.error(msg); st.stop()
                    valid, msg = validate_gender(gender)
                    if not valid: st.error(msg); st.stop()
                    valid, msg = validate_email(email)
                    if not valid: st.error(msg); st.stop()
                    valid, msg = validate_sessions(total)
                    if not valid: st.error(msg); st.stop()
                    valid, msg = validate_sessions(completed)
                    if not valid: st.error(msg); st.stop()
                    
                    if int(completed) > int(total):
                        st.error("Completed sessions cannot exceed total sessions."); st.stop()

                    try:
                        cursor.execute("""
                            UPDATE clients SET name=?, age=?, gender=?, email=?, condition=?, completed_sessions=?, total_sessions=? 
                            WHERE client_id=?
                        """, (name, int(age), gender, email, condition, int(completed), int(total), client_id))
                        conn.commit()
                        st.success("Client updated successfully.")
                    except Exception as e:
                        st.error(f"Error: {e}")

# ==========================================
# DELETE CLIENT
# ==========================================
elif action == "Delete Client":
    st.subheader("Delete Client")
    client_id = st.text_input("Enter Client ID to delete:")
    
    if st.button("Delete"):
        cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
        if cursor.fetchone() is None:
            st.warning("Client not found.")
        else:
            cursor.execute("DELETE FROM clients WHERE client_id=?", (client_id,))
            conn.commit()
            st.success("Client deleted successfully.")

# ==========================================
# VIEW SINGLE CLIENT PROGRESS
# ==========================================
elif action == "View Progress":
    st.subheader("View Client Progress")
    client_id = st.text_input("Enter Client ID:")
    
    if st.button("Fetch Progress"):
        cursor.execute("SELECT name, completed_sessions, total_sessions FROM clients WHERE client_id=?", (client_id,))
        client = cursor.fetchone()
        
        if client is None:
            st.warning("Client not found.")
        else:
            progress = calculate_progress(client[1], client[2])
            st.write(f"**Name:** {client[0]}")
            st.write(f"**Completed Sessions:** {client[1]}")
            st.write(f"**Total Sessions:** {client[2]}")
            st.progress(progress / 100)
            st.write(f"**Treatment Progress:** {progress:.2f}%")