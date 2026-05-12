import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 28px; font-weight: bold;
        background: -webkit-linear-gradient(#00d4ff, #005fcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 20px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
    label { color: #aaa !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- DATABASE ---
AIRPORT_DB = {
    "KTEB": ["Teterboro Airport", "Teterboro", "NJ", "US/Eastern"],
    "KMIA": ["Miami International", "Miami", "FL", "US/Eastern"],
    "KOPF": ["Opa-Locka Executive", "Miami", "FL", "US/Eastern"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"],
    "KASE": ["Aspen/Pitkin County", "Aspen", "CO", "US/Mountain"]
}

WEATHER_ICONS = {
    "Sunny": "☀️", "Partly Cloudy": "⛅", "Cloudy": "☁️", 
    "Rainy": "🌧️", "Thunderstorm": "⛈️", "Snowy": "❄️", "Foggy": "🌫️"
}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. INPUTS ---
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

# --- 2. WEATHER & SERVICES ---
dep_wx_msg, arr_wx_msg = "", ""
d_icon_key, a_icon_key = "Sunny", "Sunny"

if milestone == "Positioning Update":
    c_w1, c_w2 = st.columns(2)
    with c_w1:
        d_icon_key = st.selectbox("Dep Weather Icon", list(WEATHER_ICONS.keys()))
        dep_wx_msg = st.text_input("Dep Weather Brief")
    with c_w2:
        a_icon_key = st.selectbox("Arr Weather Icon", list(WEATHER_ICONS.keys()))
        arr_wx_msg = st.text_input("Arr Weather Brief")

st.subheader("⚙️ Ground & Concierge")
cs1, cs2, cs3 = st.columns(3)
with cs1: s_catering = st.checkbox("Catering Ready")
with cs2: s_ground = st.checkbox("Ground Transp.")
with cs3: s_rental = st.checkbox("Rental Car")

# --- 3. GENERATOR ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services):
    BRAND_COLOR = "#00d4ff"
    
    # Dashboard de Servicios
    svc_data = [
        {"icon": "◈", "label": "CATERING", "active": services['catering']},
        {"icon": "◈", "label": "TRANSPORT", "active": services['ground']},
        {"icon": "◈", "label": "RENTAL", "active": services['rental']}
    ]
    
    svc_html = "<div style='text-align:center;'>"
    for item in svc_data:
        bg = "#f0fbff" if item['active'] else "#f9f9f9"
        txt = BRAND_COLOR if item['active'] else "#cccccc"
        svc_html += f"""
        <div style="display:inline-block; margin:0 5px; width:90px; padding:8px 0; border-radius:6px; background:{bg}; border:1px solid {txt}; text-align:center;">
            <div style="font-size:16px; color:{txt}; font-weight:bold;">{item['icon']}</div>
            <div style="font-size:8px; color:{txt}; font-weight:bold; margin-top:2px;">{item['label']}</div>
        </div>"""
    svc_html += "</div>"

    # Bloque de Clima
    wx_display = ""
    if m_stage == "Positioning Update":
        wx_display = f"""
        <div style='margin-top:15px; display: table; width: 100%; border-collapse: separate;'>
            <div style='display: table-cell; width: 48%; padding:12px; background:#fcfcfc; border:1px solid #eee; border-radius:8px; text-align:center;'>
                <div style='font-size:24px; margin-bottom:5px;'>{d_icon}</div>
                <b style='font-size:9px; color:#999; text-transform:uppercase;'>Departure WX</b><br>
                <span style='font-size:12px; color:#333; font-weight:bold;'>{d_msg}</span>
            </div>
            <div style='display: table-cell; width: 4%;'></div>
            <div style='display: table-cell; width: 48%; padding:12px; background:#fcfcfc; border:1px solid #eee; border-radius:8px; text-align:center;'>
                <div style='font-size:24px; margin-bottom:5px;'>{a_icon}</div>
                <b style='font-size:9px; color:#999; text-transform:uppercase;'>Arrival WX</b><br>
                <span style='font-size:12px; color:#333; font-weight:bold;'>{a_msg}</span>
            </div>
        </div>"""

    msg_map = {
        "Trip Confirmation": "Flight details are confirmed for your upcoming mission.",
        "Positioning Update": "The aircraft is currently in the positioning phase.",
        "Aircraft Ready & FBO Reception": f"Aircraft is ready at {d_fbo}.",
        "Flight Active / Taxiing": "Aircraft is taxiing. Operational monitoring is live."
    }

    # RETORNO DE HTML (Cierre verificado)
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1.5px solid #444; border-radius: 10px; overflow: hidden; margin: auto; background-color: #ffffff;">
        <div style="background-color: #000; padding: 20px 10px; text-align: center;">
            <h2 style="color: #ffffff; margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px;">{m_stage}</h2>
        </div>
        <div style="padding: 25px; color: #333;">
            <div style="text-align: center; margin-bottom: 20px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
                <span style="font-size: 28px; font-weight: 800; color: #000;">{d_icao}</span>
                <span style="color: {BRAND_COLOR}; font-size: 22px; margin: 0 10px;">✈</span>
                <span style="font-size: 28px; font-weight: 800; color: #000;">{a_icao}</span>
                <div style="font-size: 11px; color: #666; font-weight: 600;">{d_city} TO {a_city}</div>
            </div>
            <p style="font-size: 14px; line-height: 1.4; color: #444; text-align: center; margin-bottom: 10px;">{msg_map[m_stage]}</p>
            {wx_display}
            <div style="margin-top:20px; padding: 15px; border: 1px solid #eee; border-radius: 8px; background: #fafafa;">
                {svc_html}
            </div>
            <table width="100%" style="margin-top: 20px; border-top: 1.5px solid #eee; padding-top: 15px;">
                <tr>
                    <td style="width: 50%; vertical-align: top; border-right: 1.5px solid #eee; padding-right: 10px;">
                        <div style="color: {BRAND_COLOR}; font-weight: bold; font-size: 9px; text-transform: uppercase;">Departure</div>
                        <b style="font-size: 15px; color: #000;">{d_time}</b><br>
                        <div
