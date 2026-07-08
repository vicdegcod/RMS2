import streamlit as st
import pandas as pd
import csv
import io
from database import conn, cursor
from validation import validate_date

# --- PAGE CONFIG ---
st.set_page_config(page_title="Therapy Notes Dashboard", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
action = st.sidebar.radio("Choose an action", 
                         ["Add Note", "View All Notes", "Search Notes", "Update Note", "Delete Note", "Export & Stats"])

# --- HELPER: GET NOTE DETAILS ---
def get_note_details():
    cursor.execute("""
        SELECT therapy_notes.note_id, clients.name, therapists.name, therapy_notes.session_date, therapy_notes.notes 
        FROM therapy_notes 
        JOIN clients ON therapy_notes.client_id = clients.client_id 
        JOIN therapists ON therapy_notes.therapist_id = therapists.therapist_id
    """)
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["Note ID", "Client", "Therapist", "Date", "Notes"])

# --- 1. ADD NOTE ---
if action == "Add Note":
    st.subheader("Add Therapy Note")
    with st.form("add_note_form"):
        client_id = st.text_input("Client ID")
        therapist_id = st.text_input("Therapist ID")
        session_date = st.text_input("Session Date (YYYY-MM-DD)")
        notes = st.text_area("Therapy Notes")
        submit = st.form_submit_button("Save Note")
        
        if submit:
            cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
            if cursor.fetchone() is None:
                st.error("Client not found.")
            else:
                cursor.execute("SELECT * FROM therapists WHERE therapist_id=?", (therapist_id,))
                if cursor.fetchone() is None:
                    st.error("Therapist not found.")
                else:
                    valid, message = validate_date(session_date)
                    if not valid:
                        st.error(message)
                    elif notes.strip() == "":
                        st.warning("Notes cannot be empty.")
                    else:
                        cursor.execute("""
                            INSERT INTO therapy_notes (client_id, therapist_id, session_date, notes) 
                            VALUES (?, ?, ?, ?)
                        """, (client_id, therapist_id, session_date, notes))
                        conn.commit()
                        st.success("Therapy note saved successfully!")

# --- 2. VIEW ALL NOTES ---
elif action == "View All Notes":
    st.subheader("All Therapy Notes")
    df = get_note_details()
    if df.empty:
        st.info("No therapy notes found.")
    else:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

# --- 3. SEARCH NOTES ---
elif action == "Search Notes":
    st.subheader("Search Notes by Client")
    client_id = st.text_input("Enter Client ID")
    if st.button("Search"):
        cursor.execute("""
            SELECT therapy_notes.note_id, clients.name, therapists.name, therapy_notes.session_date, therapy_notes.notes 
            FROM therapy_notes 
            JOIN clients ON therapy_notes.client_id = clients.client_id 
            JOIN therapists ON therapy_notes.therapist_id = therapists.therapist_id 
            WHERE therapy_notes.client_id = ? ORDER BY therapy_notes.session_date DESC
        """, (client_id,))
        rows = cursor.fetchall()
        if not rows:
            st.info("No notes found for this Client ID.")
        else:
            df_search = pd.DataFrame(rows, columns=["Note ID", "Client", "Therapist", "Date", "Notes"])
            st.dataframe(df_search, use_container_width=True)

# --- 4. UPDATE NOTE ---
elif action == "Update Note":
    st.subheader("Update Therapy Note")
    with st.form("update_note_form"):
        note_id = st.text_input("Enter Note ID to Update")
        new_date = st.text_input("New Session Date (YYYY-MM-DD)")
        new_notes = st.text_area("Enter Updated Notes")
        submit_update = st.form_submit_button("Update Note")
        
        if submit_update:
            cursor.execute("SELECT * FROM therapy_notes WHERE note_id=?", (note_id,))
            if cursor.fetchone() is None:
                st.error("Note not found.")
            else:
                valid, message = validate_date(new_date)
                if not valid:
                    st.error(message)
                elif new_notes.strip() == "":
                    st.warning("Notes cannot be empty.")
                else:
                    cursor.execute("""
                        UPDATE therapy_notes SET session_date=?, notes=? WHERE note_id=?
                    """, (new_date, new_notes, note_id))
                    conn.commit()
                    st.success("Therapy note updated successfully!")

# --- 5. DELETE NOTE ---
elif action == "Delete Note":
    st.subheader("Delete Therapy Note")
    note_id = st.text_input("Enter Note ID to Delete")
    if st.button("Delete Note"):
        cursor.execute("SELECT * FROM therapy_notes WHERE note_id=?", (note_id,))
        if cursor.fetchone() is None:
            st.error("Note not found.")
        else:
            cursor.execute("DELETE FROM therapy_notes WHERE note_id=?", (note_id,))
            conn.commit()
            st.success("Therapy note deleted successfully!")

# --- 6. EXPORT & STATS ---
elif action == "Export & Stats":
    st.subheader("Export Data & Statistics")
    df = get_note_details()
    
    # Count Notes
    st.write(f"**Total Therapy Notes:** {len(df)}")
    
    # Export CSV
    if not df.empty:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Notes as CSV",
            data=csv_buffer.getvalue(),
            file_name="therapy_notes.csv",
            mime="text/csv"
        )