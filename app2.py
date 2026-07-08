import streamlit as st

st.set_page_config(
    page_title="Rehabilitation Management System",
    layout="wide"
)

from auth import login, logout, change_password
from client import (
    add_client, view_clients, update_client,
    delete_client, view_progress
)
from therapist import (
    add_therapist, view_therapists,
    update_therapist, delete_therapist
)
from appointment import (
    book_appointment, view_appointments,
    cancel_appointment, complete_appointment,
    delete_appointment
)
from notes import (
    add_note, view_notes, search_notes,
    update_note, delete_note,
    export_notes_csv, count_notes
)
from database import close_database