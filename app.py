import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
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
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #00d4ff !important; }
    label { color: #888 !important; font-size: 14px !important; }
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

# --- 1. ITINERARY ---
st.subheader("📍 1. Flight Itinerary")
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

# --- 2. MILESTONE ---
st.markdown("---")
milestone = st.selectbox("Select Current Milestone", [
    "Trip Confirmation",
    "Positioning Update",
    "Aircraft Ready & FBO Reception",
    "Flight Active / Taxiing"
])

# --- 3. WEATHER ASSESSMENT (PERMANENTE) ---
st.markdown("---")
st.subheader("🌫️ 3. Weather Assessment")
col_w1, col_w2 = st.columns(2)
with col_w1:
    d_icon_key = st.selectbox("Departure Condition", list(WEATHER_ICONS.keys()))
    dep_wx_msg = st.text_input("Dep Weather Brief")
with col_w2:
    a_icon_key = st.selectbox("Arrival Condition", list(WEATHER_ICONS.keys()))
    arr_wx_msg = st.text_input("Arr Weather Brief")

# --- 4. ADDITIONAL SERVICES ---
st.markdown("---")
st.subheader("⚙️ 4. Additional Services")
c1, c2, c3 = st.columns(3)
with c1:
    s_pets = st.checkbox("Pets on board")
    s_catering = st.checkbox("Catering")
with c2:
    s_ground = st.checkbox("Ground transportation")
    s_rental = st.checkbox("Rental")
with c3:
    s_assist = st.checkbox("Special Assistance")
    s_cargo = st.checkbox("Special Cargo")

# --- 5. GENERATOR FUNCTION ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services):
    BRAND_COLOR = "#00d4ff"
    svc_items = [
        ("Pets on board", services['pets']),
        ("Catering", services['catering']),
        ("Ground transportation", services['ground']),
        ("Rental", services['rental']),
        ("Special Assistance", services['assist']),
        ("Special Cargo", services['cargo'])
    ]
    
    # Construcción de servicios en una sola línea para evitar SyntaxError
    svc_html = "<div style='text-align:center; margin-top:10px;'>"
    for label, active in svc_items:
        color = BRAND_COLOR if active else "#cccccc"
        opacity = "1" if active else "0.2"
        border = f"1px solid {BRAND_COLOR}" if active else "1px solid #eeeeee"
        svc_html += f'<div style="display:inline-block; width:135px; margin:5px; padding:8px 2px; border-radius:4px; border:{border}; opacity:{opacity}; text-align:center;"><div style="font-size:12px; color:{color}; font-weight:bold;">◈</div><div style="font-size:8px; color:{color}; font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">{label}</div></div>'
    svc_html += "</div>"

    # Clima
    wx_section = f"""<div style='margin-top:15px; display: table; width: 100%;'><div style='display: table-cell; width: 48%; padding:12px; background:#fcfcfc; border:1px solid #eee; border-radius:8px; text-align:center;'><div style='font-size:20px;'>{d_icon}</div><b style='font-size:9px; color:#999;'>DEPARTURE WX</b><br><span style='font-size:11px; color:#333; font-weight:bold;'>{d_msg if d_msg else "Standard"}</span></div><div style='display: table-cell; width: 4%;'></div><div style='display: table-cell; width: 48%; padding:12px; background:#fcfcfc; border:1px solid #eee; border-radius:8px; text-align:center;'><div style='font-size:20px;'>{a_icon}</div><b style='font-size:9px; color:#999;'>ARRIVAL WX</b><br><span style='font-size:11px; color:#333; font-weight:bold;'>{a_msg if a_msg else "Standard"}</span></div></div>"""

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; border: 1.5px solid #444; border-radius: 10px; overflow: hidden; margin: auto; background-color: #ffffff;">
        <div style="background-color: #000; padding: 20px; text-align: center;"><h2 style="color: #00d4ff; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">{m_stage}</h2></div>
        <div style="padding: 25px; color: #333;">
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 26px; font-weight: bold;">{d_icao}</span>
                <span style="color: {BRAND_COLOR}; font-size: 20px; margin: 0 10px;">✈</span>
                <span style="font-size: 26px; font-weight: bold;">{a_icao}</span>
                <div
