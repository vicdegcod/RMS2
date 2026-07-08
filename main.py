import streamlit as st

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


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SLIP Rehabilitation Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY = "#3B82F6"
SECONDARY = "#06B6D4"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
CARD = "#182338"
BG = "#0B1220"
TEXT = "#F8FAFC"

# ==========================================================
# PREMIUM CSS (PART 1)
# ==========================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*{
    font-family:'Inter',sans-serif;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.stApp{

background:
radial-gradient(circle at top left,#1d4ed8 0%,transparent 35%),
radial-gradient(circle at bottom right,#0891b2 0%,transparent 35%),
#08111f;

color:white;

}

section[data-testid="stSidebar"]{

background:#111827;

border-right:1px solid rgba(255,255,255,.08);

}

section[data-testid="stSidebar"]>div{

padding-top:1rem;

}

h1{

font-size:40px;

font-weight:800;

color:white;

}

h2{

font-size:30px;

font-weight:700;

color:white;

}

h3{

font-size:24px;

font-weight:700;

color:white;

}

p,label{

color:#d1d5db;

}

div[data-testid="stMetric"]{

background:rgba(255,255,255,.05);

border:1px solid rgba(255,255,255,.08);

border-radius:18px;

padding:20px;

backdrop-filter:blur(16px);

}

div[data-testid="metric-container"]{

background:rgba(255,255,255,.05);

border-radius:18px;

padding:18px;

border:1px solid rgba(255,255,255,.08);

}

.stButton>button{

width:100%;

height:48px;

border:none;

border-radius:14px;

background:linear-gradient(
135deg,
#2563eb,
#06b6d4
);

color:white;

font-weight:700;

font-size:15px;

transition:.3s;

}

.stButton>button:hover{

transform:translateY(-3px);

box-shadow:0 12px 25px rgba(37,99,235,.35);

}

.stTextInput input,
.stNumberInput input{

background:#162235;

color:white;

border-radius:12px;

border:1px solid rgba(255,255,255,.08);

}

.stSelectbox div[data-baseweb="select"]{

background:#162235;

border-radius:12px;

}

textarea{

background:#162235 !important;

color:white !important;

}

hr{

border:1px solid rgba(255,255,255,.08);

}



/* ==========================================================
   GLASS CARDS
========================================================== */

.glass-card{

    background:rgba(255,255,255,.05);

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:24px;

    margin-bottom:20px;

    box-shadow:0 10px 30px rgba(0,0,0,.25);

}

.hero-card{

    background:linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );

    border-radius:24px;

    padding:35px;

    color:white;

    box-shadow:0 18px 45px rgba(37,99,235,.35);

    margin-bottom:25px;

}

.hero-title{

    font-size:38px;

    font-weight:800;

    margin-bottom:8px;

}

.hero-subtitle{

    font-size:18px;

    opacity:.95;

}

.metric-card{

    background:rgba(255,255,255,.05);

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:22px;

    text-align:center;

    transition:.35s;

}

.metric-card:hover{

    transform:translateY(-6px);

    border:1px solid #3b82f6;

    box-shadow:0 15px 35px rgba(59,130,246,.25);

}

.metric-number{

    font-size:34px;

    font-weight:800;

    color:white;

}

.metric-label{

    color:#cbd5e1;

    font-size:15px;

}

.profile-card{

    background:linear-gradient(
        180deg,
        #1e293b,
        #0f172a
    );

    border-radius:18px;

    padding:22px;

    text-align:center;

    border:1px solid rgba(255,255,255,.08);

    margin-bottom:18px;

}

.profile-avatar{

    width:72px;

    height:72px;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

    margin:auto;

    margin-bottom:14px;

    font-size:34px;

    background:linear-gradient(
        135deg,
        #3b82f6,
        #06b6d4
    );

}

.sidebar-title{

    font-size:28px;

    font-weight:800;

    color:white;

    text-align:center;

    margin-bottom:15px;

}

/* ==========================================================
   BADGES
========================================================== */

.badge-success{

    display:inline-block;

    padding:6px 14px;

    border-radius:30px;

    background:#065f46;

    color:#6ee7b7;

    font-weight:700;

}

.badge-warning{

    display:inline-block;

    padding:6px 14px;

    border-radius:30px;

    background:#78350f;

    color:#fcd34d;

    font-weight:700;

}

.badge-danger{

    display:inline-block;

    padding:6px 14px;

    border-radius:30px;

    background:#7f1d1d;

    color:#fca5a5;

    font-weight:700;

}

/* ==========================================================
   TABLES
========================================================== */

thead tr th{

    background:#172554 !important;

    color:white !important;

    font-size:15px;

}

tbody td{

    background:rgba(255,255,255,.02);

    color:white;

}

/* ==========================================================
   ALERTS
========================================================== */

.stSuccess{

    border-radius:15px;

    border-left:5px solid #10b981;

}

.stError{

    border-radius:15px;

    border-left:5px solid #ef4444;

}

.stWarning{

    border-radius:15px;

    border-left:5px solid #f59e0b;

}

.stInfo{

    border-radius:15px;

    border-left:5px solid #3b82f6;

}

/* ==========================================================
   EXPANDERS
========================================================== */

.streamlit-expanderHeader{

    font-weight:700;

    color:white;

}

div[data-testid="stExpander"]{

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

    overflow:hidden;

}

/* ==========================================================
   TABS
========================================================== */

button[data-baseweb="tab"]{

    border-radius:12px;

    font-weight:700;

}

button[data-baseweb="tab"][aria-selected="true"]{

    background:#2563eb;

    color:white;

}

/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-track{

    background:#111827;

}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:10px;

}

