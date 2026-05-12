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

# --- AIRPORT DATABASE ---
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

# --- 1. ITINERARY INPUTS ---
st.subheader("📍 1. Flight Itinerary")
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    dep_time = st.text_input("Local Departure Time (e.g. 10:00 AM)")

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    arr_name, arr_city, arr_state, arr_tz = get_airport_details(destination)
    arr_time = st.text_input("Local Arrival Time (e.g. 01:30 PM)")

# --- 2. MILESTONE SELECTOR ---
st.markdown("---")
st.subheader("🗓 2. Select Milestone")
milestone = st.selectbox("Current Stage", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

fbo_name = ""
if milestone == "Aircraft Ready & FBO Reception":
    fbo_name = st.text_input("FBO Name (e.g. Signature Flight Support)")

# --- 3. VIP NEWSLETTER GENERATOR (HTML) ---
def generate_newsletter_html(m_stage, org_city, dst_city, d_time, a_time, f_name):
    # Dynamic message based on milestone
    if m_stage == "Trip Confirmation":
        title = "TRIP CONFIRMATION"
        msg = "We have successfully processed your flight details. Your updated trip sheet is attached for your review."
    elif m_stage == "Positioning Update":
        title = "POSITIONING UPDATE"
        msg = f"Your aircraft is currently positioning to {org_city}. Operations are proceeding as scheduled."
    elif m_stage == "Aircraft Ready & FBO Reception":
        title = "AIRCRAFT READY"
        msg = f"The aircraft is fueled and ready at {f_name}. The FBO staff is prepared for your arrival and boarding."
    else:
        title = "FLIGHT ACTIVE"
        msg = f"The aircraft is taxiing at {org_city}. We are monitoring your flight in real-time until arrival at {dst_city}."

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1px solid #eee; border-radius: 12px; overflow: hidden; margin: auto; background-color: #ffffff;">
        <div style="background-color: #000; padding: 20px; text-align: center;">
            <h2 style="color: #00d4ff; margin: 0; font-size: 18px; letter-spacing: 2px;">{title}</h2>
        </div>
        <div style="padding: 25px; color: #333;">
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 22px; font-weight: bold;">{org_city}</span> 
                <span style="color: #00d4ff; font-size: 20px;"> ✈ </span> 
                <span style="font-size: 22px; font-weight: bold;">{dst_city}</span>
            </div>
            <p style="font-size: 14px; line-height: 1.6; color: #666;">{msg}</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <table width="100%" style="font-size: 13px;">
                <tr>
                    <td><b>Departure:</b> {d_time} (Local)</td>
                    <td style="text-align: right;"><b>Arrival:</b> {a_time} (Local)</td>
                </tr>
            </table>
        </div>
        <div style="background-color: #f8f8f8; padding: 10px; text-align: center; font-size: 10px; color: #aaa;">
            FLIGHT SUPPORT OPERATIONS | VIP SERVICES
        </div>
    </div>
    """

if st.button("Generate VIP Newsletter"):
    if origin and destination:
        st.markdown("### 📧 Preview (Copy & Paste to Gmail)")
        html_code = generate_newsletter_html(milestone, dep_city, arr_city, dep_time, arr_time, fbo_name)
        st.components.v1.html(html_code, height=450)
        st.info("💡 **How to send:** Highlight the card above with your mouse, copy it, and paste it directly into your Gmail thread.")
    else:
        st.error("Please enter Departure and Arrival ICAO first.")
