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
# --- BLOCK 2: MILESTONE SELECTOR ---
st.subheader("🗓 2. Select Flight Milestone")

# This dropdown controls the entire newsletter content
milestone = st.selectbox("Current Stage", [
    "1. Trip Confirmation (Data Received)",
    "2. Final Itinerary (Tail & Crew assigned)",
    "3. Positioning & Weather (Ferry Flight)",
    "4. Aircraft Ready (FBO Reception)",
    "5. Pushing Back (Flight Active)"
])

# Variables that change based on selection
tail_number = ""
crew_names = ""
fbo_info = ""

st.markdown("---")
st.subheader("📝 3. Milestone Details")

# Logic to show specific inputs for each milestone
if "1." in milestone:
    st.info("Stage 1: Confirmation of data (Pax/Luggage). Weather not required.")
    st.write("Newsletter will focus on: *'Data received and Trip Sheet updated.'*")

elif "2." in milestone:
    col_tail, col_crew = st.columns(2)
    with col_tail:
        tail_number = st.text_input("Tail Number", value="N").upper()
    with col_crew:
        crew_names = st.text_input("Crew Names", placeholder="e.g. Capt. Smith & FO Doe")
    st.write("Newsletter will focus on: *'Final tail and crew assignments.'*")

elif "3." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()
    st.warning("Weather API logic will be integrated here in Block 4.")
    st.write("Newsletter will focus on: *'Ferry flight progress and weather report.'*")

elif "4." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()
    fbo_info = st.text_input("FBO Name & Reception Details", placeholder="e.g. Signature Flight Support - Main Lobby")
    st.write("Newsletter will focus on: *'Aircraft fueled, ready, and FBO staff waiting.'*")

elif "5." in milestone:
    tail_number = st.text_input("Tail Number", value="N").upper()
    st.write("Newsletter will focus on: *'Taxiing and real-time flight tracking.'*")

# Internal summary for the Dispatcher
st.success(f"Dispatcher selected: {milestone}")
