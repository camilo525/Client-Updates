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
    .stSelectbox div[data-baseweb="select"] { font-size: 24px !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
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
st.subheader("🗓 2. Select Milestone")
milestone = st.selectbox("Current Stage", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

# --- 3. WEATHER ASSESSMENT ---
dep_wx_msg, arr_wx_msg = "", ""
d_icon_key, a_icon_key = "Sunny", "Sunny"

if milestone == "Positioning Update":
    st.markdown("---")
    st.subheader("🌫️ 3. Weather Assessment")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        d_icon_key = st.selectbox("Departure Icon", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Departure Brief", placeholder="e.g. Clear skies...")
    with col_w2:
        a_icon_key = st.selectbox("Arrival Icon", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arrival Brief", placeholder="e.g. Standard conditions...")

# --- 4. ADDITIONAL SERVICES (NEW SECTION) ---
st.markdown("---")
st.subheader("➕ 4. Additional Services")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    s_pax = st.checkbox("Pax Names Received")
    s_catering = st.checkbox("Catering Ready")
with col_s2:
    s_ground = st.checkbox("Ground Transp.")
    s_rental = st.checkbox("Rental Car")
with col_s3:
    s_driver = st.checkbox("Chauffeur Service")

# --- 5. VIP NEWSLETTER GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services):
    
    # Logic for Services Icons
    # Format: (Icon, Active_Status)
    svc_list = [
        ("👤", services['pax']),
        ("🍽️", services['catering']),
        ("🚘", services['ground']),
        ("🔑", services['rental']),
        ("👨‍✈️", services['driver'])
    ]
    
    svc_html = "<div style='margin-top:20px; text-align:center;'>"
    for icon, is_active in svc_list:
        color = "#00d4ff" if is_active else "#e0e0e033" # Brilla o se vuelve transparente
        opacity = "1" if is_active else "0.3"
        svc_html += f"<span style='font-size:24px; margin:0 10px; color:{color}; opacity:{opacity};'>{icon}</span>"
    svc_html += "</div>"

    if m_stage == "Trip Confirmation":
        title, msg = "TRIP CONFIRMATION", "Your flight details are confirmed. Please find your updated trip sheet attached."
        wx_display = ""
    elif m_stage == "Positioning Update":
        title, msg = "POSITIONING UPDATE", f"The aircraft is currently positioning. Operations are proceeding as scheduled."
        wx_display = f"""<div style='margin-top:20px; display: table; width: 100%;'>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#f4faff; border-radius:8px; border-left:4px solid #00d4ff;'>
                                <span style='font-size:24px;'>{d_icon}</span><br>
                                <b style='font-size:12px; color:#005fcc;'>DEPARTURE:</b><br>
                                <span style='font-size:13px; color:#444;'>{d_msg}</span>
                            </div>
                            <div style='display: table-cell; width: 4%;'></div>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#f4faff; border-radius:8px; border-left:4px solid #00d4ff;'>
                                <span style='font-size:24px;'>{a_icon}</span><br>
                                <b style='font-size:12px; color:#005fcc;'>ARRIVAL:</b><br>
                                <span style='font-size:13px; color:#444;'>{a_msg}</span>
                            </div>
                         </div>"""
    else:
        title, msg = "FLIGHT STATUS", f"Operational update for your flight from {d_icao} to {a_icao}."
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
            <div style="border-top:1px solid #eee; margin-top:20px; padding-top:10px;">
                <b style="font-size:10px; color:#888; letter-spacing:1px;">ADDITIONAL SERVICES</b>
                {svc_html}
            </div>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
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

# --- 6. ACTION ---
if st.button("Generate VIP Newsletter"):
    if origin and destination:
        st.markdown("### 📧 Gmail Briefing Preview")
        d_icon = WEATHER_ICONS.get(d_icon_key, "")
        a_icon = WEATHER_ICONS.get(a_icon_key, "")
        
        services_status = {
            'pax': s_pax, 'catering': s_catering, 
            'ground': s_ground, 'rental': s_rental, 'driver': s_driver
        }
        
        newsletter = generate_newsletter_html(
            milestone, origin, dep_city, dep_fbo, dep_time, dep_tz, 
            destination, arr_city, arr_fbo, arr_time, arr_tz,
            d_icon, dep_wx_msg, a_icon, arr_wx_msg, services_status
        )
        st.components.v1.html(newsletter, height=750)
    else:
        st.error("Please enter both Departure and Arrival ICAO.")
