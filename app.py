import streamlit as st
import pytz
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (CONSOLE INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#cb2d42, #911d2d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #cb2d42 !important; }
    label { color: #ccc !important; font-size: 14px !important; }
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
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"],
    "MMMX": ["Mexico City Intl", "Mexico City", "MX", "America/Mexico_City"],
    "EGSS": ["Stansted Airport", "London", "UK", "Europe/London"]
}

WEATHER_ICONS = {"Sunny": "☀️", "Partly Cloudy": "⛅", "Cloudy": "☁️", "Rainy": "🌧️", "Thunderstorm": "⛈️", "Snowy": "❄️", "Foggy": "🌫️"}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. ITINERARY & FBO INPUTS ---
st.subheader("📍 1. Flight Itinerary & FBO Details")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", value="Signature Flight Support")
    dep_time = st.text_input("Local Departure Time", value="10:00 AM")

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    arr_name, arr_city, arr_state, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Local Arrival Time", value="01:30 PM")

# --- 2. MILESTONE SELECTOR ---
st.markdown("---")
milestone = st.selectbox("Current Stage", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

# --- 3. TRIP CONFIRMATION LOGIC (PROGRESS TRACKER) ---
switches = {}
if milestone == "Trip Confirmation":
    st.subheader("✅ Trip Progress Checklist")
    c1, c2 = st.columns(2)
    categories = ["Passenger info", "Luggage", "Pets", "Catering", "Ground transportation", "Rental", "Special medical assistance"]
    for i, cat in enumerate(categories):
        col = c1 if i % 2 == 0 else c2
        switches[cat] = col.checkbox(cat)

# --- 4. WEATHER LOGIC (VISIBLE IN OPERATIONAL STAGES) ---
dep_wx_msg, arr_wx_msg = "", ""
d_icon_key, a_icon_key = "Sunny", "Sunny"

if milestone != "Trip Confirmation":
    st.subheader("🌫️ Weather Assessment (Live Update)")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        d_icon_key = st.selectbox("Departure Icon", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Departure Brief", placeholder="Current departure weather...")
    with col_w2:
        a_icon_key = st.selectbox("Arrival Icon", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arrival Brief", placeholder="Current arrival forecast...")

# --- 5. VIP NEWSLETTER GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, sw, d_wx_icon, d_wx_msg, a_wx_icon, a_wx_msg):
    
    COMPANY_LOGO_URL = "https://images.teamtailor-cdn.com/images/s3/teamtailor-na-maroon/logotype-v3/image_uploads/d1ea3807-ceaf-486c-aefb-af34155789ba/original.png" 
    BRAND_COLOR = "#cb2d42"
    
    title_map = {
        "Trip Confirmation": "TRIP CONFIRMATION",
        "Positioning Update": "POSITIONING UPDATE",
        "Aircraft Ready & FBO Reception": "AIRCRAFT READY",
        "Flight Active / Taxiing": "FLIGHT ACTIVE"
    }
    
    tracker_html = ""
    if m_stage == "Trip Confirmation":
        tracker_html = f"<div style='margin-top:20px; border-top:1px solid #eee; padding-top:15px;'><b style='font-size:12px; color:#444;'>TRIP PROGRESS:</b><table width='100%' style='margin-top:10px; border-collapse: collapse;'>"
        icons = {"Passenger info": "👤", "Luggage": "🧳", "Pets": "🐾", "Catering": "🍽️", "Ground transportation": "🚘", "Rental": "🔑", "Special medical assistance": "⚕️"}
        for cat, active in sw.items():
            color = BRAND_COLOR if active else "#cccccc"
            status = "READY" if active else "PENDING"
            tracker_html += f"<tr><td style='font-size:16px; width:30px; padding: 4px 0;'>{icons[cat]}</td><td style='font-size:13px; color:#555;'>{cat}</td><td style='text-align:right; font-size:11px; font-weight:bold; color:{color};'>{status}</td></tr>"
        tracker_html += "</table></div>"

    wx_display = ""
    if m_stage != "Trip Confirmation" and (d_wx_msg or a_wx_msg):
        wx_display = f"""
        <div style='margin-top:15px; display:flex; gap:10px;'>
            <div style='flex:1; background:#fff5f6; padding:10px; border-radius:8px; border-left:4px solid {BRAND_COLOR};'>
                <span style='font-size:20px;'>{d_wx_icon}</span><br>
                <b style='font-size:10px; color:{BRAND_COLOR};'>DEP WX:</b><br>
                <span style='font-size:12px;'>{d_wx_msg}</span>
            </div>
            <div style='flex:1; background:#fff5f6; padding:10px; border-radius:8px; border-left:4px solid {BRAND_COLOR};'>
                <span style='font-size:20px;'>{a_wx_icon}</span><br>
                <b style='font
