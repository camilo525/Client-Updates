import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (CONSOLE INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#cb2d42, #8e1e2d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
        letter-spacing: 2px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"], div[data-baseweb="radio"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #cb2d42 !important; }
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
    ramp_dep = st.radio("Dep. Ramp Access", ["Authorized", "Not Authorized"], horizontal=True)

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    _, arr_city, _, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Arrival Time", value="01:30 PM")
    ramp_arr = st.radio("Arr. Ramp Access", ["Authorized", "Not Authorized"], horizontal=True)

milestone = st.selectbox("Current Milestone", ["Trip Confirmation", "Positioning Update", "Aircraft Ready & FBO Reception", "Flight Active / Taxiing"])

# --- 2. WEATHER ASSESSMENT ---
st.subheader("🌫️ Weather Assessment")
cw1, cw2 = st.columns(2)
with cw1:
    d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
    dep_wx_msg = st.text_input("Dep Brief", placeholder="e.g. Clear Skies")
with cw2:
    a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
    arr_wx_msg = st.text_input("Arr Brief", placeholder="e.g. Standard conditions")

# --- 3. ADDITIONAL SERVICES ---
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

# --- 4. GENERATOR FUNCTION ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, a_icao, a_city, a_fbo, a_time, d_icon, d_msg, a_icon, a_msg, services, r_dep, r_arr):
    BRAND_COLOR = "#cb2d42"
    DARK_BAR = "#282522"
    
    svc_data = [
        {"label": "PETS", "active": services['pets']},
        {"label": "CATERING", "active": services['catering']},
        {"label": "GROUND TRANS.", "active": services['ground']},
        {"label": "RENTAL CAR", "active": services['rental']},
        {"label": "SPECIAL ASST.", "active": services['assist']}
    ]
    
    svc_html = "<div style='text-align:center; margin-top:20px;'>"
    for item in svc_data:
        bg = "#fff5f6" if item['active'] else "#f5f5f5"
        txt = BRAND_COLOR if item['active'] else "#bbbbbb"
        border = f"2px solid {BRAND_COLOR}" if item['active'] else f"2px solid {DARK_BAR}22"
        svc_html += f'<div style="display:inline-block; margin:5px; width:90px; padding:12px 0; border-radius:8px; background:{bg}; border:{border}; text-align:center;"><div style="font-size:18px; color:{txt}; font-weight:bold;">◈</div><div style="font-size:8px; color:{txt}; font-weight:bold; margin-top:4px; letter-spacing:0.5px;">{item["label"]}</div></div>'
    svc_html += "</div>"

    wx_display = ""
    if m_stage != "Trip Confirmation":
        wx_display = f"""<div style='margin-top:25px; display: table; width: 100%;'><div style='display: table-cell; width: 48%; padding:20px; background:#fcfcfc; border:1px solid #eee; border-radius:10px; border-top:4px solid {BRAND_COLOR};'><span style='font-size:24px; color:{BRAND_COLOR};'>{d_icon}</span><br><b style='font-size:11px; color:#999; text-transform:uppercase;'>Departure WX</b><br><span style='font-size:13px; color:#
