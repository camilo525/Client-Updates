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
# Format: "ICAO": ["Airport Name", "City", "State/Country", "Timezone"]
AIRPORT_DB = {
    "KTEB": ["Teterboro Airport", "Teterboro", "NJ", "US/Eastern"],
    "KMIA": ["Miami International", "Miami", "FL", "US/Eastern"],
    "KOPF": ["Opa-Locka Executive", "Miami", "FL", "US/Eastern"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"],
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"],
    "VHHH": ["Hong Kong Intl", "Hong Kong", "HK", "Asia/Hong_Kong"],
    "EGSS": ["Stansted Airport", "London", "UK", "Europe/London"],
    "EGLF": ["Farnborough Airport", "Farnborough", "UK", "Europe/London"],
    "LFPN": ["Toussus-le-Noble", "Paris", "FR", "Europe/Paris"]
}

def get_airport_details(icao):
    # Returns [Name, City, State, Timezone] or defaults if not found
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- BLOCK 1: CLEAN DISPATCHER INPUTS ---
st.subheader("📍 1. Flight Itinerary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Departure")
    origin = st.text_input("Departure ICAO", placeholder="e.g. KTEB", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    
    if origin in AIRPORT_DB:
        st.caption(f"✅ **{dep_name}** | {dep_city}, {dep_state}")
    
    dep_time = st.text_input("Local Departure Time", placeholder="e.g. 10:00 AM")
    st.caption(
