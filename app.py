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
        background: -webkit-linear-gradient(#00d4ff, #005fcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea { color: #00d4ff !important; }
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
st.subheader("🗓 2. Select Milestone")
milestone = st.selectbox("Current Stage", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

# --- BLOQUE 4: MANUAL WEATHER INPUT ---
# This appears if we are in Positioning stage to paste info from the other app
custom_weather = ""
if milestone == "Positioning Update":
    st.info("💡 Paste the 'Executive Weather Brief' from the OPS Tool below.")
    custom_weather = st.text_area("Weather Assessment", placeholder="e.g. Weather conditions are ideal for departure with clear skies...")

# --- 3. VIP NEWSLETTER GENERATOR (HTML) ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, wx_info):
    if m_stage == "Trip Confirmation":
        title, msg = "TRIP CONFIRMATION", "Your flight details are confirmed. Please find your updated trip sheet attached for your review."
        wx_display = ""
    elif m_stage == "Positioning Update":
        title, msg = "POSITIONING UPDATE", f"The aircraft is currently positioning to {d_city}. Operations are proceeding as scheduled."
        # Visual box for the weather brief
        wx_display = f"""<div style='margin-top:15px; padding:12px; background:#f4faff; border-radius:8px; border-left:4px solid #00d4ff;'>
                            <b style='font-size:12px; color:#005fcc;'>WEATHER ASSESSMENT:</b><br>
                            <span style='font-size:13px; color:#444;'>{wx_info}</span>
                         </div>""" if wx_info else ""
    elif m_stage == "Aircraft Ready & FBO Reception":
        title, msg = "AIRCRAFT READY", f"The aircraft is fueled and ready at {d_fbo}. The FBO staff is prepared to assist you with boarding."
        wx_display = ""
    else:
        title, msg = "FLIGHT ACTIVE", f"The aircraft is taxiing at {d_icao}. We are monitoring your flight in real-time until arrival."
        wx_display = ""

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1px solid #eee; border-radius: 12px; overflow: hidden; margin: auto; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        <div style="background-color: #000; padding: 20px; text-align: center;">
            <h2 style="color: #00d4ff; margin: 0; font-size: 16px; letter-spacing: 2px;">{title}</h2>
        </div>
        <div style="padding: 25px; color: #333;">
            <div style="text-align: center; margin-bottom: 25px;">
                <div style="font-size: 26px; font-weight: bold; color: #111;">{d_icao} <span style="color: #00d4ff;">✈</span> {a_icao}</div>
                <div style="font-size: 12px; color: #888; margin-top: 5px;">{d_city} to {a_city}</div>
            </div>
            <p style="font-size: 14px; line-height: 1.6; color: #444;">{msg}</p>
            {wx_display}
            <hr style="border: 0; border-top: 1px solid #eee; margin: 25px 0;">
            <table width="100%" style="font-size: 12px; border-collapse: collapse;">
                <tr>
                    <td style="width: 50%; padding-right: 10px; vertical-align: top;">
                        <div style="color: #00d4ff; font-weight: bold; font-size: 10px; margin-bottom: 5px;">DEPARTURE</div>
                        <b>{d_time}</b> ({d_tz})<br>
                        <span style="color:#666;">FBO: {d_fbo}</span>
                    </td>
                    <td style="width: 50%; padding-left: 10px; vertical-align: top; border-left: 1px solid #eee;">
                        <div style="color: #00d4ff; font-weight: bold; font-size: 10px; margin-bottom: 5px;">ARRIVAL</div>
                        <b>{a_time}</b> ({a_tz})<br>
                        <span style="color:#666;">FBO: {a_fbo}</span>
                    </td>
                </tr>
            </table>
        </div>
        <div style="background-color: #000; padding: 12px; text-align: center; font-size: 9px; color: #555; letter-spacing: 1px;">
            VIP FLIGHT SUPPORT | OPERATIONAL UPDATE
        </div>
    </div>
    """

# --- 4. ACTION BUTTON ---
if st.button("Generate VIP Newsletter"):
    if origin and destination:
        st.markdown("### 📧 Gmail Briefing Preview")
        newsletter = generate_newsletter_html(
            milestone, origin, dep_city, dep_fbo, dep_time, dep_tz, 
            destination, arr_city, arr_fbo, arr_time, arr_tz, custom_weather
        )
        st.components.v1.html(newsletter, height=550)
        st.info("💡 Highlight the card, copy it, and paste it into your Gmail thread.")
    else:
        st.error("Please enter both Departure and Arrival ICAO.")