::-webkit-scrollbar-thumb:hover{

    background:#475569;

}

/* ==========================================================
   ANIMATIONS
========================================================== */

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(18px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}

.fade-in{

    animation:fadeIn .6s ease;

}

@keyframes floatCard{

    0%{

        transform:translateY(0px);

    }

    50%{

        transform:translateY(-5px);

    }

    100%{

        transform:translateY(0px);

    }

}

.float{

    animation:floatCard 4s ease-in-out infinite;

}

</style>
""",
unsafe_allow_html=True
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "page_title" not in st.session_state:
    st.session_state.page_title = "Dashboard"

if "notifications" not in st.session_state:
    st.session_state.notifications = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"


# ==========================================================
# UI COMPONENTS
# ==========================================================

def hero_banner(title: str, subtitle: str):
    """
    Beautiful gradient banner shown at the top of every page.
    """

    st.markdown(
        f"""
        <div class="hero-card fade-in">

            <div class="hero-title">
                {title}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def page_header(title: str, subtitle: str = ""):

    hero_banner(title, subtitle)


def glass_card(title: str, body: str):

    st.markdown(
        f"""
        <div class="glass-card fade-in">

        <h3>{title}</h3>

        <p>{body}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


def profile_card(username: str, role: str):

    icon = "👨‍⚕️" if role.lower() == "therapist" else "👨‍💼"

    st.sidebar.markdown(
        f"""
        <div class="profile-card">

            <div class="profile-avatar">
                {icon}
            </div>

            <h3>{username}</h3>

            <p>{role}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(title, value, icon):

    st.markdown(
        f"""
        <div class="metric-card float">

            <div style="font-size:40px;">
                {icon}
            </div>

            <div class="metric-number">
                {value}
            </div>

            <div class="metric-label">
                {title}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(title, text):

    st.markdown(
        f"""
        <div class="glass-card">

            <h3>{title}</h3>

            <p>{text}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


def status_badge(status):

    status = str(status).lower()

    if status in ["completed", "active", "success"]:

        badge = "badge-success"

    elif status in ["pending", "waiting", "scheduled"]:

        badge = "badge-warning"

    else:

        badge = "badge-danger"

    st.markdown(
        f"""
        <span class="{badge}">
            {status.title()}
        </span>
        """,
        unsafe_allow_html=True
    )


def section_title(title):

    st.markdown(
        f"""
        <h2 style="
            color:white;
            margin-top:10px;
            margin-bottom:15px;
        ">
            {title}
        </h2>
        """,
        unsafe_allow_html=True
    )


def horizontal_space():

    st.markdown("<br>", unsafe_allow_html=True)


def dashboard_metrics():

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Clients",
            "Manage",
            "👥"
        )

    with c2:
        metric_card(
            "Therapists",
            "Manage",
            "🩺"
        )

    with c3:
        metric_card(
            "Appointments",
            "Schedule",
            "📅"
        )

    with c4:
        metric_card(
            "Therapy Notes",
            "Records",
            "📝"
        )


def dashboard_welcome(user):

    hero_banner(
        "🏥 Rehabilitation Management System",
        "Secure, Modern and Intelligent Patient Rehabilitation Platform"
    )

    dashboard_metrics()

    horizontal_space()

    left, right = st.columns([2, 1])

    with left:

        info_card(
            "System Overview",
            """
Manage rehabilitation clients, therapists,
appointments, therapy notes and treatment
progress using a modern professional dashboard.
            """
        )

    with right:

        info_card(
            "Current User",
            f"""
Username

{user['username']}

Role

{user['role']}
            """
        )


# ==========================================================
# SIDEBAR COMPONENTS
# ==========================================================

def sidebar_logo():

    st.sidebar.markdown(
        """
        <div class="sidebar-title">

        🏥 SLIP REHAB

        </div>
        """,
        unsafe_allow_html=True
    )


def sidebar_footer():

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
        <div style="text-align:center;">

        <h4 style="color:#3b82f6;">
        Rehabilitation System
        </h4>

        <p style="font-size:12px;color:#94a3b8;">

        Version 2.0

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# END OF PART 1A-3
# ==========================================================

