import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="SMART TOURIST",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f7fb; }
.block-container { max-width: 1180px; padding-top: 1.2rem; padding-bottom: 3rem; }
.hero {
  background: linear-gradient(120deg, #102b46 0%, #176b75 58%, #55a69a 100%);
  color: white; padding: 2.2rem; border-radius: 24px; margin-bottom: 1.3rem;
}
.hero h1 { color: white; font-size: clamp(2rem, 5vw, 3.4rem); margin: 0; }
.hero p { color: #e5f5f3; font-size: 1.05rem; max-width: 700px; }
.pill { display:inline-block; background:#e3f3ef; color:#176b60; padding:5px 11px;
        border-radius:20px; font-size:0.8rem; font-weight:700; margin-bottom:10px; }
.small-muted { color:#667085; font-size:0.9rem; }
div[data-testid="stMetric"] { background:white; padding:14px; border-radius:16px; border:1px solid #e7ebf1; }
div[data-testid="stVerticalBlockBorderWrapper"] { background:white; border-radius:18px; }
.stButton > button { border-radius:12px; font-weight:700; min-height:2.7rem; }
</style>
""", unsafe_allow_html=True)

DESTINATIONS = [
    {"name":"Ooty, India","type":"Hill station","tag":"Nature","about":"Tea gardens, viewpoints, gardens and a scenic mountain railway.","budget":"Moderate","best":"October–June","icon":"🌿"},
    {"name":"Jaipur, India","type":"Heritage city","tag":"Culture","about":"Forts, palaces, markets, local crafts and Rajasthani food.","budget":"Moderate","best":"October–March","icon":"🏰"},
    {"name":"Goa, India","type":"Beach","tag":"Relaxation","about":"Beaches, coastal scenery, heritage areas and local cuisine.","budget":"Varies","best":"November–February","icon":"🏖️"},
    {"name":"Munnar, India","type":"Hill station","tag":"Nature","about":"Tea plantations, viewpoints, waterfalls and cool weather.","budget":"Moderate","best":"September–March","icon":"⛰️"},
    {"name":"Agra, India","type":"Heritage city","tag":"History","about":"Historic monuments, architecture and local markets.","budget":"Budget-friendly","best":"October–March","icon":"🕌"},
    {"name":"Singapore","type":"City","tag":"Family","about":"Gardens, museums, family attractions and efficient public transport.","budget":"Higher","best":"February–April","icon":"🌆"},
]

def init_state():
    defaults = {"plan": None, "checklist": {}, "saved": []}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="pill">ONE PLACE FOR YOUR WHOLE JOURNEY</div>
  <h1>SMART TOURIST 🌍</h1>
  <p>Less travel stress. More discovery. Plan, prepare and enjoy your trip with one simple travel companion.</p>
</div>
""", unsafe_allow_html=True)

pages = ["Discover", "Plan a trip", "My trip dashboard", "Travel checklist", "Travel tips"]
selected = st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")
st.write("")

# ---------- Discover ----------
if selected == "Discover":
    st.subheader("Find a place that feels right")
    st.caption("Explore sample destinations. In a full release, this section can connect to live destination, map and booking services.")
    c1, c2 = st.columns([2,1])
    with c1:
        query = st.text_input("Search destinations", placeholder="Try Ooty, Goa, Jaipur...")
    with c2:
        kind = st.selectbox("Travel style", ["All styles", "Nature", "Culture", "Relaxation", "History", "Family"])
    filtered = [d for d in DESTINATIONS if query.lower() in d["name"].lower()]
    if kind != "All styles":
        filtered = [d for d in filtered if d["tag"] == kind]
    cols = st.columns(3)
    for i, d in enumerate(filtered):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"## {d['icon']} {d['name']}")
                st.markdown(f"<span class='pill'>{d['type']}</span>", unsafe_allow_html=True)
                st.write(d["about"])
                st.caption(f"Budget: {d['budget']} · Best season: {d['best']}")
                if st.button("Add to saved places", key=f"save_{d['name']}", use_container_width=True):
                    if d["name"] not in st.session_state.saved:
                        st.session_state.saved.append(d["name"])
                    st.success("Saved to your places!")
    if not filtered:
        st.info("No sample destination found. Try another name.")

# ---------- Trip Planner ----------
elif selected == "Plan a trip":
    st.subheader("Build your trip in one place")
    st.write("Tell us the basics. SMART TOURIST will organize a starter plan and preparation checklist.")
    with st.form("trip_form"):
        a, b = st.columns(2)
        with a:
            traveller = st.text_input("Your name (optional)")
            destination = st.text_input("Where do you want to go?", placeholder="e.g. Ooty, Tamil Nadu")
            start = st.date_input("Start date", value=date.today() + timedelta(days=14), min_value=date.today())
            days = st.number_input("Trip duration (days)", 1, 30, 3)
        with b:
            people = st.number_input("Number of travellers", 1, 30, 2)
            budget = st.number_input("Approximate total budget (₹ or local currency)", min_value=0, value=15000, step=1000)
            style = st.multiselect("What do you enjoy?", ["Nature", "History", "Food", "Shopping", "Adventure", "Relaxation", "Family activities"])
            transport = st.selectbox("Preferred transport", ["Not decided", "Car", "Train", "Bus", "Flight", "Public transport"])
        notes = st.text_area("Anything we should consider?", placeholder="Accessibility needs, food preferences, places you want to visit, etc.")
        submitted = st.form_submit_button("✨ Create my trip plan", use_container_width=True)
    if submitted:
        if not destination.strip():
            st.error("Please enter a destination to create your plan.")
        else:
            st.session_state.plan = {
                "traveller": traveller.strip() or "Traveller",
                "destination": destination.strip(),
                "start": start,
                "days": int(days),
                "people": int(people),
                "budget": int(budget),
                "style": style,
                "transport": transport,
                "notes": notes.strip(),
            }
            st.session_state.checklist = {}
            st.success("Your starter trip plan is ready!")
            st.balloons()

# ---------- Dashboard ----------
elif selected == "My trip dashboard":
    st.subheader("Your trip at a glance")
    p = st.session_state.plan
    if not p:
        st.info("You haven't created a trip yet. Open **Plan a trip** to get started.")
    else:
        x, y, z = st.columns(3)
        x.metric("Destination", p["destination"])
        y.metric("Duration", f'{p["days"]} days')
        z.metric("Travellers", p["people"])
        st.markdown("### Your trip details")
        st.write(f"**Lead traveller:** {p['traveller']}")
        st.write(f"**Start date:** {p['start'].strftime('%d %B %Y')}")
        st.write(f"**Budget:** {p['budget']:,}")
        st.write(f"**Transport:** {p['transport']}")
        st.write("**Interests:** " + (", ".join(p["style"]) if p["style"] else "Not specified"))
        if p["notes"]:
            st.write("**Notes:**", p["notes"])
        st.markdown("### Simple day-by-day planner")
        for day in range(1, p["days"] + 1):
            with st.expander(f"Day {day} · {p['destination']}"):
                st.write("Morning: Choose one main attraction and check its opening hours.")
                st.write("Afternoon: Explore a nearby area or enjoy a local meal.")
                st.write("Evening: Keep time for rest and plan the next day.")
                st.caption("Starter suggestions only — confirm local details before travelling.")
        st.warning("This prototype does not book tickets, verify opening hours, or provide live route information.")

# ---------- Checklist ----------
elif selected == "Travel checklist":
    st.subheader("Your travel preparation checklist")
    st.caption("Tick items as you prepare. This demo keeps the checklist during the current app session.")
    groups = {
        "Before you leave": ["Confirm dates and bookings", "Check destination entry requirements", "Check weather forecast", "Share itinerary with a trusted person"],
        "Essentials": ["Valid ID and required travel documents", "Phone and charger", "Payment method and some emergency funds", "Regular medicines, if applicable", "Appropriate clothing"],
        "On the journey": ["Save accommodation address", "Keep emergency contacts available", "Check transport timings", "Respect local rules and customs"],
    }
    for group, items in groups.items():
        st.markdown(f"### {group}")
        for item in items:
            key = f"{group}_{item}"
            checked = st.checkbox(item, value=st.session_state.checklist.get(key, False), key=key)
            st.session_state.checklist[key] = checked
    total = sum(len(v) for v in groups.values())
    done = sum(bool(v) for v in st.session_state.checklist.values())
    st.progress(done / total)
    st.caption(f"{done} of {total} items completed")

# ---------- Tips ----------
elif selected == "Travel tips":
    st.subheader("Travel smarter and safer")
    tips = [
        ("Plan, but stay flexible", "Keep a realistic schedule and leave space for delays or rest."),
        ("Check trusted sources", "Verify current entry rules, transport schedules, ticket availability and attraction hours with official providers."),
        ("Keep important details handy", "Save accommodation details, local emergency numbers and a copy of essential travel documents securely."),
        ("Respect the destination", "Follow local rules, protect nature and be considerate of residents and local culture."),
        ("Watch your budget", "Include transport, food, tickets, accommodation and a small contingency amount."),
    ]
    for title, body in tips:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(body)

st.divider()
st.caption("SMART TOURIST · Prototype edition · Explore more, travel smart.")
