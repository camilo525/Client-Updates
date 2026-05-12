import streamlit as st
import pytz
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (CONSOLE INTERFACE) ---
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
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
    label { color: #aaa !important; font-size: 14px !important; text-transform: uppercase; }
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

WEATHER_ICONS = {"Sunny": "☼", "Partly Cloudy": "☁", "Cloudy": "☁", "Rainy": "☂", "Thunderstorm": "⚡", "Snowy": "❄", "Foggy": "░"}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- INPUTS ---
st.subheader("📍 Flight Itinerary")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    _, dep_city, _, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", value="Signature Flight Support")
    dep_time = st.text_input("Departure Time", value="10:00 AM")
with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    _, arr_city, _, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Arrival Time", value="01:30 PM")

milestone = st.selectbox("Current Milestone", ["Trip Confirmation", "Positioning Update", "Aircraft Ready & FBO Reception", "Flight Active / Taxiing"])

# --- WEATHER & SERVICES ---
dep_wx_msg, arr_wx_msg = "", ""
d_icon_key, a_icon_key = "Sunny", "Sunny"
if milestone == "Positioning Update":
    c_w1, c_w2 = st.columns(2)
    with c_w1:
        d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Dep Brief")
    with c_w2:
        a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arr Brief")

st.subheader("⚙️ Ground & Concierge")
cs1, cs2, cs3 = st.columns(3)
with cs1: s_catering = st.checkbox("Catering")
with cs2: s_ground = st.checkbox("Ground Transp.")
with cs3: s_rental = st.checkbox("Rental Car")

# --- GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services):
    
    BRAND_COLOR = "#00d4ff"
    
    # Dashboard de Servicios Robusto
    svc_data = [
        {"icon": "◈", "label": "CATERING", "active": services['catering']},
        {"icon": "◈", "label": "TRANSPORT", "active": services['ground']},
        {"icon": "◈", "label": "RENTAL", "active": services['rental']}
    ]
    
    svc_html = "<div style='margin-top:20px; text-align:center;'>"
    for item in svc_data:
        bg = "#e6faff" if item['active'] else "#f5f5f5"
        txt = BRAND_COLOR if item['active'] else "#bbbbbb"
        border = f"2px solid {BRAND_COLOR}" if item['active'] else "2px solid #eeeeee"
        svc_html += f"""
        <div style="display:inline-block; margin:0 8px; width:100px; padding:12px 0; border-radius:8px; background:{bg}; border:{border}; text-align:center;">
            <div style="font-size:20px; color:{txt}; font-weight:bold;">{item['icon']}</div>
            <div style="font-size:9px; color:{txt}; font-weight:bold; margin-top:4px; letter-spacing:1px;">{item['label']}</div>
        </div>
        """
    svc_html += "</div>"

    # Mensaje de Estado
    msg_map = {
        "Trip Confirmation": "Confirmation of trip details and operational feasibility.",
        "Positioning Update": "Aircraft is currently in positioning phase. All schedules are on track.",
        "Aircraft Ready & FBO Reception": f"Aircraft is ready at {d_fbo}. Ground staff is on standby.",
        "Flight Active / Taxiing": "Aircraft has commenced taxi operations. Flight tracking is active."
    }

    wx_display = ""
    if m_stage == "Positioning Update":
        wx_display = f"""
        <div style='margin-top:25px; border-collapse: separate; display: table; width: 100%;'>
            <div style='display: table-cell; width: 48%; padding:20px; background:#fcfcfc; border:1px solid #eee; border-radius:10px; border-top:4px solid {BRAND_COLOR};'>
                <span style='font-size:24px; color:{BRAND_COLOR};'>{d_icon}</span><br>
                <b style='font-size:11px; color:#999; text-transform:uppercase;'>Departure WX</b><br>
                <span style='font-size:13px; color:#333; font-weight:500;'>{d_msg}</span>
            </div>
            <div style='display: table-cell; width: 4%;'></div>
            <div style='display: table-cell; width: 48%; padding:20px; background:#fcfcfc; border:1px solid #eee; border-radius:10px; border-top:4px solid {BRAND_COLOR};'>
                <span style='font-size:24px; color:{BRAND_COLOR};'>{a_icon}</span><br>
                <b style='font-size:11px; color:#999; text-transform:uppercase;'>Arrival WX</b><br>
                <span style='font-size:13px; color:#333; font-weight:500;'>{a_msg}</span>
            </div>
        </div>"""

    return f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 550px; border: 2px solid #333; border-radius: 15px; overflow: hidden; margin: auto; background-color: #ffffff; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <div style="background-color: #000; padding: 40px 20px; text-align: center;">
            <h2 style="color: #ffffff; margin: 0; font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 4px;">{m_stage}</h2>
        </div>
        <div style="padding: 40px; color: #333;">
            <div style="text-align: center; margin-bottom: 35px; background: #f9f9f9; padding: 30px; border-radius: 12px;">
                <span style="font-size: 36px; font-weight: 800; color: #000; letter-spacing: 1px;">{d_icao}</span>
                <span style="color: {BRAND_COLOR}; font-size: 28px; margin: 0 20px;">✈</span>
                <span style="font-size: 36px; font-weight: 800; color: #000; letter-spacing: 1px;">{a_icao}</span>
                <div style="font-size: 13px; color: #666; margin-top: 10px; font-weight: 600; text-transform: uppercase;">{d_city} TO {a_city}</div>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #444; text-align: center; font-weight: 400; padding: 0 10px;">{msg_map[m_stage]}</p>
            
            {wx_display}
            
            <div style="margin-top:40px; padding: 25px; border: 1px solid #eee; border-radius: 12px; background: #fafafa;">
                <div style="text-align:center; font-size:11px; color:#999; letter-spacing:2px; text-transform:uppercase; margin-bottom:15px; font-weight:bold;">Logistic Status</div>
                {svc_html}
            </div>

            <table width="100%" style="margin-top: 40px; border-top: 2px solid #eee; padding-top: 30px;">
                <tr>
                    <td style="width: 50%; vertical-align: top; border-right: 2px solid #eee; padding-right: 20px;">
                        <div style="color: {BRAND_COLOR}; font-weight: 800; font-size: 10px; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase;">Departure Info</div>
                        <b style="font-size: 18px; color: #000;">{d_time}</b><br>
                        <div style="margin-top: 5px; color: #555; font-size: 13px; font-weight: 500;">FBO: {d_fbo}</div>
                    </td>
                    <td style="width: 50%; vertical-align: top; padding-left: 20px; text-align: right;">
                        <div style="color: {BRAND_COLOR}; font-weight: 800; font-size: 10px; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase;">Arrival Info</div>
                        <b style="font-size: 18px; color: #000;">{a_time}</b><br>
                        <div style="margin-top: 5px; color: #555; font-size: 13px; font-weight: 500;">FBO: {a_fbo}</div>
                    </td>
                </tr>
            </table>
        </div>
        <div style="background-color: #333; padding: 15px; text-align: center; font-size: 11px; color: #fff; letter-spacing: 1px; font-weight: 600;">
            VIP OPERATIONAL UPDATE | PRIVATE AVIATION
        </div>
    </div>
    """

if st.button("Generate Robust Newsletter"):
    if origin and destination:
        d_icon = WEATHER_ICONS.get(d_icon_key, "")
        a_icon = WEATHER_ICONS.get(a_icon_key, "")
        services_status = {'catering': s_catering, 'ground': s_ground, 'rental': s_rental}
        html = generate_newsletter_html(milestone, origin, dep_city, dep_fbo, dep_time, dep_tz, destination, arr_city, arr_fbo, arr_time, arr_tz, d_icon, dep_wx_msg, a_icon, arr_wx_msg, services_status)
        st.components.v1.html(html, height=900)
    else:
        st.error("Please enter codes first.")
