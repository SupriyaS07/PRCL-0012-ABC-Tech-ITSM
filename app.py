import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="ABC Tech ITSM | ML Dashboard",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FLASK_URL = "http://127.0.0.1:5000"

# ── Background images (free Unsplash IT/tech themed) ──
BG_IMAGES = {
    "login"  : "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80",  # server room
    "home"   : "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80",  # data center
    "uc1"    : "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1920&q=80",  # alert monitor
    "uc2"    : "https://images.unsplash.com/photo-1526628953301-3cd68b5e7d41?w=1920&q=80",  # analytics
    "uc3"    : "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1920&q=80",  # network
}

def set_background(page="login"):
    url = BG_IMAGES.get(page, BG_IMAGES["login"])
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(8, 8, 20, 0.82);
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# ── Global CSS ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; position: relative; z-index: 1; }

/* ── GLASS ── */
.glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
}

/* ── NAVBAR ── */
.navbar {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 12px 24px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 24px;
    position: relative; z-index: 10;
}

.navbar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #b478ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.3px;
}

.navbar-badge {
    background: linear-gradient(135deg, rgba(120,80,255,0.35), rgba(40,120,255,0.35));
    border: 1px solid rgba(120,80,255,0.5);
    color: rgba(255,255,255,0.85);
    padding: 5px 14px; border-radius: 20px;
    font-size: 0.76rem; letter-spacing: 1.5px; text-transform: uppercase;
}

.user-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #7850ff, #4080ff);
    border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: white;
    border: 2px solid rgba(255,255,255,0.2);
}

/* ── KPI CARDS ── */
.kpi-glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 24px 20px; text-align: center;
    position: relative; overflow: hidden;
    transition: all 0.3s ease;
}

.kpi-glass:hover {
    background: rgba(255,255,255,0.09);
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
}

.kpi-glass::after {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    border-radius: 0 0 18px 18px;
}

.kpi-glass.blue::after   { background: linear-gradient(90deg, #4080ff, #80b0ff); }
.kpi-glass.purple::after { background: linear-gradient(90deg, #7850ff, #b478ff); }
.kpi-glass.pink::after   { background: linear-gradient(90deg, #ff4080, #ff80a0); }
.kpi-glass.green::after  { background: linear-gradient(90deg, #20c070, #60e0a0); }
.kpi-glass.orange::after { background: linear-gradient(90deg, #ff8040, #ffb080); }

.kpi-emoji { font-size: 1.6rem; margin-bottom: 8px; }

.kpi-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: #ffffff; line-height: 1; margin-bottom: 5px;
}

.kpi-label {
    color: rgba(255,255,255,0.4);
    font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase;
}

/* ── PAGE TITLES ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.5px;
    margin-bottom: 4px; line-height: 1.2;
}

.page-sub {
    color: rgba(255,255,255,0.38);
    font-size: 0.86rem; letter-spacing: 1px; margin-bottom: 24px;
}

.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem; font-weight: 700;
    color: rgba(255,255,255,0.35);
    letter-spacing: 3px; text-transform: uppercase;
    margin: 24px 0 12px 0;
}

/* ── UC CARDS ── */
.uc-glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px; padding: 24px; height: 100%;
    transition: all 0.3s ease;
}

.uc-glass:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.15);
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.uc-tag {
    display: inline-block;
    padding: 3px 10px; border-radius: 20px;
    font-size: 0.68rem; letter-spacing: 1.5px;
    text-transform: uppercase; font-weight: 600; margin-bottom: 12px;
}

.uc-tag.red   { background: rgba(255,60,100,0.15); color: #ff6080; border: 1px solid rgba(255,60,100,0.3); }
.uc-tag.blue  { background: rgba(40,120,255,0.15); color: #60a0ff; border: 1px solid rgba(40,120,255,0.3); }
.uc-tag.green { background: rgba(30,180,100,0.15); color: #50d090; border: 1px solid rgba(30,180,100,0.3); }

.uc-metric {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem; font-weight: 800; margin-bottom: 6px; line-height: 1;
}

.uc-desc { color: rgba(255,255,255,0.42); font-size: 0.82rem; line-height: 1.7; }

/* ── USER WELCOME CARD ── */
.welcome-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 28px;
    position: relative; overflow: hidden;
    margin-bottom: 24px;
}

.welcome-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #7850ff, #4080ff, #b478ff);
}

.welcome-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem; font-weight: 800;
    color: #ffffff; margin-bottom: 4px;
}

.welcome-role {
    color: rgba(255,255,255,0.4);
    font-size: 0.82rem; letter-spacing: 1px; text-transform: uppercase;
}

.welcome-meta {
    display: flex; gap: 20px; margin-top: 16px; flex-wrap: wrap;
}

.meta-pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 5px 14px;
    color: rgba(255,255,255,0.6); font-size: 0.78rem;
    display: flex; align-items: center; gap: 6px;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    backdrop-filter: blur(10px) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(120,80,255,0.7) !important;
    box-shadow: 0 0 0 3px rgba(120,80,255,0.18) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: #ffffff !important;
    backdrop-filter: blur(10px) !important;
}

.stTextInput label, .stSelectbox label,
.stNumberInput label, .stSlider label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.8rem !important; font-family: 'DM Sans', sans-serif !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #7850ff 0%, #4080ff 100%) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.86rem !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    border: none !important; border-radius: 12px !important;
    padding: 13px 24px !important; width: 100% !important;
    box-shadow: 0 8px 24px rgba(120,80,255,0.35) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 16px 40px rgba(120,80,255,0.55) !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(8,8,20,0.88) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.65) !important;
    font-size: 0.84rem !important; letter-spacing: 0.3px !important;
    text-transform: none !important; box-shadow: none !important;
    text-align: left !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(120,80,255,0.18) !important;
    border-color: rgba(120,80,255,0.35) !important;
    color: #ffffff !important;
    transform: none !important; box-shadow: none !important;
}

/* ── STATUS ── */
.status-ok {
    background: rgba(30,180,100,0.1);
    border: 1px solid rgba(30,180,100,0.28);
    border-radius: 10px; padding: 10px 16px;
    color: #50d090; font-size: 0.82rem; margin-bottom: 16px;
}

.status-fail {
    background: rgba(255,60,80,0.1);
    border: 1px solid rgba(255,60,80,0.28);
    border-radius: 10px; padding: 10px 16px;
    color: #ff8090; font-size: 0.82rem; margin-bottom: 16px;
}

/* ── RESULT CARDS ── */
.result-card {
    border-radius: 18px; padding: 32px;
    text-align: center; margin: 16px 0; backdrop-filter: blur(20px);
}

.result-card.danger  { background: rgba(255,40,80,0.09); border: 1px solid rgba(255,40,80,0.22); box-shadow: 0 0 60px rgba(255,40,80,0.08); }
.result-card.success { background: rgba(30,180,100,0.09); border: 1px solid rgba(30,180,100,0.22); box-shadow: 0 0 60px rgba(30,180,100,0.08); }

.result-emoji { font-size: 3rem; margin-bottom: 12px; }
.result-label { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; margin-bottom: 6px; }
.result-label.danger  { color: #ff6080; }
.result-label.success { color: #50d090; }
.result-sub { color: rgba(255,255,255,0.45); font-size: 0.84rem; margin-bottom: 14px; }
.result-confidence {
    display: inline-block;
    background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.13);
    border-radius: 20px; padding: 5px 16px;
    color: rgba(255,255,255,0.65); font-size: 0.82rem; letter-spacing: 1px;
}

/* ── PRIORITY RESULT ── */
.priority-result { border-radius: 18px; padding: 32px; text-align: center; margin: 16px 0; backdrop-filter: blur(20px); }
.priority-result.p2 { background: rgba(255,40,80,0.09); border: 1px solid rgba(255,40,80,0.22); }
.priority-result.p3 { background: rgba(255,140,40,0.09); border: 1px solid rgba(255,140,40,0.22); }
.priority-result.p4 { background: rgba(40,120,255,0.09); border: 1px solid rgba(40,120,255,0.22); }
.priority-result.p5 { background: rgba(30,180,100,0.09); border: 1px solid rgba(30,180,100,0.22); }

/* ── INFO PANEL ── */
.info-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 18px; margin-top: 14px;
}

.info-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.5); font-size: 0.82rem;
}

.info-row:last-child { border-bottom: none; }
.info-val { color: #ffffff; font-weight: 600; font-family: 'Syne', sans-serif; }

/* ── EMPTY STATE ── */
.empty-state {
    background: rgba(255,255,255,0.03);
    border: 1px dashed rgba(255,255,255,0.09);
    border-radius: 18px; padding: 50px; text-align: center; margin-top: 16px;
}

.empty-icon { font-size: 2.5rem; margin-bottom: 12px; }
.empty-text { color: rgba(255,255,255,0.25); font-size: 0.82rem; letter-spacing: 1.5px; text-transform: uppercase; }

/* ── LOGIN CARD ── */
.login-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(40px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 28px; padding: 40px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.5);
    position: relative; overflow: hidden;
}

.login-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180,120,255,0.8), transparent);
}

/* ── PROJECT STATS ── */
.stat-row {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 14px 18px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}

.stat-row:hover { background: rgba(255,255,255,0.07); }
.stat-label { color: rgba(255,255,255,0.5); font-size: 0.82rem; }
.stat-val { color: #ffffff; font-weight: 700; font-family: 'Syne', sans-serif; font-size: 0.9rem; }

</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────
if 'logged_in'  not in st.session_state: st.session_state.logged_in  = False
if 'username'   not in st.session_state: st.session_state.username   = ""
if 'page'       not in st.session_state: st.session_state.page       = "🏠 Home"
if 'login_time' not in st.session_state: st.session_state.login_time = None

USERS = {
    "admin"   : {"password": "itsm2024", "role": "Administrator",  "name": "Admin",   "dept": "IT Management"},
    "supriya" : {"password": "rubix123", "role": "Data Scientist",  "name": "Supriya", "dept": "Data Science"},
    "analyst" : {"password": "abctech",  "role": "Analyst",         "name": "Analyst", "dept": "Analytics"},
}

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='rgba(255,255,255,0.55)', family='DM Sans'),
    margin=dict(l=0, r=0, t=30, b=0),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
)
COLORS = ['#7850ff','#4080ff','#ff4080','#20c070','#ff8040','#40d0ff']


