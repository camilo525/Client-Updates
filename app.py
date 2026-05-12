import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VIP Milestone Console", layout="centered")

# --- UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-size: 32px; font-weight: bold;
        background: -webkit-linear-gradient(#cb2d42, #8e1e2d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 30px; letter-spacing: 2px;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"], div[data-baseweb="checkbox"], div[data-baseweb="radio"] { 
        background-color: #111 !important; border: 1px solid #333 !important; 
    }
    input, textarea, select { color: #cb2d42 !important; }
    label { color: #aaa !important; font-size: 14px !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">VIP MILESTONE CONSOLE</div>', unsafe_allow_html=True)

# --- AIRPORT DATABASE ---
AIRPORT_DB = {
    "KTEB": ["Teterboro", "Teterboro", "NJ", "US/Eastern"],
    "KHPN": ["Westchester Co", "White Plains", "NY", "US/Eastern"],
    "KFRG": ["Republic", "Farmingdale", "NY", "US/Eastern"],
    "KOPF": ["Opa-Locka Exec", "Miami", "FL", "US/Eastern"],
    "KMIA": ["Miami Intl", "Miami", "FL", "US/Eastern"],
    "KDAL": ["Dallas Love Field", "Dallas", "TX", "US/Central"],
    "KASE": ["Aspen/Pitkin Co", "Aspen", "CO", "US/Mountain"],
    "KVNY": ["Van Nuys", "Los Angeles", "CA", "US/Pacific"],
    "KLAX": ["Los Angeles Intl", "Los Angeles", "CA", "US/Pacific"],
    "KLAS": ["Harry Reid Intl", "Las Vegas", "NV", "US/Pacific"]
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
    dep_fbo = st.text_input("Departure FBO", value="")
    dep_time = st.text_input("Departure Time", value="")
    ramp_dep = st.radio("Dep. Ramp Access", ["Authorized", "Not Authorized"], horizontal=False)

with col2:
    destination = st.text_input("Arrival ICAO", key="dst").upper()
    _, arr_city, _, arr_tz = get_airport_details(destination)
    arr_fbo = st.text_input("Arrival FBO", value="")
    arr_time = st.text_input("Arrival Time", value="")
    ramp_arr = st.radio("Arr. Ramp Access", ["Authorized", "Not Authorized"], horizontal=False)

milestone = st.selectbox("Current Milestone", ["Trip Coordination", "Repositioning Update", "FBO Arrival & Boarding Coordination", "Departure & Enroute Monitoring"])

# --- 2. WEATHER ---
st.subheader("🌫️ Weather Assessment")
cw1, cw2 = st.columns(2)
with cw1:
    d_icon_key = st.selectbox("Dep Weather", list(WEATHER_ICONS.keys()))
    dep_wx_msg = st.text_input("Dep Brief", placeholder="Paste Executive report here")
with cw2:
    a_icon_key = st.selectbox("Arr Weather", list(WEATHER_ICONS.keys()))
    arr_wx_msg = st.text_input("Arr Brief", placeholder="Paste Executive report here")

# --- 3. SERVICES ---
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

# --- 4. GENERATOR (SEGMENTED FOR SAFETY) ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, d_tz, a_icao, a_city, a_fbo, a_time, a_tz, d_icon, d_msg, a_icon, a_msg, services, r_dep, r_arr):
    BRAND_COLOR = "#cb2d42"
    DARK_BAR = "#282522"
    
    # Mensajes
    msg_map = {
        "Trip Coordination": "Hello, ____________. We have updated the flight details accordingly. Please find attached the revised trip sheet for your review, reflecting the latest confirmed information.",
        "Repositioning Update": "The aircraft is currently in its repositioning phase. We will provide an update once the aircraft is in position and ready to welcome you on board. <b>We would appreciate it if you could notify us when you are approximately 15 minutes away from the airport, enabling our crew to prepare for your timely departure.</b>.",
        "FBO Arrival & Boarding Coordination": f"Aircraft is ready at {d_fbo}. The flight crew and FBO staff are standing by to assist with your arrival, check-in, and boarding process.",
        "Departure & Enroute Monitoring": "We noticed you are ready to depart, and our team will continue monitoring the flight’s progress through active flight following. The Estimated Time Enroute is: <b>XX hrs XX mins</b>."
    }

    # Servicios
    svc_items = ""
    for label, active in [("PETS", services['pets']), ("CATERING", services['catering']), ("GROUND", services['ground']), ("RENTAL", services['rental']), ("ASST", services['assist'])]:
        txt_c = BRAND_COLOR if active else "#bbbbbb"
        bg_c = "#fff5f6" if active else "#f5f5f5"
        svc_items += f'<div style="display:inline-block; margin:4px; width:85px; padding:10px 0; border-radius:8px; background:{bg_c}; border:1px solid {txt_c}; text-align:center;"><div style="font-size:16px; color:{txt_c};">◈</div><div style="font-size:8px; color:{txt_c}; font-weight:bold;">{label}</div></div>'

    # Clima
    wx_html = ""
    if m_stage != "Trip Confirmation":
        wx_html = f"""<div style="margin-top:20px; display:table; width:100%;">
            <div style="display:table-cell; width:48%; padding:15px; background:#fcfcfc; border:1px solid #eee; border-top:3px solid {BRAND_COLOR};">
                <span style="font-size:20px; color:{BRAND_COLOR};">{d_icon}</span><br><b style="font-size:10px; color:#999;">DEP WX</b><br><span style="font-size:12px;">{d_msg if d_msg else "Visual"}</span>
            </div>
            <div style="display:table-cell; width:4%;"></div>
            <div style="display:table-cell; width:48%; padding:15px; background:#fcfcfc; border:1px solid #eee; border-top:3px solid {BRAND_COLOR};">
                <span style="font-size:20px; color:{BRAND_COLOR};">{a_icon}</span><br><b style="font-size:10px; color:#999;">ARR WX</b><br><span style="font-size:12px;">{a_msg if a_msg else "Visual"}</span>
            </div></div>"""

    # Ramp Tag
    def r_tag(status):
        c = BRAND_COLOR if status == "Authorized" else "#999"
        return f'<div style="font-size:8px; color:{c}; font-weight:800; margin-top:5px;">• Plane-side vehicle access: {status}</div>'

    # Ensamblaje final
    header = f'<div style="background:{DARK_BAR}; padding:35px 20px; text-align:center;"><h2 style="color:#fff; margin:0; font-size:15px; letter-spacing:3px;">{m_stage.upper()}</h2></div>'
    body = f"""<div style="padding:35px; color:#333;">
        <div style="text-align:center; margin-bottom:30px; background:#f9f9f9; padding:25px; border-radius:12px;">
            <span style="font-size:32px; font-weight:800;">{d_icao}</span> <span style="color:{BRAND_COLOR}; font-size:24px; margin:0 15px;">〉</span> <span style="font-size:32px; font-weight:800;">{a_icao}</span>
            <div style="font-size:12px; color:#666; margin-top:8px; font-weight:600;">{d_city.upper()} TO {a_city.upper()}</div>
        </div>
        <p style="font-size:15px; line-height:1.5; color:#444; text-align:center;">{msg_map[m_stage]}</p>
        {wx_html}
        <div style="margin-top:25px; padding:20px; border:1px solid #eee; background:#fafafa; text-align:center;">
            <div style="font-size:10px; color:#999; letter-spacing:1px; margin-bottom:10px;">LOGISTICS STATUS</div>{svc_items}
        </div>
        <table width="100%" style="margin-top:30px; border-top:1px solid #eee; padding-top:20px;"><tr>
            <td style="width:50%; vertical-align:top; border-right:1px solid #eee; padding-right:15px;">
                <b style="color:{BRAND_COLOR}; font-size:10px;">DEPARTURE</b><br><b style="font-size:16px;">{d_time} ({d_tz})</b><br><div style="font-size:12px;">FBO: {d_fbo}</div>{r_tag(r_dep)}
            </td>
            <td style="width:50%; vertical-align:top; padding-left:15px; text-align:right;">
                <b style="color:{BRAND_COLOR}; font-size:10px;">ARRIVAL</b><br><b style="font-size:16px;">{a_time} ({a_tz})</b><br><div style="font-size:12px;">FBO: {a_fbo}</div>{r_tag(r_arr)}
            </td>
        </tr></table></div>"""
    footer = f'<div style="background:{DARK_BAR}; padding:15px; text-align:center; font-size:10px; color:#fff;">Should you require any further assistance, please do not hesitate to reach back out to us.</div>'

    return f'<div style="font-family:Arial; max-width:550px; border:1px solid {DARK_BAR}; margin:auto; background:#fff;">{header}{body}{footer}</div>'

# --- 5. ACTION ---
st.markdown("---")
if st.button("Generate Executive Report"):
    if origin and destination:
        d_icon = WEATHER_ICONS.get(d_icon_key, "")
        a_icon = WEATHER_ICONS.get(a_icon_key, "")
        status = {'pets': s_pets, 'catering': s_catering, 'ground': s_ground, 'rental': s_rental, 'assist': s_assist}
        newsletter = generate_newsletter_html(milestone, origin, dep_city, dep_fbo, dep_time, dep_tz, destination, arr_city, arr_fbo, arr_time, arr_tz, d_icon, dep_wx_msg, a_icon, arr_wx_msg, status, ramp_dep, ramp_arr)
        st.components.v1.html(newsletter, height=1000)
    else:
        st.error("Please enter codes first.")
