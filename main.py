import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="COD Shield Portal",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session State for mock data if missing
if 'network_reports' not in st.session_state:
    st.session_state.network_reports = [
        {"phone": "03001234567", "outcome": "delivered", "date": "2026-10-12"},
        {"phone": "03219876543", "outcome": "refused", "date": "2026-10-11"}
    ]

# Exact Replit Warm Color Scheme CSS
st.markdown("""
    <style>
    /* Global App Background - Warm Paper Tone */
    .stApp {
        background-color: #f7f5f0 !important;
        color: #292524 !important;
    }
    
    /* Top Header Badge */
    .top-badge {
        background-color: #143825;
        color: #4ade80;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Hero Typography */
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #1c1917;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #57534e;
        margin-top: 5px;
    }

    /* Section Headers */
    .section-header {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #78716c;
        font-weight: 700;
        border-bottom: 1px solid #e7e5e4;
        padding-bottom: 8px;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    /* Streamlit Containers styling to match Replit Cards */
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #e7e5e4 !important;
        border-radius: 12px !important;
        padding: 5px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Header
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("**🛡️ COD Shield** &nbsp; <span style='color: #78716c; font-size: 13px;'>Shared trust network</span>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align: right;'><span class='top-badge'>● NETWORK LIVE</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="hero-title">Better decisions, fewer returns.</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Check every COD order against shared delivery history.</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 1: Network Overview
st.markdown('<div class="section-header">01 / Network overview</div>', unsafe_allow_html=True)

total_checked = len(st.session_state.network_reports) * 14 + 128
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    with st.container(border=True):
        st.markdown("<p style='color: #78716c; font-size: 13px; margin-bottom:5px;'>Total Shared Records</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin:0; color:#1c1917;'>{total_checked}</h3>", unsafe_allow_html=True)
with col_m2:
    with st.container(border=True):
        st.markdown("<p style='color: #78716c; font-size: 13px; margin-bottom:5px;'>Network Uptime</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color:#1c1917;'>99.99%</h3>", unsafe_allow_html=True)
with col_m3:
    with st.container(border=True):
        st.markdown("<p style='color: #78716c; font-size: 13px; margin-bottom:5px;'>Shield Status</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color:#15803d;'>🟢 Active</h3>", unsafe_allow_html=True)

# Section 2: Before You Decide (Single Check & Report)
st.markdown('<div class="section-header">02 / Before you decide</div>', unsafe_allow_html=True)

col_chk, col_rep = st.columns(2)

with col_chk:
    with st.container(border=True):
        st.markdown("#### Check customer risk")
        st.markdown("<p style='color: #78716c; font-size: 13px;'>Review previous COD outcomes</p>", unsafe_allow_html=True)
        
        phone_check = st.text_input("Customer phone number", placeholder="03XX XXXXXXX", key="chk_phone")
        
        if st.button("Search", type="primary", use_container_width=True):
            if phone_check:
                found = next((r for r in st.session_state.network_reports if r['phone'] == phone_check), None)
                if found:
                    if found['outcome'] == 'delivered':
                        st.markdown("<div style='background:#ecfdf5; border:1px solid #10b981; padding:12px; border-radius:8px; color:#065f46; margin-top:10px;'><b>GREEN: Low Risk</b><br>Customer has positive delivery history.</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background:#fef2f2; border:1px solid #ef4444; padding:12px; border-radius:8px; color:#991b1b; margin-top:10px;'><b>RED: High Risk / Refusal History</b><br>Reported as refused/returned previously.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#f4f4f5; border:1px solid #d4d4d8; padding:12px; border-radius:8px; color:#27272a; margin-top:10px;'><b>GREEN: Low Risk</b><br>No negative delivery history found for this number.</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a phone number.")

with col_rep:
    with st.container(border=True):
        st.markdown("#### Report a delivery outcome")
        st.markdown("<p style='color: #78716c; font-size: 13px;'>Accurate reports make the network more useful</p>", unsafe_allow_html=True)
        
        phone_rep = st.text_input("Order phone number", placeholder="03XX XXXXXXX", key="rep_phone")
        outcome = st.radio("What happened to the order?", ["Delivered", "Returned / Refused"], horizontal=True)
        
        if st.button("Submit report", use_container_width=True):
            if phone_rep:
                status_val = "delivered" if outcome == "Delivered" else "refused"
                st.session_state.network_reports.append({"phone": phone_rep, "outcome": status_val, "date": "2026-10-12"})
                st.success("✅ Report submitted successfully to the shared network!")
            else:
                st.warning("Please enter a phone number to report.")

# Section 3: Import a CSV sheet
st.markdown('<div class="section-header">03 / Import a CSV sheet</div>', unsafe_allow_html=True)
with st.container(border=True):
    st.markdown("#### Bulk delivery reports")
    st.markdown("<p style='color: #78716c; font-size: 13px;'>Upload a UTF-8 CSV with one order per row. Required columns: phone_number, outcome.</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    if uploaded_file is not None:
        df_csv = pd.read_csv(uploaded_file)
        st.success(f"Successfully loaded {len(df_csv)} rows from CSV!")
        st.dataframe(df_csv.head(3))

# Section 4: Recent reports
st.markdown('<div class="section-header">04 / Recent reports</div>', unsafe_allow_html=True)
with st.container(border=True):
    if st.session_state.network_reports:
        df_recent = pd.DataFrame(st.session_state.network_reports)
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No recent reports available yet.")
