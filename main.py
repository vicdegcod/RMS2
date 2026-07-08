import streamlit as st
import streamlit_shadcn_ui as ui

from auth import login, logout, change_password

from client import (
    add_client,
    view_clients,
    update_client,
    delete_client,
    view_progress
)

from therapist import (
    add_therapist,
    view_therapists,
    update_therapist,
    delete_therapist
)

from appointment import (
    book_appointment,
    view_appointments,
    cancel_appointment,
    complete_appointment,
    delete_appointment
)

from notes import (
    add_note,
    view_notes,
    search_notes,
    update_note,
    delete_note,
    export_notes_csv,
    count_notes
)

from database import close_database

# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Rehabilitation Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# SHADCN + DARK THEME
# ======================================================

st.markdown("""
<style>
#MainMenu,header,footer{
visibility:hidden;
}

.stApp{
background:#020817;
color:white;
}

section[data-testid="stSidebar"]{
background:#0f172a;
border-right:1px solid #1e293b;
}

.block-container{
padding-top:1.5rem;
padding-bottom:1rem;
}

h1,h2,h3{
color:#38bdf8;
}

[data-testid="stMetric"]{
background:#111827;
padding:1rem;
border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================

if "user" not in st.session_state:
    st.session_state.user = None

def page_title(title: str, subtitle: str = ""):
    ui.card(
        title=title,
        content=subtitle,
        key=f"card_{title}"
    )

# ======================================================
# LOGIN PAGE (SHADCN UI)
# ======================================================

if st.session_state.user is None:

    left, center, right = st.columns([1, 1.3, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        ui.card(
            title="🏥 Rehabilitation Management System",
            content="Secure Login",
            key="login_card"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        login_btn = ui.button(
            text="🔐 Login",
            key="login_button"
        )

        if login_btn:

            if username.strip() == "" or password.strip() == "":

                st.error("Please enter both username and password.")

            else:

                user = login(username, password)

                if user:

                    st.session_state.user = user

                    st.success("Login successful.")

                    st.rerun()

                else:

                    st.error("Invalid username or password.")

        st.markdown("<br>", unsafe_allow_html=True)

        ui.badges(
            badge_list=[
                ("Secure Authentication", "secondary"),
                ("Admin", "default"),
                ("Therapist", "outline"),
            ],
            class_name="flex gap-2",
            key="login_badges"
        )

    st.stop()


# ======================================================
# LOGGED-IN USER
# ======================================================

user = st.session_state.user

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown("## 🏥 Rehabilitation System")

    ui.card(
        title=f"👤 {user['username']}",
        content=f"Role: {user['role']}",
        key="profile_card"
    )

    ui.badges(
        badge_list=[
            (user["role"], "secondary")
        ],
        class_name="flex gap-2",
        key="role_badge"
    )

    st.divider()

    # ==========================================
    # MAIN MODULES
    # ==========================================

    module = ui.tabs(
        options=[
            "Dashboard",
            "Clients",
            "Therapists",
            "Appointments",
            "Therapy Notes",
            "Client Progress",
            "Account"
        ],
        default_value="Dashboard",
        key="module_tabs"
    )

menu = None

# ======================================================
# ADMIN MENU
# ======================================================

if user["role"] == "Admin":

    if module == "Dashboard":
        menu = "Dashboard"

    elif module == "Clients":

        menu = st.radio(
            "Client Management",
            [
                "Add Client",
                "View Clients",
                "Update Client",
                "Delete Client"
            ]
        )

    elif module == "Therapists":

        menu = st.radio(
            "Therapist Management",
            [
                "Add Therapist",
                "View Therapists",
                "Update Therapist",
                "Delete Therapist"
            ]
        )

    elif module == "Appointments":

        menu = st.radio(
            "Appointment Management",
            [
                "Book Appointment",
                "View Appointments",
                "Cancel Appointment",
                "Complete Appointment",
                "Delete Appointment"
            ]
        )

    elif module == "Therapy Notes":

        menu = st.radio(
            "Therapy Notes",
            [
                "Add Therapy Note",
                "View Therapy Notes",
                "Search Therapy Notes",
                "Update Therapy Note",
                "Delete Therapy Note",
                "Export Therapy Notes",
                "Count Therapy Notes"
            ]
        )

    elif module == "Client Progress":

        menu = "View Client Progress"

    elif module == "Account":

        menu = st.radio(
            "Account",
            [
                "Change Password",
                "Logout"
            ]
        )

# ======================================================
# THERAPIST MENU
# ======================================================

else:

    if module == "Dashboard":
        menu = "Dashboard"

    elif module == "Clients":

        menu = "View Clients"

    elif module == "Therapists":

        menu = "View Therapists"

    elif module == "Appointments":

        menu = st.radio(
            "Appointments",
            [
                "Book Appointment",
                "View Appointments",
                "Cancel Appointment",
                "Complete Appointment"
            ]
        )

    elif module == "Therapy Notes":

        menu = st.radio(
            "Therapy Notes",
            [
                "Add Therapy Note",
                "View Therapy Notes",
                "Search Therapy Notes",
                "Export Therapy Notes",
                "Count Therapy Notes"
            ]
        )

    elif module == "Client Progress":

        menu = "View Client Progress"

    elif module == "Account":

        menu = st.radio(
            "Account",
            [
                "Change Password",
                "Logout"
            ]
        )

# ======================================================
# PAGE HEADER
# ======================================================

page_title(
    "🏥 Rehabilitation Management Dashboard",
    "Manage clients, therapists, appointments, therapy notes, and rehabilitation progress."
)

st.markdown("")

# ======================================================
# SHADCN DASHBOARD
# ======================================================

if menu == "Dashboard":

    page_title(
        "🏥 Rehabilitation Dashboard",
        "Welcome to the Rehabilitation Management System"
    )

    st.write("")

    # =====================================================
    # METRIC CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        ui.metric_card(
            title="Clients",
            content="Manage",
            description="Client Records",
            key="metric_clients"
        )

    with c2:
        ui.metric_card(
            title="Therapists",
            content="Manage",
            description="Staff",
            key="metric_therapists"
        )

    with c3:
        ui.metric_card(
            title="Appointments",
            content="Schedule",
            description="Therapy Visits",
            key="metric_appointments"
        )

    with c4:
        ui.metric_card(
            title="Therapy Notes",
            content="Records",
            description="Clinical Notes",
            key="metric_notes"
        )

    st.write("")

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    ui.card(
        title="⚡ Quick Actions",
        content="Choose a commonly used task below.",
        key="quick_actions_title"
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:

        if ui.button(
            text="➕ Add Client",
            key="quick_add_client"
        ):
            menu = "Add Client"

    with q2:

        if ui.button(
            text="📅 Book Appointment",
            key="quick_book"
        ):
            menu = "Book Appointment"

    with q3:

        if ui.button(
            text="📝 Add Therapy Note",
            key="quick_note"
        ):
            menu = "Add Therapy Note"

    with q4:

        if ui.button(
            text="📈 Client Progress",
            key="quick_progress"
        ):
            menu = "View Client Progress"

    st.divider()

    # =====================================================
    # DASHBOARD CONTENT
    # =====================================================

    left, right = st.columns([2, 1])

    with left:

        ui.card(
            title="🏥 System Overview",
            content="""
• Manage rehabilitation clients

• Register therapists

• Book therapy appointments

• Record therapy session notes

• Monitor treatment progress

• Export reports

• Secure role-based access
""",
            key="overview_card"
        )

    with right:

        ui.card(
            title="👤 Logged-in User",
            content=f"""
Username

{user['username']}

-------------------

Role

{user['role']}
""",
            key="logged_user_card"
        )

        ui.badges(
            badge_list=[
                ("System Online", "default"),
                (user["role"], "secondary")
            ],
            class_name="flex gap-2",
            key="dashboard_badges"
        )

    st.divider()

    # =====================================================
    # MODULES
    # =====================================================

    st.subheader("System Modules")

    m1, m2 = st.columns(2)

    with m1:

        ui.card(
            title="👥 Client Management",
            content="""
• Add Clients

• Update Clients

• Delete Clients

• Search Records

• Track Recovery
""",
            key="clients_module"
        )

        ui.card(
            title="🩺 Therapist Management",
            content="""
• Register Therapists

• Update Details

• Remove Therapists

• View Therapist List
""",
            key="therapist_module"
        )

    with m2:

        ui.card(
            title="📅 Appointment Management",
            content="""
• Book Sessions

• View Schedule

• Cancel Visits

• Complete Sessions
""",
            key="appointment_module"
        )

        ui.card(
            title="📝 Therapy Notes",
            content="""
• Add Notes

• Search Notes

• Export CSV

• Statistics
""",
            key="notes_module"
        )

    st.divider()

    # =====================================================
    # STATUS
    # =====================================================

    ui.alert_dialog(
        show=False,
        title="System Status",
        description="All services are operating normally.",
        confirm_label="OK",
        key="system_status"
    )

    st.success("✅ Rehabilitation Management System is ready.")

    # ======================================================
# CLIENT MANAGEMENT
# ======================================================

elif menu == "Add Client":

    page_title(
        "👥 Add Client",
        "Register a new rehabilitation client."
    )

    ui.card(
        title="Client Registration",
        content="Fill in the client's details below.",
        key="client_add_card"
    )

    add_client()


elif menu == "View Clients":

    page_title(
        "👥 Client Records",
        "View all registered rehabilitation clients."
    )

    ui.card(
        title="Registered Clients",
        content="Search and review client information.",
        key="view_clients_card"
    )

    view_clients()


elif menu == "Update Client":

    page_title(
        "✏ Update Client",
        "Edit an existing client record."
    )

    ui.card(
        title="Update Client",
        content="Modify client details and save the changes.",
        key="update_client_card"
    )

    update_client()


elif menu == "Delete Client":

    page_title(
        "🗑 Delete Client",
        "Remove a client from the system."
    )

    ui.card(
        title="Delete Client",
        content="Deleted records cannot be recovered.",
        key="delete_client_card"
    )

    delete_client()


# ======================================================
# THERAPIST MANAGEMENT
# ======================================================

elif menu == "Add Therapist":

    page_title(
        "🩺 Add Therapist",
        "Register a therapist."
    )

    ui.card(
        title="Therapist Registration",
        content="Enter therapist information.",
        key="add_therapist_card"
    )

    add_therapist()


elif menu == "View Therapists":

    page_title(
        "🩺 Therapist Records",
        "View therapist information."
    )

    ui.card(
        title="Registered Therapists",
        content="Browse therapist profiles.",
        key="view_therapists_card"
    )

    view_therapists()


elif menu == "Update Therapist":

    page_title(
        "✏ Update Therapist",
        "Modify therapist information."
    )

    ui.card(
        title="Update Therapist",
        content="Edit therapist details.",
        key="update_therapist_card"
    )

    update_therapist()


elif menu == "Delete Therapist":

    page_title(
        "🗑 Delete Therapist",
        "Remove a therapist."
    )

    ui.card(
        title="Delete Therapist",
        content="This action permanently removes the selected therapist.",
        key="delete_therapist_card"
    )

    delete_therapist()


# ======================================================
# APPOINTMENT MANAGEMENT
# ======================================================

elif menu == "Book Appointment":

    page_title(
        "📅 Book Appointment",
        "Schedule a therapy session."
    )

    ui.card(
        title="Appointment Scheduler",
        content="Select a client, therapist, date and time.",
        key="book_appointment_card"
    )

    book_appointment()


elif menu == "View Appointments":

    page_title(
        "📅 Appointment Records",
        "View scheduled therapy sessions."
    )

    ui.card(
        title="Appointments",
        content="Upcoming and completed appointments.",
        key="view_appointments_card"
    )

    view_appointments()


elif menu == "Cancel Appointment":

    page_title(
        "❌ Cancel Appointment",
        "Cancel a scheduled therapy appointment."
    )

    ui.card(
        title="Cancel Appointment",
        content="Choose an appointment to cancel.",
        key="cancel_appointment_card"
    )

    cancel_appointment()


elif menu == "Complete Appointment":

    page_title(
        "✅ Complete Appointment",
        "Mark a therapy session as completed."
    )

    ui.card(
        title="Complete Appointment",
        content="Update the appointment status.",
        key="complete_appointment_card"
    )

    complete_appointment()


elif menu == "Delete Appointment":

    page_title(
        "🗑 Delete Appointment",
        "Permanently remove an appointment."
    )

    ui.card(
        title="Delete Appointment",
        content="Deleted appointments cannot be recovered.",
        key="delete_appointment_card"
    )

    delete_appointment()

    # ======================================================
# THERAPY NOTES
# ======================================================

elif menu == "Add Therapy Note":

    page_title(
        "📝 Add Therapy Note",
        "Record therapy session notes."
    )

    add_note()


elif menu == "View Therapy Notes":

    page_title(
        "📝 Therapy Notes",
        "View all therapy notes."
    )

    view_notes()


elif menu == "Search Therapy Notes":

    page_title(
        "🔍 Search Therapy Notes",
        "Search therapy notes by client or keyword."
    )

    search_notes()


elif menu == "Update Therapy Note":

    page_title(
        "✏ Update Therapy Note",
        "Edit an existing therapy note."
    )

    update_note()


elif menu == "Delete Therapy Note":

    page_title(
        "🗑 Delete Therapy Note",
        "Remove a therapy note."
    )

    delete_note()


elif menu == "Export Therapy Notes":

    page_title(
        "📤 Export Therapy Notes",
        "Download therapy notes as CSV."
    )

    export_notes_csv()


elif menu == "Count Therapy Notes":

    page_title(
        "📊 Therapy Note Statistics",
        "Display note totals."
    )

    count_notes()


# ======================================================
# CLIENT PROGRESS
# ======================================================

elif menu == "View Client Progress":

    page_title(
        "📈 Client Progress",
        "Monitor rehabilitation progress."
    )

    view_progress()


# ======================================================
# ACCOUNT
# ======================================================

elif menu == "Change Password":

    page_title(
        "🔒 Change Password",
        "Update your account password."
    )

    change_password(user)


elif menu == "Logout":

    logout()

    st.session_state.user = None

    st.success("Logged out successfully.")

    st.rerun()


# ======================================================
# SIDEBAR FOOTER
# ======================================================

with st.sidebar:

    st.divider()

    st.caption("🏥 Rehabilitation Management System")

    st.caption("Version 2.0")

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="sidebar_logout"
    ):

        logout()

        st.session_state.user = None

        st.rerun()


# ======================================================
# PAGE FOOTER
# ======================================================

st.divider()

st.markdown(
    """
<div style="text-align:center;
padding:15px;
color:#94a3b8;">

© 2026 SLIP Rehabilitation Management System

</div>
""",
    unsafe_allow_html=True
)


# ======================================================
# CLOSE DATABASE CONNECTION
# ======================================================

try:

    close_database()

except Exception:

    pass