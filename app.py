import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN (CONSOLE INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#cb2d42, #8e1e2d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px;
        letter-spacing: 2px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"], div[data-baseweb="radio"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #cb2d42 !important; }
    label { color: #aaa !important; font-size: 14px !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- AIRPORT DATABASE (MASTER LIST) ---
AIRPORT_DB = {
    "KTEB": ["Teterboro", "Teterboro", "NJ", "US/Eastern"],
    "KHPN": ["Westchester Co", "White Plains", "NY", "US/Eastern"],
    "KFRG": ["Republic", "Farmingdale", "NY", "US/Eastern"],
    "KISP": ["Long Island Mac", "Islip", "NY", "US/Eastern"],
    "KBOS": ["Logan Intl", "Boston", "MA", "US/Eastern"],
    "KBED": ["Laurence Hanscom", "Bedford", "MA", "US/Eastern"],
    "KPHL": ["Philadelphia Intl", "Philadelphia", "PA", "US/Eastern"],
    "KPNE": ["Northeast Phila", "Philadelphia", "PA", "US/Eastern"],
    "KIAD": ["Dulles Intl", "Washington", "DC", "US/Eastern"],
    "KDCA": ["Reagan National", "Washington", "DC", "US/Eastern"],
    "KHEF": ["Manassas Regional", "Manassas", "VA", "US/Eastern"],
    "KOPF": ["Opa-Locka Exec", "Miami", "FL", "US/Eastern"],
    "KMIA": ["Miami Intl", "Miami", "FL", "US/Eastern"],
    "KTMB": ["Miami Exec", "Miami", "FL", "US/Eastern"],
    "KFXE": ["Ft Lauderdale Exec", "Ft Lauderdale", "FL", "US/Eastern"],
    "KFLL": ["Ft Lauderdale Intl", "Ft Lauderdale", "FL", "US/Eastern"],
    "KPBI": ["Palm Beach Intl", "West Palm Beach", "FL", "US/Eastern"],
    "KAPF": ["Naples Municipal", "Naples", "FL", "US/Eastern"],
    "KORL": ["Orlando Exec", "Orlando", "FL", "US/Eastern"],
    "KMCO": ["Orlando Intl", "Orlando", "FL", "US/Eastern"],
    "KTPA": ["Tampa Intl", "Tampa", "FL", "US/Eastern"],
    "KPDK": ["DeKalb-Peachtree", "Atlanta", "GA", "US/Eastern"],
    "KATL": ["Hartsfield-Jackson", "Atlanta", "GA", "US/Eastern"],
    "KCLT": ["Charlotte Douglas", "Charlotte", "NC", "US/Eastern"],
    "KDAL": ["Dallas Love Field", "Dallas", "TX", "US/Central"],
    "KADS": ["Addison", "Dallas", "TX", "US/Central"],
    "KDFW": ["Dallas/Fort Worth", "Dallas", "TX", "US/Central"],
    "KHOU": ["William Hobby", "Houston", "TX", "US/Central"],
    "KIAH": ["Bush Intercontinental", "Houston", "TX", "US/Central"],
    "KTME": ["Houston Exec", "Houston", "TX", "US/Central"],
    "KAUS": ["Austin-Bergstrom", "Austin", "TX", "US/Central"],
    "KORD": ["O'Hare Intl", "Chicago", "IL", "US/Central"],
    "KMDW": ["Midway Intl", "Chicago", "IL", "US/Central"],
    "KPWK": ["Chicago Exec", "Wheeling", "IL", "US/Central"],
    "KMSP": ["Minneapolis-St Paul", "Minneapolis", "MN", "US/Central"],
    "KMSY": ["Louis Armstrong", "New Orleans", "LA", "US/Central"],
    "KASE": ["Aspen/Pitkin Co", "Aspen", "CO", "US/Mountain"],
    "KEGE": ["Eagle County", "Vail", "CO", "US/Mountain"],
    "KAPA": ["Centennial", "Denver", "CO", "US/Mountain"],
    "KDEN": ["Denver Intl", "Denver", "CO", "US/Mountain"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"],
    "KVGT": ["North Las Vegas", "Las Vegas", "NV", "US/Pacific"],
    "KHND": ["Henderson Exec", "Las Vegas", "NV", "US/Pacific"],
    "KPHX": ["Sky Harbor Intl", "Phoenix", "AZ", "US/Mountain"],
    "KSDL": ["Scottsdale", "Scottsdale", "AZ", "US/Mountain"],
    "KSLC": ["Salt Lake City", "Salt Lake City", "UT", "US/Mountain"],
    "KVNY": ["Van Nuys", "Los Angeles", "CA", "US/Pacific"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KBUR": ["Bob Hope/Burbank", "Burbank", "CA", "US/Pacific"],
    "KSNA": ["John Wayne", "Santa Ana", "CA", "US/Pacific"],
    "KSAN": ["San Diego Intl", "San Diego", "CA", "US/Pacific"],
    "KCRQ": ["McClellan-Palomar", "Carlsbad", "CA", "US/Pacific"],
    "KSFO": ["San Francisco Intl", "San Francisco", "CA", "US/Pacific"],
    "KOAK": ["Oakland Intl", "Oakland", "CA", "US/Pacific"],
    "KSJC": ["San Jose Intl", "San Jose", "CA", "US/Pacific"],
    "KSQL": ["San Carlos", "San Carlos", "CA", "US/Pacific"],
    "KSEA": ["Seattle-Tacoma", "Seattle", "WA", "US/Pacific"],
    "KBFI": ["Boeing Field", "Seattle", "WA", "US/Pacific"]
}

WEATHER_ICONS = {"Sunny": "☼", "Partly Cloudy": "☁", "Cloudy": "☁", "Rainy": "☂", "Thunderstorm": "⚡", "Snowy": "❄", "Foggy": "░"}

def get_airport_details(icao):
    return AIRPORT_DB.get(icao, [icao, "Unknown City", "Unknown State", "UTC"])

# --- 1. ITINERARY INPUTS ---
st.subheader("📍 Flight Itinerary")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Departure ICAO", key="org").upper()
    _, dep_city, _, dep_tz = get_airport_details(origin)
    dep_fbo = st.text_input("Departure FBO", value="Signature Flight Support")
    dep_time = st.text_input("Departure Time", value="10:00 AM")
    ramp_dep = st.radio("Dep. Ramp Access", ["Authorized", "Not Authorized"], horizontal=True)

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    _, arr_city, _, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="Jet Aviation")
    arr_time = st.text_input("Arrival Time", value="01:30 PM")
    ramp_arr = st.radio("Arr. Ramp Access", ["Authorized", "Not Authorized"], horizontal=True)

milestone = st.selectbox("Current Milestone", ["Trip Coordination", "Repositioning Update", "FBO Arrival & Boarding Coordination", "Departure & Enroute Monitoring"])

# --- 2. WEATHER ASSESSMENT ---
st.subheader("🌫️ Weather Assessment")
cw1, cw2 = st.columns(2)
with cw1:
    d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
    dep_wx_msg = st.text_input("Dep Brief", placeholder="e.g. Clear Skies")
with cw2:
    a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
    arr_wx_msg = st.text_input("Arr Brief", placeholder="e.g. Standard conditions")

# --- 3. ADDITIONAL SERVICES ---
st.subheader("⚙️ Additional Services")
cs1, cs2, cs3 = st.columns(3)
with cs1: 
    s_pets = st.checkbox("Pets")
    s_catering = st.checkbox("Catering")
with cs2: 
    s_ground = st.checkbox("Ground Transportation")
    s_rental = st.checkbox("Rental Car")
with cs3:
    s_assist = st.checkbox("Special Assistance")

# --- 4. GENERATOR FUNCTION ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services, r_dep, r_arr):
    BRAND_COLOR = "#cb2d42"
    DARK_BAR = "#282522"
    
    svc_list = [
        ("PETS", services['pets']),
        ("CATERING", services['catering']),
        ("GROUND TRANS.", services['ground']),
        ("RENTAL CAR", services['rental']),
        ("SPECIAL ASST.", services['assist'])
    ]
    
    svc_items_html = ""
    for label, active in svc_list:
        bg = "#fff5f6" if active else "#f5f5f5"
        txt = BRAND_COLOR if active else "#bbbbbb"
        border = f"2px solid {BRAND_COLOR}" if active else f"2px solid {DARK_BAR}22"
        # Estilo segmentado para evitar SyntaxError
        svc_items_html += f'<div style="display:inline-block; margin:5px; width:90px; padding:12px 0; border-radius:8px; background:{bg}; border:{border}; text-align:center;">'
        svc_items_html += f'<div style="font-size:18px; color:{txt}; font-weight:bold;">◈</div>'
        svc_items_html += f'<div style="font-size:8px; color:{txt}; font-weight:bold; margin-top:4px; letter-spacing:0.5px;">{label}</div></div>'

    wx_display = ""
    if m_stage != "Trip Confirmation":
        wx_display = f"""<div style="margin-top:25px; display: table; width: 100%;">
<div style="display: table-cell; width: 48%; padding:20px; background:#fcfcfc; border:1px solid #eee; border-radius:10px; border-top:4px solid {BRAND_COLOR};"><span style="font-size:24px; color:{BRAND_COLOR};">{d_icon}</span><br><b style="font-size:11px; color:#999; text-transform:uppercase;">Departure WX</b><br><span style="font-size:13px; color:#333; font-weight:500;">{d_msg if d_msg else "Visual"}</span></div>
<div style="display: table-cell; width: 4%;"></div>
<div style="display: table-cell; width: 48%; padding:20px; background:#fcfcfc; border:1px solid #eee; border-radius:10px; border-top:4px solid {BRAND_COLOR};"><span style="font-size:24px; color:{BRAND_COLOR};">{a_icon}</span><br><b style="font-size:11px; color:#999; text-transform:uppercase;">Arrival WX</b><br><span style="font-size:13px; color:#333; font-weight:500;">{a_msg if a_msg else "Visual"}</span></div></div>"""

    def ramp_tag(status):
        color = BRAND_COLOR if status == "Authorized" else "#aaaaaa"
        return f'<div style="font-size:8px; color:{color}; font-weight:800; margin-top:6px; text-transform:uppercase;">• Plane-side vehicle access: {status}</div>'

    msg_map = {
        "Trip Coordination": "Hello, ___________, Please find attached the updated trip sheet reflecting the confirmed revisions and latest trip details.",
        "Repositioning Update": "The aircraft is currently in its repositioning phase, and all operations are proceeding as planned.",
        "FBO Arrival & Boarding Coordination": f"Aircraft is ready at {d_fbo}. The flight crew and FBO staff are standing by. <b>Please notify us when you are 15 minutes away.</b>",
        "Departure & Enroute Monitoring": "The aircraft is preparing for departure. We will continue monitoring the flight’s progress."
    }

    return f"""<div style="font-family: Arial, sans-serif; max-width: 550px; border: 2px solid {DARK_BAR}; border-radius: 15px; overflow: hidden; margin: auto; background-color: #ffffff;">
<div style="background-color: {DARK_BAR}; padding: 40px 20px; text-align: center;"><h2 style="color: #ffffff; margin:
