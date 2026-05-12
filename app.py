import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (CONSOLE INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#00d4ff, #005fcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
        letter-spacing: 2px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
    label { color: #aaa !important; font-size: 14px !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- AIRPORT DATABASE ---
AIRPORT_DB = {
    "KTEB": ["Teterboro Airport", "Teterboro", "NJ", "US/Eastern"],
    "KMIA": ["Miami International", "Miami", "FL", "US/Eastern"],
    "KOPF": ["Opa-Locka Executive", "Miami", "FL", "US/Eastern"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"],
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"]
}

WEATHER_ICONS = {"Sunny": "☼", "Partly Cloudy": "☁", "Cloudy": "☁", "Rainy": "☂", "Thunderstorm": "⚡", "Snowy": "❄", "Foggy": "░"}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. ITINERARY INPUTS ---
st.subheader("📍 Flight Itinerary")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    _, dep_city, _, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", value="Signature Flight Support")
    dep_time = st.text_input("Departure Time", value="10:00 AM")
with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    _, arr_city, _, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Arrival Time", value="01:30 PM")

milestone = st.selectbox("Current Milestone", ["Trip Confirmation", "Positioning Update", "Aircraft Ready & FBO Reception", "Flight Active / Taxiing"])

# --- 2. WEATHER ASSESSMENT (AHORA SIEMPRE VISIBLE EN CONSOLA) ---
st.subheader("🌫️ Weather Assessment")
c_w1, c_w2 = st.columns(2)
with c_w1:
    d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
    dep_wx_msg = st.text_input("Dep Brief", placeholder="e.g. Clear Skies")
with c_w2:
    a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
    arr_wx_msg = st.text_input("Arr Brief", placeholder="e.g. Standard conditions")

# --- 3. GROUND & CONCIERGE ---
st.subheader("⚙️ Additional Services")
cs1, cs2, cs3 = st.columns(3)
with cs1: 
    s_pets = st.checkbox("Pets")
    s_catering = st.checkbox("Catering")
with cs2: 
    s_ground = st.checkbox("Ground Transportation")
    s_rental = st.checkbox("Rental Car")
with cs3:
    s_assist = st.checkbox("Special Assistance")

# --- 4. GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, a_icao, a_city, a_fbo, a_time, d_icon, d_msg, a_icon, a_msg, services):
    
    BRAND_COLOR = "#00d4ff"
    
    # Dashboard de Servicios
    svc_data = [
        {"label": "PETS", "active": services['pets']},
        {"label": "CATERING", "active": services['catering']},
        {"label": "GROUND TRANS.", "active": services['ground']},
        {"label": "RENTAL CAR", "active": services['rental']},
        {"label": "SPECIAL ASST.", "active": services['assist']}
    ]
    
    svc_html = "<div style='margin-top:20px; text-align:center;'>"
    for item in svc_data:
        bg = "#e6faff" if item['active'] else "#f5f5f5"
        txt = BRAND_COLOR if item['active'] else "#bbbbbb"
        border = f"2px solid {BRAND_COLOR}" if item['active'] else "2px solid #eeeeee"
        svc_html
