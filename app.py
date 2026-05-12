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

# --- 4. GENERATOR FUNCTION (VERSION BLINDADA) ---
def generate_newsletter_html(m_stage, d_icao, d_city, d_fbo, d_time, a_icao, a_city, a_fbo, a_time, d_icon, d_msg, a_icon, a_msg, services, r_dep, r_arr):
    BRAND_COLOR = "#cb2d42"
    DARK_BAR = "#282522"
    
    svc_data = [
        {"label": "PETS", "active": services['pets']},
        {"label": "CATERING", "active": services['catering']},
        {"label": "GROUND TRANS.", "active": services['ground']},
        {"label": "RENTAL CAR", "active": services['rental']},
        {"label": "SPECIAL ASST.", "active": services['assist']}
    ]
    
    svc_items_html = ""
    for item in svc_data:
        bg = "#fff5f6" if item['active'] else "#f5f5f5"
        txt = BRAND_COLOR if item['active'] else "#bbbbbb"
        border = f"2px solid {BRAND_COLOR}" if item['active'] else f"2px solid {DARK_BAR}22"
        svc_items_html += f'<div style="display:inline-block; margin:5px; width:90px; padding:12px 0; border-radius:8px; background:{bg}; border:{border}; text-align:center;"><div style="font-size:18px; color:{txt}; font-weight:bold;">◈</div><div style="font-size:8px; color:{txt}; font-weight:bold; margin-top:4px; letter-spacing:0.5px;">{item["label"]}</div></div>'

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
        "Trip Coordination": "Please find attached the updated trip sheet reflecting the confirmed revisions and latest trip details.",
        "Repositioning Update": "The aircraft is currently in its repositioning phase, and all operations are proceeding as planned. We will provide an update once the aircraft is in position and ready to welcome you on board.",
        "FBO Arrival & Boarding Coordination": f"Aircraft is ready at {d_fbo}. The flight crew and FBO staff are standing by to assist with your arrival, check-in, and boarding process. <b>We would appreciate it if you could notify us when you are approximately 15 minutes away from the airport, enabling our crew to prepare for your timely departure.<b>",
        "Departure & Enroute Monitoring": "The aircraft is preparing for departure. Our team will continue monitoring the flight’s progress through active flight following. The Estimated Time Enroute is <b>XX:XX<b>."
    }

    # Construcción final del string
    html = f"""<div style="font-family: Arial, sans-serif; max-width: 550px; border: 2px solid {DARK_BAR}; border-radius: 15px; overflow: hidden; margin: auto; background-color: #ffffff;">
<div style="background-color: {DARK_BAR}; padding: 40px 20px; text-align: center;"><h2 style="color: #ffffff; margin: 0; font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 4px;">{m_stage}</h2></div>
<div style="padding: 40px; color: #333;">
<div style="text-align: center; margin-bottom: 35px; background: #f9f9f9; padding: 30px; border-radius: 12px;"><span style="font-size: 36px; font-weight: 800; color: #000;">{d_icao}</span><span style="color: {BRAND_COLOR}; font-size: 28px; margin: 0 20px;">✈</span><span style="font-size: 36px; font-weight: 800; color: #000;">{a_icao}</span><div style="font-size: 13px; color: #666; margin-top: 10px; font-weight: 600; text-transform: uppercase;">{d_city} TO {a_city}</div></div>
<p style="font-size: 16px; line-height: 1.6; color: #444; text-align: center;">{msg_map[m_stage]}</p>
{wx_display}
<div style="margin-top:30px; padding: 25px; border: 1px solid #eee; border-radius: 12px; background: #fafafa;"><div style="text-align:center; font-size:11px; color:#999; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px; font-weight:bold;">Logistics Status</div><div style="text-align:center;">{svc_items_html}</div></div>
<table width="100%" style="margin-top: 40px; border-top: 2px solid #eee; padding-top: 30px;"><tr>
<td style="width: 50%; vertical-align: top; border-right: 2px solid #eee; padding-right: 20px;"><div style="color: {BRAND_COLOR}; font-weight: 800; font-size: 10px; text-transform: uppercase;">Departure Info</div><b style="font-size: 18px; color: #000;">{d_time}</b><br><div style="margin-top: 5px; color: #555; font-size: 12px;">FBO: {d_fbo}</div>{ramp_tag(r_dep)}</td>
<td style="width: 50%; vertical-align: top; padding-left: 20px; text-align: right;"><div style="color: {BRAND_COLOR}; font-weight: 800; font-size: 10px; text-transform: uppercase;">Arrival Info</div><b style="font-size: 18px; color: #000;">{a_time}</b><br><div style="margin-top: 5px; color: #555; font-size: 12px;">FBO: {a_fbo}</div>{ramp_tag(r_arr)}</td>
</tr></table></div>
<div style="background-color: {DARK_BAR}; padding: 15px; text-align: center; font-size: 11px; color: #ffffff; letter-spacing: 1px;">Should you require any further assistance, please do not hesitate to reach back out to us.
</div>
</div>"""
    return html

# --- 5. ACTION BUTTON ---
st.markdown("---")
if st.button("Generate Executive Report"):
    if origin and destination:
        d_icon = WEATHER_ICONS.get(d_icon_key, "")
        a_icon = WEATHER_ICONS.get(a_icon_key, "")
        status = {'pets': s_pets, 'catering': s_catering, 'ground': s_ground, 'rental': s_rental, 'assist': s_assist}
        newsletter = generate_newsletter_html(milestone, origin, dep_city, dep_fbo, dep_time, destination, arr_city, arr_fbo, arr_time, d_icon, dep_wx_msg, a_icon, arr_wx_msg, status, ramp_dep, ramp_arr)
        st.components.v1.html(newsletter, height=1100)
    else:
        st.error("Please enter codes first.")