# ══════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════
def show_login():
    set_background("login")

    try:
        requests.get(f"{FLASK_URL}/", timeout=10)
        db_ok = True
    except:
        db_ok = False

    st.markdown("""
    <div style='text-align:center; padding-top:30px; margin-bottom:6px;'>
        <span style='font-size:3.5rem;'>🎫</span>
    </div>
    <div style='text-align:center; margin-bottom:36px;'>
        <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800;
                    background:linear-gradient(135deg,#fff 0%,#b478ff 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:-1px; margin-bottom:5px;'>
            ABC Tech ITSM
        </div>
        <div style='color:rgba(255,255,255,0.32); font-size:0.78rem;
                    letter-spacing:3px; text-transform:uppercase;'>
            Machine Learning Powered Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.05, 1])
    with col2:
        if db_ok:
            st.markdown("<div class='status-ok'>✅ &nbsp; Database Connected — MySQL project_itsm · 46,606 records</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-fail'>❌ &nbsp; Flask API Offline — Run flask_api.py first</div>",
                        unsafe_allow_html=True)

        st.markdown("""
        <div class='login-card'>
            <div style='font-family:Syne,sans-serif; font-size:0.82rem; font-weight:700;
                        color:rgba(255,255,255,0.6); letter-spacing:2.5px; text-transform:uppercase;
                        margin-bottom:22px; text-align:center;'>Secure Sign In</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤  Username", placeholder="Enter your username")
        password = st.text_input("🔒  Password", type="password", placeholder="Enter your password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀   SIGN IN TO DASHBOARD", use_container_width=True):
            uname = username.lower().strip()
            if uname in USERS and USERS[uname]['password'] == password:
                st.session_state.logged_in  = True
                st.session_state.username   = uname
                st.session_state.login_time = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")

        st.markdown("""
        <div style='margin-top:18px; padding-top:14px;
                    border-top:1px solid rgba(255,255,255,0.06);
                    color:rgba(255,255,255,0.22); font-size:0.75rem;
                    text-align:center; line-height:1.9;'>
            Demo Credentials<br>
            admin / itsm2024 &nbsp;·&nbsp; supriya / rubix123 &nbsp;·&nbsp; analyst / abctech
        </div>
        """, unsafe_allow_html=True)

        # Project info below login
        st.markdown("""
        <div style='margin-top:28px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;'>
            <span style='background:rgba(120,80,255,0.15); border:1px solid rgba(120,80,255,0.3);
                         color:rgba(255,255,255,0.55); padding:4px 12px; border-radius:20px;
                         font-size:0.72rem; letter-spacing:1px;'>PRCL-0012</span>
            <span style='background:rgba(40,120,255,0.15); border:1px solid rgba(40,120,255,0.3);
                         color:rgba(255,255,255,0.55); padding:4px 12px; border-radius:20px;
                         font-size:0.72px; letter-spacing:1px; font-size:0.72rem;'>ABC Tech</span>
            <span style='background:rgba(30,180,100,0.15); border:1px solid rgba(30,180,100,0.3);
                         color:rgba(255,255,255,0.55); padding:4px 12px; border-radius:20px;
                         font-size:0.72rem; letter-spacing:1px;'>Rubixe AI Solutions</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# DASHBOARD WRAPPER
# ══════════════════════════════════════════════════
def show_dashboard():
    user     = USERS[st.session_state.username]
    initials = user['name'][0].upper()
    page     = st.session_state.page

    # Set page-specific background
    bg_map = {
        "Home": "home", "UC1": "uc1", "UC2": "uc2", "UC3": "uc3"
    }
    for key, val in bg_map.items():
        if key in page:
            set_background(val)
            break

    # ── Navbar ──
    st.markdown(f"""
    <div class='navbar'>
        <div class='navbar-brand'>🎫 &nbsp; ABC Tech ITSM</div>
        <div style='display:flex; align-items:center; gap:14px;'>
            <span class='navbar-badge'>ML Dashboard · PRCL-0012</span>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div class='user-avatar'>{initials}</div>
                <div>
                    <div style='color:#fff; font-size:0.84rem; font-weight:600; line-height:1.2;'>
                        {user['name']}
                    </div>
                    <div style='color:rgba(255,255,255,0.32); font-size:0.7rem; letter-spacing:0.5px;'>
                        {user['role']} · {user['dept']}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:20px 10px 16px;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:20px;'>
                <div style='width:40px; height:40px; background:linear-gradient(135deg,#7850ff,#4080ff);
                            border-radius:50%; display:flex; align-items:center; justify-content:center;
                            font-size:0.9rem; font-weight:700; color:#fff; flex-shrink:0;'>
                    {initials}
                </div>
                <div>
                    <div style='color:#fff; font-weight:700; font-size:0.9rem;'>{user['name']}</div>
                    <div style='color:rgba(255,255,255,0.35); font-size:0.72rem;'>{user['role']}</div>
                </div>
            </div>
            <div style='font-family:Syne,sans-serif; font-size:0.68rem;
                        color:rgba(255,255,255,0.25); letter-spacing:3px;
                        text-transform:uppercase; margin-bottom:10px; padding-left:4px;'>
                Navigation
            </div>
        </div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🏠", "🏠 Home",              "Overview & Live Stats"),
            ("🔴", "🔴 UC1 — High Priority","Predict critical tickets"),
            ("📈", "📈 UC2 — Forecast",     "Volume forecasting"),
            ("🏷️", "🏷️ UC3 — Auto Tag",   "Auto assign priority"),
        ]

        for _, label, desc in nav_items:
            active = label in st.session_state.page or st.session_state.page == label
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state.page = label
                st.rerun()

        st.markdown("---")

        # Session info
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
                    border-radius:12px; padding:14px; margin-bottom:10px;'>
            <div style='color:rgba(255,255,255,0.3); font-size:0.66rem; letter-spacing:2px;
                        text-transform:uppercase; margin-bottom:10px;'>Session Info</div>
            <div class='stat-row' style='margin-bottom:6px;'>
                <span class='stat-label'>Logged in</span>
                <span class='stat-val' style='font-size:0.76rem;'>{st.session_state.login_time or '—'}</span>
            </div>
            <div class='stat-row' style='margin-bottom:6px;'>
                <span class='stat-label'>Department</span>
                <span class='stat-val' style='font-size:0.76rem;'>{user['dept']}</span>
            </div>
            <div class='stat-row'>
                <span class='stat-label'>Project</span>
                <span class='stat-val' style='font-size:0.76rem;'>PRCL-0012</span>
            </div>
        </div>
        <div style='color:rgba(255,255,255,0.18); font-size:0.68rem; text-align:center;
                    line-height:1.9; padding:6px;'>
            ABC Tech · Rubixe AI Solutions<br>Developed by Supriya
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪  Logout", use_container_width=True):
            st.session_state.logged_in  = False
            st.session_state.login_time = None
            st.rerun()

    # ── Route ──
    if   "Home" in page: show_home()
    elif "UC1"  in page: show_uc1()
    elif "UC2"  in page: show_uc2()
    elif "UC3"  in page: show_uc3()


# ══════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════
def show_home():
    user = USERS[st.session_state.username]
    now  = datetime.datetime.now()

    st.markdown(f"""
    <div class='welcome-card'>
        <div style='display:flex; align-items:center; gap:16px;'>
            <div style='width:56px; height:56px; background:linear-gradient(135deg,#7850ff,#4080ff);
                        border-radius:16px; display:flex; align-items:center; justify-content:center;
                        font-size:1.5rem; font-weight:800; color:#fff; flex-shrink:0;'>
                {user['name'][0].upper()}
            </div>
            <div>
                <div style='color:rgba(255,255,255,0.45); font-size:0.76rem;
                            letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px;'>
                    Welcome back
                </div>
                <div class='welcome-name'>{user['name']} 👋</div>
                <div class='welcome-role'>{user['role']} · {user['dept']}</div>
            </div>
        </div>
        <div class='welcome-meta'>
            <span class='meta-pill'>🕐 {now.strftime('%I:%M %p')}</span>
            <span class='meta-pill'>📅 {now.strftime('%d %b %Y')}</span>
            <span class='meta-pill'>🗄️ MySQL Connected</span>
            <span class='meta-pill'>🤖 3 Models Active</span>
            <span class='meta-pill'>📋 PRCL-0012</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # DB Stats
    db_ok = False
    stats = {}
    try:
        r     = requests.get(f"{FLASK_URL}/api/summary", timeout=5)
        stats = r.json()
        db_ok = True
        st.markdown("<div class='status-ok'>✅ &nbsp; Live data — MySQL project_itsm · 46,606 records loaded successfully</div>",
                    unsafe_allow_html=True)
    except:
        st.markdown("<div class='status-fail'>❌ &nbsp; Cannot reach Flask API — check if flask_api.py is running</div>",
                    unsafe_allow_html=True)

    # KPI Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, color, emoji, val, label in zip(
        [c1,c2,c3,c4,c5],
        ['blue','purple','pink','green','orange'],
        ['📊','🔴','🤖','🏷️','📅'],
        ['46,606','700','99.31%','91.92%','2012–14'],
        ['Total Tickets','High Priority','UC1 Accuracy','UC3 Accuracy','Data Range']
    ):
        with col:
            st.markdown(f"""
            <div class='kpi-glass {color}'>
                <div class='kpi-emoji'>{emoji}</div>
                <div class='kpi-val'>{val}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # Charts
    if db_ok:
        st.markdown("<div class='sec-title'>Live Database Insights</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            priority_df = pd.DataFrame(stats.get('priority', []))
            if not priority_df.empty:
                fig = px.bar(priority_df, x='Priority', y='count',
                             color_discrete_sequence=COLORS,
                             template='plotly_dark', title='Priority Distribution')
                fig.update_layout(**PLOT_LAYOUT)
                fig.update_traces(marker_color=COLORS[:len(priority_df)], marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            category_df = pd.DataFrame(stats.get('category', []))
            if not category_df.empty:
                fig = px.pie(category_df, values='count', names='Category',
                             color_discrete_sequence=COLORS, template='plotly_dark',
                             title='Category Distribution', hole=0.55)
                fig.update_layout(**PLOT_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

        yearly_df = pd.DataFrame(stats.get('yearly', [])).dropna()
        if not yearly_df.empty:
            st.markdown("<div class='sec-title'>Annual Incident Volume</div>", unsafe_allow_html=True)
            fig = px.area(yearly_df, x='year', y='count', template='plotly_dark',
                          title='Yearly Incident Volume', color_discrete_sequence=['#7850ff'])
            fig.update_layout(**PLOT_LAYOUT, height=260)
            fig.update_traces(fill='tozeroy', fillcolor='rgba(120,80,255,0.1)',
                              line=dict(color='#7850ff', width=3))
            st.plotly_chart(fig, use_container_width=True)

    # Project Details + UC Cards
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown("<div class='sec-title'>Project Details</div>", unsafe_allow_html=True)
        details = [
            ("Project Ref", "PRCL-0012"),
            ("Client", "ABC Tech"),
            ("Domain", "IT Service Management"),
            ("Dataset", "46,606 records"),
            ("Database", "MySQL project_itsm"),
            ("Years", "2012 · 2013 · 2014"),
            ("Use Cases", "3 Active (UC4 skipped)"),
            ("Best UC1", "99.31% accuracy"),
            ("Best UC3", "91.92% accuracy"),
            ("UC2 MAE", "272.93 tickets"),
            ("Intern", "Supriya"),
            ("Company", "Rubixe AI Solutions"),
        ]
        for label, val in details:
            st.markdown(f"""
            <div class='stat-row'>
                <span class='stat-label'>{label}</span>
                <span class='stat-val'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='sec-title'>ML Use Cases</div>", unsafe_allow_html=True)
        ca, cb = st.columns(2)

        with ca:
            st.markdown("""
            <div class='uc-glass' style='margin-bottom:12px;'>
                <span class='uc-tag red'>Binary Classification</span>
                <div class='uc-metric' style='color:#ff6080;'>99.31%</div>
                <div style='font-family:Syne,sans-serif;color:#fff;font-weight:700;margin-bottom:8px;font-size:0.95rem;'>UC1 — High Priority</div>
                <div class='uc-desc'>Predicts Priority 1 or 2 tickets. Random Forest + SMOTE. Recall 99.46%. Only 50 missed out of 9,181.</div>
            </div>
            <div class='uc-glass'>
                <span class='uc-tag blue'>Time Series</span>
                <div class='uc-metric' style='color:#60a0ff;'>272.93</div>
                <div style='font-family:Syne,sans-serif;color:#fff;font-weight:700;margin-bottom:8px;font-size:0.95rem;'>UC2 — Forecasting</div>
                <div class='uc-desc'>ARIMA(2,1,2) for monthly volume. MAE 272. Beats LR and Facebook Prophet on 24 months data.</div>
            </div>
            """, unsafe_allow_html=True)

        with cb:
            st.markdown("""
            <div class='uc-glass' style='margin-bottom:12px;'>
                <span class='uc-tag green'>Multi-class</span>
                <div class='uc-metric' style='color:#50d090;'>91.92%</div>
                <div style='font-family:Syne,sans-serif;color:#fff;font-weight:700;margin-bottom:8px;font-size:0.95rem;'>UC3 — Auto Tag</div>
                <div class='uc-desc'>4-class priority tagging (2/3/4/5). Random Forest + SMOTE. Priority 2 achieves F1 of 0.98.</div>
            </div>
            <div class='uc-glass'>
                <span style='background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                             display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.68rem;
                             letter-spacing:1.5px;text-transform:uppercase;font-weight:600;margin-bottom:12px;
                             color:rgba(255,255,255,0.4);'>Data Limitation</span>
                <div class='uc-metric' style='color:rgba(255,255,255,0.3);font-size:1.4rem;'>Skipped</div>
                <div style='font-family:Syne,sans-serif;color:rgba(255,255,255,0.5);font-weight:700;margin-bottom:8px;font-size:0.95rem;'>UC4 — RFC Failure</div>
                <div class='uc-desc'>Only 1 RFC record in 46,606 tickets. Insufficient data to build a reliable model. Documented as limitation.</div>
            </div>
            """, unsafe_allow_html=True)

    # Model Summary Table
    st.markdown("<div class='sec-title'>Model Performance Summary</div>", unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Use Case' : ['UC1 — High Priority','UC2 — Forecasting','UC3 — Auto Tag','UC4 — RFC Failure'],
        'Model'    : ['Random Forest (Tuned)','ARIMA(2,1,2)','Random Forest (Tuned)','Not Built'],
        'Status'   : ['✅ Deployed','✅ Deployed','✅ Deployed','❌ Skipped'],
        'Accuracy' : ['99.31%','MAE: 272.93','91.92%','—'],
        'Precision': ['99.16%','RMSE: 319.14','91.95%','—'],
        'Recall'   : ['99.46%','—','91.92%','—'],
        'F1 Score' : ['99.31%','—','91.92%','—'],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════
# UC1
# ══════════════════════════════════════════════════
def show_uc1():
    st.markdown("""
    <div class='page-title'>🔴 High Priority Prediction</div>
    <div class='page-sub'>UC1 — Binary classification to detect Priority 1 or 2 tickets instantly</div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, val, label, color in zip([c1,c2,c3,c4],
        ['99.31%','99.16%','99.46%','Random Forest'],
        ['Accuracy','Precision','Recall','Best Model'],
        ['blue','purple','pink','green']):
        with col:
            st.markdown(f"<div class='kpi-glass {color}'><div class='kpi-val' style='font-size:1.4rem;'>{val}</div><div class='kpi-label'>{label}</div></div>",
                        unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>Enter Ticket Details</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        ci_cat      = st.selectbox("CI Category",            options=list(range(0,13)))
        ci_subcat   = st.selectbox("CI Sub Category",        options=list(range(0,65)))
        wbs         = st.selectbox("WBS Code",               options=list(range(0,274)))
        status      = st.selectbox("Status",                 options=[0,1], format_func=lambda x: ['Open','Closed'][x])
        category    = st.selectbox("Category",               options=[0,1,2,3], format_func=lambda x: ['Complaint','Incident','RFC','Request for Info'][x])
        kb_number   = st.selectbox("KB Number",              options=list(range(0,1825)))
        no_reassign = st.number_input("No of Reassignments", min_value=0, max_value=50, value=0)

    with c2:
        handle_time     = st.number_input("Handle Time (hrs)",       min_value=0.0, value=10.0)
        closure_code    = st.selectbox("Closure Code",               options=list(range(0,15)))
        no_interactions = st.number_input("Related Interactions",    min_value=0, max_value=10, value=0)
        open_year       = st.selectbox("Open Year",                  options=[2012,2013,2014])
        open_month      = st.selectbox("Open Month",                 options=list(range(1,13)), format_func=lambda x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][x-1])
        open_quarter    = st.selectbox("Open Quarter",               options=[1,2,3,4], format_func=lambda x: f"Q{x}")
        open_dow        = st.selectbox("Day of Week",                options=list(range(0,7)), format_func=lambda x: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔴   PREDICT PRIORITY LEVEL", use_container_width=True):
        payload = {
            'CI_Cat':ci_cat,'CI_Subcat':ci_subcat,'WBS':wbs,'Status':status,
            'Category':category,'KB_number':kb_number,'No_of_Reassignments':no_reassign,
            'Handle_Time_hrs':handle_time,'Closure_Code':closure_code,
            'No_of_Related_Interactions':no_interactions,'Open_Year':open_year,
            'Open_Month':open_month,'Open_Quarter':open_quarter,'Open_DayOfWeek':open_dow
        }
        try:
            r = requests.post(f"{FLASK_URL}/api/predict_priority", json=payload)
            result = r.json()
            pred = result['prediction']
            conf = result['confidence']

            c1, c2 = st.columns([1.5, 1])
            with c1:
                if pred == 1:
                    st.markdown(f"""
                    <div class='result-card danger'>
                        <div class='result-emoji'>🚨</div>
                        <div class='result-label danger'>HIGH PRIORITY TICKET</div>
                        <div class='result-sub'>Priority 1 or 2 — Immediate escalation required</div>
                        <span class='result-confidence'>Model Confidence: {conf}%</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='result-card success'>
                        <div class='result-emoji'>✅</div>
                        <div class='result-label success'>NORMAL PRIORITY</div>
                        <div class='result-sub'>Priority 3, 4 or 5 — Standard processing queue</div>
                        <span class='result-confidence'>Model Confidence: {conf}%</span>
                    </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='sec-title'>Input Summary</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='info-panel'>
                    <div class='info-row'><span>CI Sub Category</span><span class='info-val'>{ci_subcat}</span></div>
                    <div class='info-row'><span>KB Number</span><span class='info-val'>{kb_number}</span></div>
                    <div class='info-row'><span>WBS Code</span><span class='info-val'>{wbs}</span></div>
                    <div class='info-row'><span>Handle Time</span><span class='info-val'>{handle_time} hrs</span></div>
                    <div class='info-row'><span>Reassignments</span><span class='info-val'>{no_reassign}</span></div>
                    <div class='info-row'><span>Category</span><span class='info-val'>{['Complaint','Incident','RFC','Request for Info'][category]}</span></div>
                    <div class='info-row'><span>Status</span><span class='info-val'>{'Open' if status==0 else 'Closed'}</span></div>
                    <div class='info-row'><span>Open Period</span><span class='info-val'>{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][open_month-1]} {open_year}</span></div>
                    <div class='info-row'><span>Prediction</span><span class='info-val'>{'🔴 High Priority' if pred==1 else '✅ Normal'}</span></div>
                    <div class='info-row'><span>Confidence</span><span class='info-val'>{conf}%</span></div>
                </div>""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"API Error: {e}")


# ══════════════════════════════════════════════════
# UC2
# ══════════════════════════════════════════════════
def show_uc2():
    st.markdown("""
    <div class='page-title'>📈 Incident Volume Forecast</div>
    <div class='page-sub'>UC2 — ARIMA(2,1,2) time series model for proactive resource planning</div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, val, label, color in zip([c1,c2,c3,c4],
        ['ARIMA(2,1,2)','272.93','319.14','Stationary'],
        ['Algorithm','MAE Score','RMSE Score','ADF Test'],
        ['blue','purple','pink','green']):
        with col:
            st.markdown(f"<div class='kpi-glass {color}'><div class='kpi-val' style='font-size:1.3rem;'>{val}</div><div class='kpi-label'>{label}</div></div>",
                        unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>Forecast Configuration</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])

    with c1:
        periods = st.slider("Forecast Months", min_value=1, max_value=12, value=6)
        st.markdown(f"""
        <div class='info-panel'>
            <div style='font-family:Syne,sans-serif;font-size:0.68rem;color:rgba(255,255,255,0.28);
                        letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;'>Model Details</div>
            <div class='info-row'><span>Algorithm</span><span class='info-val'>ARIMA(2,1,2)</span></div>
            <div class='info-row'><span>p (AR order)</span><span class='info-val'>2</span></div>
            <div class='info-row'><span>d (Differencing)</span><span class='info-val'>1</span></div>
            <div class='info-row'><span>q (MA order)</span><span class='info-val'>2</span></div>
            <div class='info-row'><span>Training Data</span><span class='info-val'>2013–2014</span></div>
            <div class='info-row'><span>Data Points</span><span class='info-val'>24 months</span></div>
            <div class='info-row'><span>MAE</span><span class='info-val'>272.93</span></div>
            <div class='info-row'><span>RMSE</span><span class='info-val'>319.14</span></div>
            <div class='info-row'><span>Forecast</span><span class='info-val'>{periods} months</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("📈   GENERATE FORECAST", use_container_width=True)

    with c2:
        if run:
            try:
                r        = requests.post(f"{FLASK_URL}/api/forecast", json={'periods': periods})
                result   = r.json()
                forecast = result['forecast']

                start = datetime.date(2015, 1, 1)
                dates = []
                for i in range(periods):
                    m = ((start.month + i - 1) % 12) + 1
                    y = start.year + (start.month + i - 1) // 12
                    dates.append(f"{y}-{str(m).zfill(2)}")

                fdf = pd.DataFrame({'Month': dates, 'Predicted Incidents': [int(f) for f in forecast]})

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=fdf['Month'], y=fdf['Predicted Incidents'],
                    mode='lines+markers',
                    line=dict(color='#7850ff', width=3),
                    marker=dict(size=9, color='#7850ff',
                                line=dict(color='rgba(8,8,20,0.8)', width=2)),
                    fill='tozeroy', fillcolor='rgba(120,80,255,0.08)', name='Forecast'
                ))
                fig.update_layout(**PLOT_LAYOUT, height=300,
                    title=dict(text=f'Incident Volume Forecast — Next {periods} Months',
                               font=dict(color='rgba(255,255,255,0.65)', size=13)))
                st.plotly_chart(fig, use_container_width=True)

                ca, cb, cc, cd = st.columns(4)
                for col, val, label, color in zip([ca,cb,cc,cd],
                    [f"{int(sum(forecast)/len(forecast)):,}",
                     f"{int(max(forecast)):,}",
                     f"{int(min(forecast)):,}",
                     f"{int(sum(forecast)):,}"],
                    ['Avg / Month','Peak Month','Low Month','Total Forecast'],
                    ['blue','pink','green','purple']):
                    with col:
                        st.markdown(f"<div class='kpi-glass {color}' style='margin-top:8px;'><div class='kpi-val' style='font-size:1.3rem;'>{val}</div><div class='kpi-label'>{label}</div></div>",
                                    unsafe_allow_html=True)

                st.markdown("<div class='sec-title'>Forecast Table</div>", unsafe_allow_html=True)
                st.dataframe(fdf, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"API Error: {e}")
        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-icon'>📈</div>
                <div class='empty-text'>Configure periods and click Generate Forecast</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# UC3
# ══════════════════════════════════════════════════
def show_uc3():
    st.markdown("""
    <div class='page-title'>🏷️ Auto Tag Tickets</div>
    <div class='page-sub'>UC3 — Multi-class classification to auto-assign correct priority level</div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, val, label, color in zip([c1,c2,c3,c4],
        ['91.92%','91.95%','91.92%','4 Classes'],
        ['Accuracy','Precision','Recall','Priority Levels'],
        ['blue','purple','pink','green']):
        with col:
            st.markdown(f"<div class='kpi-glass {color}'><div class='kpi-val' style='font-size:1.4rem;'>{val}</div><div class='kpi-label'>{label}</div></div>",
                        unsafe_allow_html=True)

    # Priority legend
    st.markdown("""
    <div style='display:flex; gap:8px; margin:16px 0; flex-wrap:wrap;'>
        <span style='background:rgba(255,40,80,0.12);border:1px solid rgba(255,40,80,0.28);color:#ff6080;padding:4px 14px;border-radius:20px;font-size:0.76rem;'>🔴 Priority 2 — Critical</span>
        <span style='background:rgba(255,140,40,0.12);border:1px solid rgba(255,140,40,0.28);color:#ff9040;padding:4px 14px;border-radius:20px;font-size:0.76rem;'>🟠 Priority 3 — High</span>
        <span style='background:rgba(40,120,255,0.12);border:1px solid rgba(40,120,255,0.28);color:#60a0ff;padding:4px 14px;border-radius:20px;font-size:0.76rem;'>🔵 Priority 4 — Medium</span>
        <span style='background:rgba(30,180,100,0.12);border:1px solid rgba(30,180,100,0.28);color:#50d090;padding:4px 14px;border-radius:20px;font-size:0.76rem;'>🟢 Priority 5 — Low</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>Enter Ticket Details</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        ci_cat      = st.selectbox("CI Category ",           options=list(range(0,13)))
        ci_subcat   = st.selectbox("CI Sub Category ",       options=list(range(0,65)))
        wbs         = st.selectbox("WBS Code ",              options=list(range(0,274)))
        status      = st.selectbox("Status ",                options=[0,1], format_func=lambda x: ['Open','Closed'][x])
        category    = st.selectbox("Category ",              options=[0,1,2,3], format_func=lambda x: ['Complaint','Incident','RFC','Request for Info'][x])
        kb_number   = st.selectbox("KB Number ",             options=list(range(0,1825)))
        no_reassign = st.number_input("Reassignments ",      min_value=0, max_value=50, value=0)

    with c2:
        handle_time     = st.number_input("Handle Time (hrs) ",       min_value=0.0, value=10.0)
        closure_code    = st.selectbox("Closure Code ",               options=list(range(0,15)))
        no_interactions = st.number_input("Related Interactions ",    min_value=0, max_value=10, value=0)
        open_year       = st.selectbox("Open Year ",                  options=[2012,2013,2014])
        open_month      = st.selectbox("Open Month ",                 options=list(range(1,13)), format_func=lambda x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][x-1])
        open_quarter    = st.selectbox("Open Quarter ",               options=[1,2,3,4], format_func=lambda x: f"Q{x}")
        open_dow        = st.selectbox("Day of Week ",                options=list(range(0,7)), format_func=lambda x: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🏷️   AUTO TAG THIS TICKET", use_container_width=True):
        payload = {
            'CI_Cat':ci_cat,'CI_Subcat':ci_subcat,'WBS':wbs,'Status':status,
            'Category':category,'KB_number':kb_number,'No_of_Reassignments':no_reassign,
            'Handle_Time_hrs':handle_time,'Closure_Code':closure_code,
            'No_of_Related_Interactions':no_interactions,'Open_Year':open_year,
            'Open_Month':open_month,'Open_Quarter':open_quarter,'Open_DayOfWeek':open_dow
        }
        try:
            r        = requests.post(f"{FLASK_URL}/api/auto_tag", json=payload)
            result   = r.json()
            priority = result['predicted_priority']
            conf     = result['confidence']

            styles = {
                2: ('p2','🔴','#ff6080','CRITICAL',  'Immediate response required — Major business impact',       '< 1 hour'),
                3: ('p3','🟠','#ff9040','HIGH',      'Respond within 4 hours — Significant operational impact',  '4 hours'),
                4: ('p4','🔵','#60a0ff','MEDIUM',    'Respond within 8 hours — Moderate business impact',        '8 hours'),
                5: ('p5','🟢','#50d090','LOW',       'Respond within 24 hours — Minimal business impact',        '24 hours'),
            }
            cls, icon, color, severity, desc, sla = styles.get(
                priority, ('p4','🔵','#60a0ff','MEDIUM','Standard processing','8 hours'))

            c1, c2 = st.columns([1.5, 1])

            with c1:
                st.markdown(f"""
                <div class='priority-result {cls}'>
                    <div style='font-size:3rem;margin-bottom:10px;'>{icon}</div>
                    <div style='font-family:Syne,sans-serif;font-size:0.68rem;color:rgba(255,255,255,0.35);
                                letter-spacing:3px;text-transform:uppercase;margin-bottom:5px;'>Auto Tagged As</div>
                    <div style='font-family:Syne,sans-serif;font-size:1.9rem;font-weight:800;
                                color:{color};margin-bottom:3px;'>PRIORITY {priority}</div>
                    <div style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
                                color:rgba(255,255,255,0.65);margin-bottom:8px;'>{severity}</div>
                    <div style='color:rgba(255,255,255,0.38);font-size:0.82rem;margin-bottom:14px;'>{desc}</div>
                    <div style='display:flex;gap:10px;justify-content:center;flex-wrap:wrap;'>
                        <span class='result-confidence'>Confidence: {conf}%</span>
                        <span style='background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.13);
                                     border-radius:20px;padding:5px 16px;color:rgba(255,255,255,0.65);
                                     font-size:0.82rem;letter-spacing:1px;'>SLA: {sla}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='sec-title'>Ticket Summary</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='info-panel'>
                    <div class='info-row'><span>CI Sub Category</span><span class='info-val'>{ci_subcat}</span></div>
                    <div class='info-row'><span>KB Number</span><span class='info-val'>{kb_number}</span></div>
                    <div class='info-row'><span>WBS Code</span><span class='info-val'>{wbs}</span></div>
                    <div class='info-row'><span>Category</span><span class='info-val'>{['Complaint','Incident','RFC','Request for Info'][category]}</span></div>
                    <div class='info-row'><span>Handle Time</span><span class='info-val'>{handle_time} hrs</span></div>
                    <div class='info-row'><span>Reassignments</span><span class='info-val'>{no_reassign}</span></div>
                    <div class='info-row'><span>Open Period</span><span class='info-val'>{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][open_month-1]} {open_year}</span></div>
                    <div class='info-row'><span>Tagged Priority</span><span class='info-val' style='color:{color};'>Priority {priority} — {severity}</span></div>
                    <div class='info-row'><span>SLA Target</span><span class='info-val'>{sla}</span></div>
                    <div class='info-row'><span>Confidence</span><span class='info-val'>{conf}%</span></div>
                </div>""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"API Error: {e}")


# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
