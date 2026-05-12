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
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"],
    "VHHH": ["Hong Kong Intl", "Hong Kong", "HK", "Asia/Hong_Kong"],
    "EGSS": ["Stansted Airport", "London", "UK", "Europe/London"],
    "EGLF": ["Farnborough Airport", "Farnborough", "UK", "Europe/London"],
    "LFPN": ["Toussus-le-Noble", "Paris", "FR", "Europe/Paris"]
}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- BLOCK 1: CLEAN DISPATCHER INPUTS ---
st.subheader("📍 1. Flight Itinerary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Departure")
    origin = st.text_input("Departure ICAO", placeholder="e.g. KTEB", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    
    # FIX: Only show caption if 'origin' is not empty
    if origin:
        if origin in AIRPORT_DB:
            st.caption(f"✅ **{dep_name}** | {dep_city}, {dep_state}")
        else:
            st.caption("ICAO not in database - Defaulting to UTC")
    
    dep_time = st.text_input("Local Departure Time", placeholder="e.g. 10:00 AM")
    if origin: st.caption(f"Timezone: **{dep_tz}**")

with col2:
    st.markdown("### Arrival")
    destination = st.text_input("Arrival ICAO", placeholder="e.g. KMIA", key="dst").upper()
    arr_name, arr_city, arr_state, arr_tz = get_airport_details(destination)
    
    # FIX: Only show caption if 'destination' is not empty
    if destination:
        if destination in AIRPORT_DB:
            st.caption(f"✅ **{arr_name}** | {arr_city}, {arr_state}")
        else:
            st.caption("ICAO not in database - Defaulting to UTC")
        
    arr_time = st.text_input("Local Arrival Time", placeholder="e.g. 02:30 PM")
    if destination: st.caption(f"Timezone: **{arr_tz}**")

st.markdown("---")

# --- BLOCK 2: MILESTONE SELECTOR ---
st.subheader("🗓 2. Select Flight Milestone")

milestone = st.selectbox("Current Stage", [
    "1. Trip Confirmation (Data Received)",
    "2. Final Itinerary (Tail & Crew assigned)",
    "3. Positioning & Weather (Ferry Flight)",
    "4. Aircraft Ready (FBO Reception)",
    "5. Pushing Back (Flight Active)"
])

st.markdown("---")
st.subheader("📝 3. Milestone Details")

# Logic to show specific inputs for each milestone
if "1." in milestone:
    st.info("Stage 1: Confirmation of data (Pax/Luggage). Weather not required.")

elif "2." in milestone:
    col_tail, col_crew = st.columns(2)
    with col_tail:
        tail_number = st.text_input("Tail Number", value="N").upper()
    with col_crew:
        crew_names = st.text_input("Crew Names", placeholder="e.g. Capt. Smith & FO Doe")

elif "3." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()
    st.warning("Weather API logic will be integrated in Block 4.")

elif "4." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()
    fbo_info = st.text_input("FBO Name & Reception Details", placeholder="e.g. Signature Flight Support")

elif "5." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()

# Internal success message
if origin and destination:
    st.success(f"Ready for: {milestone}")
