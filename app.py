import streamlit as st
import pytz
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (VIP DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#cb2d42, #911d2d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
    }
    .stSelectbox div[data-baseweb="select"] { font-size: 24px !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #cb2d42 !important; }
    label { color: #888 !important; font-size: 14px !important; }
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

WEATHER_ICONS = {
    "Sunny": "☀️", "Partly Cloudy": "⛅", "Cloudy": "☁️", 
    "Rainy": "🌧️", "Thunderstorm": "⛈️", "Snowy": "❄️", "Foggy": "🌫️"
}

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

# --- 4. WEATHER LOGIC ---
dep_wx_msg, arr_wx_msg = "", ""
dep_wx_icon_key, arr_wx_icon_key = "Sunny", "Sunny"

if milestone != "Trip Confirmation":
    st.subheader("🌫️ Weather Assessment")
    col_dep_wx, col_arr_wx = st.columns(2)
    with col_dep_wx:
        dep_wx_icon_key = st.selectbox("Departure Icon", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Departure Brief")
    with col_arr_wx:
        arr_wx_icon_key = st.selectbox("Arrival Icon", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arrival Brief")

# --- 5. VIP NEWSLETTER GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, sw, d_wx_icon, d_wx_msg, a_wx_icon, a_wx_msg):
    
    # BRANDING
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
        tracker_html = f"<div style='margin-top:20px; border-top:1px solid #eee; padding-top:15px;'><b style='font-size:12px; color:#444;'>TRIP PROGRESS:</b><table width='100%' style='margin-top:10px;'>"
        icons = {"Passenger info": "👤", "Luggage": "🧳", "Pets": "🐾", "Catering": "🍽️", "Ground transportation": "🚘", "Rental": "🔑", "Special medical assistance": "⚕️"}
        for cat, active in sw.items():
            color = BRAND_COLOR if active else "#cccccc"
            status = "READY" if active else "PENDING"
            tracker_html += f"<tr><td style='font-size:16px; width:30px;'>{icons[cat]}</td><td style='font-size:13px; color:#555;'>{cat}</td><td style='text-align:right; font-size:11px; font-weight:bold; color:{color};'>{status}</td></tr>"
        tracker_html += "</table></div>"

    wx_display = ""
    if m_stage != "Trip Confirmation" and (d_wx_msg or a_wx_msg):
        wx_display = f"""<div style='margin-top:20px; display: table; width: 100%; border-collapse: collapse;'>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#fff5f6; border-radius:8px; border-left:4px solid {BRAND_COLOR};'>
                                <span style='font-size:24px;'>{d_wx_icon}</span><br>
                                <b style='font-size:10px; color:{BRAND_COLOR};'>DEPARTURE:</b><br>
                                <span style='font-size:12px;'>{d_wx_msg}</span>
                            </div>
                            <div style='display: table-cell; width: 4%;'></div>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#fff5f6; border-radius:8px; border-left:4px solid {BRAND_COLOR};'>
                                <span style='font-size:24px;'>{a_wx_icon}</span><br>
                                <b style='font-size:12px; color:{BRAND_COLOR};'>ARRIVAL:</b><br>
                                <span style='font-size:12px;'>{a_wx_msg}</span>
                            </div>
                         </div>"""

    msg_map = {
        "Trip Confirmation": "Your flight details are confirmed. Please find your updated trip sheet attached.",
        "Positioning Update": f"The aircraft is currently positioning to {d_city}. Operations are on schedule.",
        "Aircraft Ready & FBO Reception": f"The aircraft is ready at {d_fbo}. The staff is prepared for your boarding.",
        "Flight Active / Taxiing": f"The aircraft is taxiing at {d_icao}. Real-time monitoring is active."
    }

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1px solid #eee; border-radius: 12px; overflow: hidden; margin: auto; background-color: #ffffff;">
        <div style="background-color: #000; padding: 25px; text-align: center;">
            <img src="{COMPANY_LOGO_URL}"
