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
        letter-spacing: 2px;
    }
    .stSelectbox div[data-baseweb="select"] { font-size: 18px !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #222 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
    label { color: #777 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 1px; }
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
    "Sunny": "☼", "Partly Cloudy": "☁", "Cloudy": "☁", 
    "Rainy": "☂", "Thunderstorm": "⚡", "Snowy": "❄", "Foggy": "░"
}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. ITINERARY & FBO INPUTS ---
st.subheader("📍 1. Flight Itinerary")
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    dep_name, dep_city, dep_state, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", value="Signature Flight Support")
    dep_time = st.text_input("Departure Time", value="10:00 AM")

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    arr_name, arr_city, arr_state, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Arrival Time", value="01:30 PM")

# --- 2. MILESTONE SELECTOR ---
st.markdown("---")
milestone = st.selectbox("Current Milestone", [
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
    st.subheader("🌫️ 3. Weather Briefing")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Dep Brief", placeholder="Operational info...")
    with col_w2:
        a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arr Brief", placeholder="Operational info...")

# --- 4. ADDITIONAL SERVICES ---
st.markdown("---")
st.subheader("⚙️ 4. Ground & Concierge")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    s_catering = st.checkbox("Catering Status")
with col_s2:
    s_ground = st.checkbox("Ground Transp.")
with col_s3:
    s_rental = st.checkbox("Rental Car")

# --- 5. NEWSLETTER GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services):
    
    # Icons Pro (Minimalistas)
    # Catering (Bowl/Plate), Ground (Luxury Sedan), Rental (Key/Car)
    svc_data = [
        {"icon": "◈", "label": "CATERING", "active": services['catering']},
        {"icon": "◈", "label": "TRANSPORT", "active": services['ground']},
        {"icon": "◈", "label": "RENTAL", "active": services['rental']}
    ]
    
    svc_html = "<div style='margin-top:15px; text-align:center;'>"
    for item in svc_data:
        color = "#00d4ff" if item['active'] else "#eeeeee"
        opacity = "1" if item['active'] else "0.2"
        border = f"1px solid {color}" if item['active'] else "1px solid #ddd"
        
        svc_html += f"""
        <div style="display:inline-block; margin:0 10px; padding:10px 15px; border-radius:4px; border:{border}; opacity:{opacity}; text-align:center;">
            <div style="font-size:18px; color:{color}; font-weight:bold;">{item['icon']}</div>
            <div style="font-size:8px; color:#555; margin-top:4px; letter-spacing:1px;">{item['label']}</div>
        </div>
        """
    svc_html += "</div>"

    if m_stage == "Trip Confirmation":
        title, msg = "TRIP CONFIRMATION", "We are pleased to confirm your upcoming flight. Your itinerary details are updated below."
        wx_display = ""
    elif m_stage == "Positioning Update":
        title, msg = "POSITIONING UPDATE", f"Your aircraft is currently positioning. All systems are operational for your departure."
        wx_display = f"""<div style='margin-top:20px; display: table; width: 100%;'>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#f9f9f9; border-radius:4px; border-top:3px solid #00d4ff;'>
                                <span style='font-size:20px; color:#00d4ff;'>{d_icon}</span><br>
                                <b style='font-size:10px; color:#888;'>DEPARTURE WX</b><br>
                                <span style='font-size:12px; color:#333;'>{d_msg}</span>
                            </div>
                            <div style='display: table-cell; width: 4%;'></div>
                            <div style='display: table-cell; width: 48%; padding:15px; background:#f9f9f9; border-radius:4px; border-top:3px solid #00d4ff;'>
                                <span style='font-size:20px; color:#00d4ff;'>{a_icon}</span><br>
                                <b style='font-size:10px; color:#888;'>ARRIVAL WX</b><br>
                                <span style='font-size:12px; color:#333;'>{a_msg}</span>
                            </div>
                         </div>"""
    else:
        title, msg = "FLIGHT STATUS", f"Operational update for your flight from {d_icao} to {a_icao}."
        wx_display = ""

    return f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 550px; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; margin: auto; background-color: #ffffff;">
        <div style="background-color: #111; padding: 30px 20px; text-align: center; letter-spacing: 3px;">
            <h2 style="color: #ffffff; margin: 0; font-size: 14px; font-weight: 300; text-transform: uppercase;">{title}</h2>
        </div>
        <div style="padding: 40px; color: #333;">
            <div style="text-align: center; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 30px;">
                <span style="font-size: 32px; font-weight: 200; color: #000; letter-spacing: 2px;">{d_icao}</span>
                <span style="color: #00d4ff; font-size: 24px; margin: 0 20px; position: relative; top: -4px;">⟶</span>
                <span style="font-size: 32px; font-weight: 200; color: #000; letter-spacing: 2px;">{a_icao}</span>
                <div style="font-size: 11px; color: #aaa; margin-top: 10px; text-transform: uppercase; letter-spacing: 1px;">{d_city} to {a_city}</div>
            </div>
            
            <p style="font-size: 15px; line-height: 1.7; color: #555; text-align: center; font-style: italic;">"{msg}"</p>
            
            {wx_display}
            
            <div style="margin-top:40px;">
                <div style="text-align:center; font-size:10px; color:#bbb; letter-spacing:2px; text-transform:uppercase; margin-bottom:15px;">Concierge & Logistics</div>
                {svc_html}
            </div>

            <table width="100%" style="margin-top: 40px; border-top: 1px solid #eee; padding-top: 30px; font-size: 12px; color: #444;">
                <tr>
                    <td style="width: 50%; vertical-align: top; border-right: 1px solid #eee; padding-right: 20px;">
                        <div style="color: #00d4ff; font-weight: bold; font-size: 9px; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase;">Departure Information</div>
                        <b style="font-size: 16px; color: #000;">{d_time}</b> <span style="font-size: 10px; color: #aaa;">{d_tz}</span><br>
                        <div style="margin-top: 8px; color: #666;">FBO: {d_fbo}</div>
                    </td>
                    <td style="width: 50%; vertical-align: top; padding-left: 20px; text-align: right;">
                        <div style="color: #00d4ff; font-weight: bold; font-size: 9px; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase;">Arrival Information</div>
                        <b style="font-size: 16px; color: #000;">{a_time}</b> <span style="font-size: 10px; color: #aaa;">{a_tz}</span><br>
                        <div style="margin-top: 8px; color: #666;">F
