import streamlit as st
import pytz
from datetime import datetime

# --- PAGE CONFIGURATION ---
# This sets the browser tab title and layout
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (VIP DARK MODE) ---
# Custom CSS to give it a high-end look
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#00d4ff, #005fcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
    }
    /* Input box styling */
    div[data-baseweb="input"] { background-color: #111 !important; border: 1px solid #333 !important; }
    input { color: #00d4ff !important; }
    label { color: #888 !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- BLOCK 1: CLEAN DISPATCHER INPUTS ---
st.subheader("📍 Flight Itinerary")

# Using columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Departure")
    origin = st.text_input("Departure ICAO", placeholder="e.g. KTEB").upper()
    dep_time = st.text_input("Local Departure Time", placeholder="e.g. 10:00 AM")
    # Searchable list of global time zones
    dep_tz = st.selectbox("Departure Time Zone", pytz.all_timezones, index=pytz.all_timezones.index('US/Eastern'))

with col2:
    st.markdown("### Arrival")
    destination = st.text_input("Arrival ICAO", placeholder="e.g. KMIA").upper()
    arr_time = st.text_input("Local Arrival Time", placeholder="e.g. 02:30 PM")
    # Crucial for the customer experience
    arr_tz = st.selectbox("Arrival Time Zone (Destination)", pytz.all_timezones, index=pytz.all_timezones.index('US/Eastern'))

st.markdown("---")

# Internal verification for the dispatcher
if origin and destination:
    st.info(f"FLIGHT DATA: {origin} ({dep_time}) to {destination} ({arr_time})")
    st.write(f"The customer will see time in: {arr_tz}")
