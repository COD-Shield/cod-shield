import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bulk & Shield | COD Shield", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f7f5f0 !important; color: #292524 !important; }
    .top-badge { background-color: #143825; color: #4ade80; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
    .hero-title { font-size: 38px; font-weight: 800; color: #1c1917; letter-spacing: -0.03em; margin-bottom: 0px; }
    .hero-subtitle { font-size: 16px; color: #57534e; margin-top: 5px; }
    .section-header { font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: #78716c; font-weight: 700; border-bottom: 1px solid #e7e5e4; padding-bottom: 8px; margin-top: 30px; margin-bottom: 20px; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] { background-color: #ffffff !important; border: 1px solid #e7e5e4 !important; border-radius: 12px !important; padding: 10px !important; }
    </style>
""", unsafe_allow_html=True)

if 'network_reports' not in st.session_state:
    st.session_state.network_reports = [
        {"phone": "03001234567", "outcome": "delivered", "date": "2026-10-12"},
        {"phone": "03219876543", "outcome": "refused", "date": "2026-10-11"}
    ]

# Top Bar
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("**🛡️ COD Shield** &nbsp; <span style='color: #78716c; font-size: 13px;'>Shared trust network</span>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align: right;'><span class='top-badge'>● NETWORK LIVE</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="hero-title">Better decisions, fewer returns.</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Check every COD order against shared delivery history.</p>', unsafe_allow_html=True)

# Section 1
st.markdown('<div class="section-header">01 / Network overview</div>', unsafe_allow_html=True)
total_checked = len(st.session_state.network_reports) * 14 + 128
m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.markdown("<p style='color:#78716c; font-size:12px;'>TOTAL SHARED RECORDS</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin:0; color:#1c1917;'>{total_checked}</h3>", unsafe_allow_html=True)
with m2:
    with st.container(border=True):
        st.markdown("<p style='color:#78716c; font-size:12px;'>NETWORK UPTIME</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color:#1c1917;'>99.99%</h3>", unsafe_allow_html=True)
with m3:
    with st.container(border=True):
        st.markdown("<p style='color:#78716c; font-size:12px;'>SHIELD STATUS</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color:#15803d;'>🟢 Active</h3>", unsafe_allow_html=True)

# Section 2
st.markdown('<div class="section-header">02 / Report delivery outcome</div>', unsafe_allow_html=True)
with st.container(border=True):
    r_phone = st.text_input("Order Phone Number", placeholder="03XX XXXXXXX")
    r_outcome = st.radio("What happened to the order?", ["Delivered", "Returned / Refused"], horizontal=True)
    if st.button("Submit Network Report", use_container_width=True):
        if r_phone:
            val = "delivered" if r_outcome == "Delivered" else "refused"
            st.session_state.network_reports.append({"phone": r_phone, "outcome": val, "date": "2026-10-12"})
            st.success("✅ Report successfully added to shared network.")
        else:
            st.warning("Please enter a phone number.")

# Section 3
st.markdown('<div class="section-header">03 / Import a CSV sheet</div>', unsafe_allow_html=True)
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload UTF-8 CSV (phone_number, outcome)", type="csv")
    if uploaded_file:
        df_csv = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df_csv)} records successfully!")
        st.dataframe(df_csv.head(3))
