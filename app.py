import streamlit as st
import pytz
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#00d4ff, #005fcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
    }
    div[data-baseweb="input"] { background-color: #111 !important; border: 1px solid #333 !important; }
    input { color: #00d4ff !important; }
    label { color: #888 !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- ENHANCED AIRPORT DATABASE ---
AIRPORT_DB = {
    "KTEB": ["Teterboro Airport", "Teterboro", "NJ", "US/Eastern"],
    "KMIA": ["Miami International", "Miami", "FL", "US/Eastern"],
    "KOPF": ["Opa-Locka Executive", "Miami", "FL", "US/Eastern"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"],
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"]
}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. ITINERARY & FBO INPUTS ---
st.subheader("📍 1. Flight Itinerary & FBO Details")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Departure")
    origin = st.text_input("Departure ICAO", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", placeholder="e.g. Signature South")
    dep_time = st.text_input("Local Departure Time", placeholder="e.g. 10:00 AM")
    if origin: st.caption(f"Timezone: {dep_tz}")

with col2:
    st.markdown("### Arrival")
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    arr_name, arr_city, arr_state, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", placeholder="e.g. Jet Aviation")
    arr_time = st.text_input("Local Arrival Time", placeholder="e.g. 01:30 PM")
    if destination: st.caption(f"Timezone: {arr_tz}")

# --- 2. MILESTONE SELECTOR ---
st.markdown("---")
st.subheader("🗓 2. Select Milestone")
milestone = st.selectbox("Current Stage", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

# --- 3. VIP NEWSLETTER GENERATOR (HTML) ---
def generate_newsletter_html(m_stage, d_icao, d_name, d_city, d_fbo, d_time, d_tz, a_icao, a_name, a_city, a_fbo, a_time, a_tz):
    # Dynamic message logic
    if m_stage == "Trip Confirmation":
        title, msg = "TRIP CONFIRMATION", "Your flight details are confirmed. Please find your updated trip sheet attached."
    elif m_stage == "Positioning Update":
        title, msg = "POSITIONING UPDATE", f"The aircraft is currently positioning to {d_city} for your departure."
    elif m_stage == "Aircraft Ready & FBO Reception":
        title, msg = "AIRCRAFT READY", f"The aircraft is ready at {d_fbo}. The staff is waiting to assist you with boarding."
    else:
        title, msg = "FLIGHT ACTIVE", f"The aircraft is taxiing at {d_icao}. Real-time monitoring is active."

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1px solid #eee; border-radius: 12px; overflow: hidden; margin: auto; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        <div style="background-color:
