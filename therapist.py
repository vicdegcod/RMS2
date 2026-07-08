import streamlit as st
from database import conn, cursor
from validation import validate_name, validate_email, validate_phone

st.set_page_config(page_title="Therapist Management", layout="wide")
st.title("🏥 Therapist Management System")

# Navigation Menu
menu = ["Add Therapist", "View Therapists", "Update Therapist", "Delete Therapist", "Search Therapist"]
choice = st.sidebar.selectbox("Navigation", menu)

# ==========================================
# ADD THERAPIST
# ==========================================
if choice == "Add Therapist":
    st.subheader("Add New Therapist")
    
    with st.form("add_form"):
        name = st.text_input("Therapist Name")
        specialization = st.text_input("Specialization")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        submit = st.form_submit_button("Add Therapist")
        
        if submit:
            valid_n, msg_n = validate_name(name)
            valid_p, msg_p = validate_phone(phone)
            valid_e, msg_e = validate_email(email)
            
            if not valid_n: st.error(msg_n)
            elif not specialization.strip(): st.error("Specialization cannot be empty.")
            elif not valid_p: st.error(msg_p)
            elif not valid_e: st.error(msg_e)
            else:
                try:
                    cursor.execute("""
                        INSERT INTO therapists (name, specialization, phone, email) 
                        VALUES (?,?,?,?)
                    """, (name, specialization, phone, email))
                    conn.commit()
                    st.success("Therapist added successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# VIEW THERAPISTS
# ==========================================
elif choice == "View Therapists":
    st.subheader("All Therapists")
    cursor.execute("SELECT * FROM therapists")
    therapists = cursor.fetchall()
    
    if not therapists:
        st.info("No therapists found.")
    else:
        for t in therapists:
            st.markdown(f"**ID:** {t[0]} | **Name:** {t[1]}")
            st.markdown(f"**Specialization:** {t[2]} | **Phone:** {t[3]} | **Email:** {t[4]}")
            st.markdown("---")

# ==========================================
# UPDATE THERAPIST
# ==========================================
elif choice == "Update Therapist":
    st.subheader("Update Therapist Information")
    
    t_id = st.number_input("Enter Therapist ID to Update", min_value=1, step=1)
    cursor.execute("SELECT * FROM therapists WHERE therapist_id = ?", (t_id,))
    therapist = cursor.fetchone()
    
    if therapist:
        with st.form("update_form"):
            new_name = st.text_input("New Name", value=therapist[1])
            new_spec = st.text_input("New Specialization", value=therapist[2])
            new_phone = st.text_input("New Phone Number", value=therapist[3])
            new_email = st.text_input("New Email", value=therapist[4])
            update_submit = st.form_submit_button("Update Therapist")
            
            if update_submit:
                valid_n, msg_n = validate_name(new_name)
                valid_p, msg_p = validate_phone(new_phone)
                valid_e, msg_e = validate_email(new_email)
                
                if not valid_n: st.error(msg_n)
                elif not new_spec.strip(): st.error("Specialization cannot be empty.")
                elif not valid_p: st.error(msg_p)
                elif not valid_e: st.error(msg_e)
                else:
                    try:
                        cursor.execute("""
                            UPDATE therapists 
                            SET name=?, specialization=?, phone=?, email=? 
                            WHERE therapist_id=?
                        """, (new_name, new_spec, new_phone, new_email, t_id))
                        conn.commit()
                        st.success("Therapist updated successfully.")
                    except Exception as e:
                        st.error(f"Error: {e}")
    else:
        st.warning("Therapist not found.")

# ==========================================
# DELETE THERAPIST
# ==========================================
elif choice == "Delete Therapist":
    st.subheader("Delete Therapist")
    
    t_id = st.number_input("Enter Therapist ID to Delete", min_value=1, step=1)
    cursor.execute("SELECT * FROM therapists WHERE therapist_id = ?", (t_id,))
    therapist = cursor.fetchone()
    
    if therapist:
        st.warning(f"Are you sure you want to delete {therapist[1]}?")
        if st.button("Delete Therapist"):
            cursor.execute("DELETE FROM therapists WHERE therapist_id = ?", (t_id,))
            conn.commit()
            st.success("Therapist deleted successfully.")
    else:
        st.warning("Therapist not found.")

# ==========================================
# SEARCH THERAPIST
# ==========================================
elif choice == "Search Therapist":
    st.subheader("Search Therapist")
    
    t_id = st.number_input("Enter Therapist ID to Search", min_value=1, step=1)
    cursor.execute("SELECT * FROM therapists WHERE therapist_id = ?", (t_id,))
    therapist = cursor.fetchone()
    
    if therapist:
        st.success("Therapist Found!")
        st.write(f"**Therapist ID:** {therapist[0]}")
        st.write(f"**Name:** {therapist[1]}")
        st.write(f"**Specialization:** {therapist[2]}")
        st.write(f"**Phone:** {therapist[3]}")
        st.write(f"**Email:** {therapist[4]}")
    else:
        st.warning("Therapist not found.")