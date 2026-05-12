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

# --- AUTO TIMEZONE LOGIC ---
# Professional mapping for major business aviation hubs (Example)
# In a full version, this can be expanded or linked to a database
ICAO_TIMEZONES = {
    "KTEB": "US/Eastern",
    "KMIA": "US/Eastern",
    "KLAX": "US/Pacific",
    "KLAS": "US/Pacific",
    "KOPF": "US/Eastern",
    "KASE": "US/Mountain",
    "VHHH": "Asia/Hong_Kong",
    "EGSS": "Europe/London",
    "EGLF": "Europe/London",
    "LFPN": "Europe/Paris"
}

def get_timezone_by_icao(icao):
    return ICAO_TIMEZONES.get(icao, "UTC") # Defaults to UTC if not found

# --- BLOCK 1: CLEAN DISPATCHER INPUTS ---
st.subheader("📍 Flight Itinerary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Departure")
    origin = st.text_input("Departure ICAO", placeholder="e.g. KTEB").upper()
    dep_time = st.text_input("Local Departure Time", placeholder="e.g. 10:00 AM")
    # AUTOMATIC SELECTION
    auto_dep_tz = get_timezone_by_icao(origin)
    st.caption(f"Detected Timezone: **{auto_dep_tz}**")

with col2:
    st.markdown("### Arrival")
    destination = st.text_input("Arrival ICAO", placeholder="e.g. KMIA").upper()
    arr_time = st.text_input("Local Arrival Time", placeholder="e.g. 02:30 PM")
    # AUTOMATIC SELECTION
    auto_arr_tz = get_timezone_by_icao(destination)
    st.caption(f"Detected Timezone: **{auto_arr_tz}**")

st.markdown("---")

if origin and destination:
    st.info(f"CONFIRMED: {origin} to {destination}")
    st.write(f"The system will lock the newsletter to: {auto_arr_tz}")
