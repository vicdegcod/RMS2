# ==========================================================
# REHABILITATION MANAGEMENT SYSTEM
# main.py
# Part 1A
# ==========================================================

import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

# ==========================================================
# IMPORT MODULES
# ==========================================================

from auth import (
    login,
    logout,
    change_password
)

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


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Rehabilitation Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

def load_css():

    try:

        with open("styles.css") as css:

            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        st.warning(
            "styles.css not found. Default Streamlit theme is being used."
        )


load_css()


# ==========================================================
# SESSION STATE
# ==========================================================

if "user" not in st.session_state:

    st.session_state.user = None


if "module" not in st.session_state:

    st.session_state.module = "Dashboard"


if "menu" not in st.session_state:

    st.session_state.menu = "Dashboard"


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def page_header(title, subtitle=""):

    st.markdown(
        f"""
<div class="dashboard-card">

<h1>{title}</h1>

<p>{subtitle}</p>

</div>
""",
        unsafe_allow_html=True
    )


def profile_card(user):

    st.sidebar.markdown(
        f"""
<div class="profile-card">

<h2>👤 {user['username']}</h2>

<p><strong>Role</strong></p>

<p>{user['role']}</p>

</div>
""",
        unsafe_allow_html=True
    )


def footer():

    st.markdown(
        """
<div class="footer">

© 2026 SLIP Rehabilitation Management System

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# DASHBOARD METRICS
# ==========================================================

def dashboard_metrics():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Clients",
            "Manage"
        )

    with col2:
        st.metric(
            "Therapists",
            "Manage"
        )

    with col3:
        st.metric(
            "Appointments",
            "Schedule"
        )

    with col4:
        st.metric(
            "Therapy Notes",
            "Records"
        )


# ==========================================================
# QUICK ACTION BUTTONS
# ==========================================================

def quick_actions():

    st.subheader("Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "➕ Add Client",
            use_container_width=True
        ):
            st.session_state.menu = "Add Client"

    with c2:

        if st.button(
            "📅 Book Appointment",
            use_container_width=True
        ):
            st.session_state.menu = "Book Appointment"

    with c3:

        if st.button(
            "📝 Add Therapy Note",
            use_container_width=True
        ):
            st.session_state.menu = "Add Therapy Note"

    with c4:

        if st.button(
            "📈 View Progress",
            use_container_width=True
        ):
            st.session_state.menu = "View Client Progress"
            # ==========================================================
# LOGIN PAGE
# ==========================================================

if st.session_state.user is None:

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="dashboard-card" style="text-align:center;">
                <h1>🏥 Rehabilitation Management System</h1>
                <p>Secure Login</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        remember_me = st.checkbox("Remember me")

        login_clicked = st.button(
            "🔐 Login",
            use_container_width=True
        )

        if login_clicked:

            username = username.strip()
            password = password.strip()

            if not username:

                st.warning("Please enter your username.")

            elif not password:

                st.warning("Please enter your password.")

            else:

                try:

                    user = login(username, password)

                    if user:

                        st.session_state.user = user

                        if remember_me:
                            st.session_state["remember_me"] = True

                        st.success(
                            f"Welcome {user['username']}!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Invalid username or password."
                        )

                except Exception as e:

                    st.error(
                        f"Login failed: {e}"
                    )

        st.markdown("<br>", unsafe_allow_html=True)

        st.info(
            """
            **Demo Roles**

            • Administrator

            • Therapist
            """
        )

    st.stop()


# ==========================================================
# CURRENT USER
# ==========================================================

user = st.session_state.user


# ==========================================================
# GREETING
# ==========================================================

current_hour = datetime.now().hour

if current_hour < 12:

    greeting = "Good Morning"

elif current_hour < 18:

    greeting = "Good Afternoon"

else:

    greeting = "Good Evening"


st.markdown(
    f"""
<div class="dashboard-card">

<h2>{greeting}, {user['username']} 👋</h2>

<p>Welcome to the Rehabilitation Management System.</p>

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-title">

🏥 Rehabilitation System

</div>
""",
        unsafe_allow_html=True
    )

    profile_card(user)

    st.markdown("---")

    # =====================================================
    # MAIN NAVIGATION
    # =====================================================

    if user["role"] == "Admin":

        module = option_menu(

            menu_title="Navigation",

            options=[
                "Dashboard",
                "Clients",
                "Therapists",
                "Appointments",
                "Therapy Notes",
                "Client Progress",
                "Account"
            ],

            icons=[
                "speedometer2",
                "people",
                "person-badge",
                "calendar-event",
                "journal-medical",
                "graph-up-arrow",
                "gear"
            ],

            menu_icon="list",

            default_index=0,

            styles={

                "container":{
                    "padding":"5px",
                    "background-color":"#0f172a"
                },

                "icon":{
                    "color":"#38bdf8",
                    "font-size":"18px"
                },

                "nav-link":{

                    "font-size":"15px",

                    "text-align":"left",

                    "margin":"3px",

                    "--hover-color":"#1e293b"

                },

                "nav-link-selected":{

                    "background-color":"#2563eb"

                }

            }

        )

    else:

        module = option_menu(

            menu_title="Navigation",

            options=[
                "Dashboard",
                "Clients",
                "Therapists",
                "Appointments",
                "Therapy Notes",
                "Client Progress",
                "Account"
            ],

            icons=[
                "speedometer2",
                "people",
                "person-badge",
                "calendar-event",
                "journal-medical",
                "graph-up-arrow",
                "gear"
            ],

            menu_icon="list",

            default_index=0
        )

st.session_state.module = module

# ==========================================================
# SUB MENUS
# ==========================================================

menu = None

# ----------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------

if module == "Dashboard":

    menu = "Dashboard"

# ----------------------------------------------------------
# CLIENTS
# ----------------------------------------------------------

elif module == "Clients":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Client Management",

            (

                "Add Client",

                "View Clients",

                "Update Client",

                "Delete Client"

            )

        )

    else:

        menu = "View Clients"

# ----------------------------------------------------------
# THERAPISTS
# ----------------------------------------------------------

elif module == "Therapists":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Therapist Management",

            (

                "Add Therapist",

                "View Therapists",

                "Update Therapist",

                "Delete Therapist"

            )

        )

    else:

        menu = "View Therapists"

# ----------------------------------------------------------
# APPOINTMENTS
# ----------------------------------------------------------

elif module == "Appointments":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Appointments",

            (

                "Book Appointment",

                "View Appointments",

                "Cancel Appointment",

                "Complete Appointment",

                "Delete Appointment"

            )

        )

    else:

        menu = st.sidebar.radio(

            "Appointments",

            (

                "Book Appointment",

                "View Appointments",

                "Cancel Appointment",

                "Complete Appointment"

            )

        )

# ----------------------------------------------------------
# NOTES
# ----------------------------------------------------------

elif module == "Therapy Notes":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Therapy Notes",

            (

                "Add Therapy Note",

                "View Therapy Notes",

                "Search Therapy Notes",

                "Update Therapy Note",

                "Delete Therapy Note",

                "Export Therapy Notes",

                "Count Therapy Notes"

            )

        )

    else:

        menu = st.sidebar.radio(

            "Therapy Notes",

            (

                "Add Therapy Note",

                "View Therapy Notes",

                "Search Therapy Notes",

                "Export Therapy Notes",

                "Count Therapy Notes"

            )

        )

# ----------------------------------------------------------
# CLIENT PROGRESS
# ----------------------------------------------------------

elif module == "Client Progress":

    menu = "View Client Progress"

# ----------------------------------------------------------
# ACCOUNT
# ----------------------------------------------------------

elif module == "Account":

    menu = st.sidebar.radio(

        "Account",

        (

            "Change Password",

            "Logout"

        )

    )

# ==========================================================
# PAGE HEADER
# ==========================================================

page_header(

    "🏥 Rehabilitation Management Dashboard",

    f"Logged in as {user['username']} ({user['role']})"

)

# ==========================================================
# PART 2A
# LIVE DASHBOARD
# ==========================================================

from database import cursor

# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

def dashboard_statistics():

    stats = {}

    # ----------------------------
    # Clients
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM clients")

        stats["clients"] = cursor.fetchone()[0]

    except:

        stats["clients"] = 0

    # ----------------------------
    # Therapists
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM therapists")

        stats["therapists"] = cursor.fetchone()[0]

    except:

        stats["therapists"] = 0

    # ----------------------------
    # Appointments
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM appointments")

        stats["appointments"] = cursor.fetchone()[0]

    except:

        stats["appointments"] = 0

    # ----------------------------
    # Therapy Notes
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM therapy_notes")

        stats["notes"] = cursor.fetchone()[0]

    except:

        stats["notes"] = 0

    return stats


# ==========================================================
# DASHBOARD
# ==========================================================

if menu == "Dashboard":

    page_header(
        "🏥 Rehabilitation Dashboard",
        "Welcome to the Rehabilitation Management System"
    )

    stats = dashboard_statistics()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Clients", stats["clients"])

    with c2:
        st.metric("🩺 Therapists", stats["therapists"])

    with c3:
        st.metric("📅 Appointments", stats["appointments"])

    with c4:
        st.metric("📝 Therapy Notes", stats["notes"])

    st.markdown("---")

    dashboard_metrics()

    quick_actions()

elif menu == "Add Client":

    page_header(
        "👥 Add Client",
        "Register a new rehabilitation client."
    )

    add_client()

elif menu == "View Clients":

    page_header(
        "👥 Client Records",
        "View all registered clients."
    )

    view_clients()


elif menu == "Update Client":

    page_header(
        "✏️ Update Client",
        "Edit an existing client."
    )

    update_client()


elif menu == "Delete Client":

    page_header(
        "🗑 Delete Client",
        "Remove a client record."
    )

    delete_client()


# ==========================================================
# THERAPIST MANAGEMENT
# ==========================================================

elif menu == "Add Therapist":

    page_header(
        "🩺 Add Therapist",
        "Register a therapist."
    )

    add_therapist()


elif menu == "View Therapists":

    page_header(
        "🩺 Therapist Records",
        "View registered therapists."
    )

    view_therapists()


elif menu == "Update Therapist":

    page_header(
        "✏️ Update Therapist",
        "Modify therapist information."
    )

    update_therapist()


elif menu == "Delete Therapist":

    page_header(
        "🗑 Delete Therapist",
        "Remove a therapist."
    )

    delete_therapist()


# ==========================================================
# APPOINTMENT MANAGEMENT
# ==========================================================

elif menu == "Book Appointment":

    page_header(
        "📅 Book Appointment",
        "Schedule a rehabilitation session."
    )

    book_appointment()


elif menu == "View Appointments":

    page_header(
        "📅 Appointment Records",
        "View all appointments."
    )

    view_appointments()


elif menu == "Cancel Appointment":

    page_header(
        "❌ Cancel Appointment",
        "Cancel an existing appointment."
    )

    cancel_appointment()


elif menu == "Complete Appointment":

    page_header(
        "✅ Complete Appointment",
        "Mark an appointment as completed."
    )

    complete_appointment()


elif menu == "Delete Appointment":

    page_header(
        "🗑 Delete Appointment",
        "Delete an appointment permanently."
    )

    delete_appointment()


# ==========================================================
# THERAPY NOTES
# ==========================================================

elif menu == "Add Therapy Note":

    page_header(
        "📝 Add Therapy Note",
        "Record a therapy session."
    )

    add_note()


elif menu == "View Therapy Notes":

    page_header(
        "📝 Therapy Notes",
        "View recorded therapy notes."
    )

    view_notes()


elif menu == "Search Therapy Notes":

    page_header(
        "🔍 Search Therapy Notes",
        "Find therapy notes."
    )

    search_notes()


elif menu == "Update Therapy Note":

    page_header(
        "✏️ Update Therapy Note",
        "Edit an existing therapy note."
    )

    update_note()


elif menu == "Delete Therapy Note":

    page_header(
        "🗑 Delete Therapy Note",
        "Remove a therapy note."
    )

    delete_note()


elif menu == "Export Therapy Notes":

    page_header(
        "📤 Export Therapy Notes",
        "Download notes as CSV."
    )

    export_notes_csv()


elif menu == "Count Therapy Notes":

    page_header(
        "📊 Therapy Note Statistics",
        "Display therapy note totals."
    )

    count_notes()


# ==========================================================
# CLIENT PROGRESS
# ==========================================================

elif menu == "View Client Progress":

    page_header(
        "📈 Client Progress",
        "Treatment progress for all clients."
    )

    view_progress()


# ==========================================================
# ACCOUNT
# ==========================================================

elif menu == "Change Password":

    page_header(
        "🔒 Change Password",
        "Update your account password."
    )

    change_password(user)


elif menu == "Logout":

    logout()

    st.success("Logged out successfully.")

    st.rerun()


# ==========================================================
# SIDEBAR FOOTER
# ==========================================================

with st.sidebar:

    st.markdown("---")

    st.caption("🏥 Rehabilitation Management System")

    st.caption("Version 2.0")

    st.caption("© 2026")


# ==========================================================
# PAGE FOOTER
# ==========================================================

footer()


# ==========================================================
# DATABASE CLEANUP
# ==========================================================

try:

    close_database()

except Exception:

    pass
    page_header(

        "🏥 Rehabilitation Dashboard",

        "Welcome to the Rehabilitation Management System"

    )

    stats = dashboard_statistics()

    # ======================================================
    # KPI CARDS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "👥 Clients",

            stats["clients"]

        )

    with c2:

        st.metric(

            "🩺 Therapists",

            stats["therapists"]

        )

    with c3:

        st.metric(

            "📅 Appointments",

            stats["appointments"]

        )

    with c4:

        st.metric(

            "📝 Therapy Notes",

            stats["notes"]

        )

    st.markdown("---")

    # ======================================================
    # QUICK ACTIONS
    # ======================================================

    st.subheader("⚡ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:

        if st.button(

            "➕ Add Client",

            use_container_width=True

        ):

            st.session_state.menu = "Add Client"

            st.rerun()

    with q2:

        if st.button(

            "📅 Book Appointment",

            use_container_width=True

        ):

            st.session_state.menu = "Book Appointment"

            st.rerun()

    with q3:

        if st.button(

            "📝 Add Therapy Note",

            use_container_width=True

        ):

            st.session_state.menu = "Add Therapy Note"

            st.rerun()

    with q4:

        if st.button(

            "📈 View Progress",

            use_container_width=True

        ):

            st.session_state.menu = "View Client Progress"

            st.rerun()

    st.markdown("---")

    # ======================================================
    # SYSTEM OVERVIEW
    # ======================================================

    left, right = st.columns([2, 1])

    with left:

        st.markdown(
            """
### 🏥 System Overview

The Rehabilitation Management System allows you to:

- 👥 Manage rehabilitation clients
- 🩺 Manage therapists
- 📅 Schedule therapy appointments
- 📝 Record therapy notes
- 📈 Track rehabilitation progress
- 🔒 Secure administrator and therapist access
"""
        )

    with right:

        st.info(

            f"""
### Logged-in User

**Username**

{user['username']}

**Role**

{user['role']}
"""

        )

    st.markdown("---")

    st.success("✅ System is ready.")

    # ==========================================================
# DASHBOARD CHARTS & RECENT ACTIVITY
# ==========================================================

st.subheader("📊 Dashboard Analytics")

left, right = st.columns(2)

# ======================================================
# CLIENT GENDER DISTRIBUTION
# ======================================================

with left:

    try:

        gender_df = pd.read_sql_query(
            """
            SELECT gender,
                   COUNT(*) AS total
            FROM clients
            GROUP BY gender
            """,
            conn
        )

        if not gender_df.empty:

            fig = px.pie(
                gender_df,
                names="gender",
                values="total",
                title="Client Gender Distribution",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No client records available.")

    except Exception as e:

        st.warning(f"Unable to load gender chart.\n\n{e}")


# ======================================================
# APPOINTMENT STATUS
# ======================================================

with right:

    try:

        status_df = pd.read_sql_query(
            """
            SELECT status,
                   COUNT(*) AS total
            FROM appointments
            GROUP BY status
            """,
            conn
        )

        if not status_df.empty:

            fig = px.bar(
                status_df,
                x="status",
                y="total",
                title="Appointment Status"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No appointments available.")

    except Exception as e:

        st.warning(f"Unable to load appointment chart.\n\n{e}")

st.markdown("---")

# ======================================================
# RECENT APPOINTMENTS
# ======================================================

left, right = st.columns([2, 1])

with left:

    st.subheader("📅 Upcoming Appointments")

    try:

        appointments_df = pd.read_sql_query(
            """
            SELECT

                a.appointment_id,

                c.name AS Client,

                t.name AS Therapist,

                a.appointment_date,

                a.status

            FROM appointments a

            INNER JOIN clients c

            ON a.client_id=c.client_id

            INNER JOIN therapists t

            ON a.therapist_id=t.therapist_id

            ORDER BY a.appointment_date ASC

            LIMIT 10
            """,
            conn
        )

        if appointments_df.empty:

            st.info("No appointments scheduled.")

        else:

            st.dataframe(
                appointments_df,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:

        st.error(e)


# ======================================================
# RECENT THERAPY NOTES
# ======================================================

with right:

    st.subheader("📝 Recent Notes")

    try:

        notes_df = pd.read_sql_query(
            """
            SELECT

                c.name,

                session_date

            FROM therapy_notes n

            INNER JOIN clients c

            ON n.client_id=c.client_id

            ORDER BY session_date DESC

            LIMIT 5
            """,
            conn
        )

        if notes_df.empty:

            st.info("No therapy notes.")

        else:

            st.dataframe(
                notes_df,
                hide_index=True,
                use_container_width=True
            )

    except Exception as e:

        st.error(e)

st.markdown("---")

# ======================================================
# CLIENT RECOVERY PROGRESS
# ======================================================

st.subheader("📈 Client Recovery Progress")

try:

    progress_df = pd.read_sql_query(
        """
        SELECT

            name,

            completed_sessions,

            total_sessions

        FROM clients
        """,
        conn
    )

    if progress_df.empty:

        st.info("No clients available.")

    else:

        progress_df["Progress (%)"] = (
            progress_df["completed_sessions"]
            /
            progress_df["total_sessions"].replace(0, 1)
        ) * 100

        fig = px.bar(

            progress_df,

            x="name",

            y="Progress (%)",

            title="Treatment Progress",

            text="Progress (%)"

        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        

except Exception as e:

    st.error(e)

st.markdown("---")

