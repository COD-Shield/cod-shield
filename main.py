import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COD Risk Assessment & Merchant Protection Portal",
    page_icon="🛡️",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator"},
        "operator": {"password": "pass123", "role": "Operator"}
    }

if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "admin": {"daily_limit": 500, "used_today": 42, "balance": 7500.0, "total_attempts": 320},
        "operator": {"daily_limit": 50, "used_today": 18, "balance": 450.0, "total_attempts": 85}
    }

# Consistent Warm Paper Theme & Custom Banner Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f5f0 !important;
        color: #292524 !important;
    }
    .top-badge {
        background-color: #143825;
        color: #4ade80;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: #1c1917;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
    }
    /* Dynamic Cost-Saving Banner Style */
    .savings-banner {
        background: linear-gradient(135deg, #0f291e 0%, #163829 100%);
        border-left: 6px solid #4ade80;
        padding: 24px;
        border-radius: 14px;
        color: #ffffff;
        box-shadow: 0 10px 25px rgba(15, 41, 30, 0.15);
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .savings-banner h3 {
        color: #4ade80;
        margin-top: 0;
        font-size: 22px;
        font-weight: 800;
    }
    .section-header {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #78716c;
        font-weight: 700;
        border-bottom: 1px solid #e7e5e4;
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 20px;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #e7e5e4 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: #1c1917;'>🛡️ COD Shield Login</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #78716c; font-size:13px;'>Merchant Cost & Stock Protection Gateway</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Secure Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
else:
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 320})
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Header Bar
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("**🛡️ COD Shield Portal** &nbsp; <span style='color: #78716c; font-size: 13px;'>Merchant Protection Network</span>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align: right;'><span class='top-badge'>{curr_user.upper()}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hero Title & Motto
    st.markdown('<p class="hero-title">Better decisions, fewer returns.</p>', unsafe_allow_html=True)
    st.markdown("<p style='color: #57534e; font-size: 16px; margin-top:4px;'>Stop shipping blind. Save your stock, labor, and courier freight from chronic returners before dispatch.</p>", unsafe_allow_html=True)

    # 🌟 Interactive Merchant Cost-Saving Banner (Bilingual)
    st.markdown("""
        <div class="savings-banner">
            <h3>💰 How COD Shield Saves Your Money & Stock (آپ کے پیسے اور اسٹاک کی بچت کیسے ہوتی ہے؟)</h3>
            <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 12px;">
                <div style="flex: 1; min-width: 250px;">
                    <b>1. Pre-Dispatch Verification</b><br>
                    Check buyer history <i>before</i> packing. Filter out chronic returners to keep your stock safe from torn boxes and damaged inventory.<br>
                    <span style="color: #cbd5e1; font-size: 13px;">(آئٹم پیک کرنے سے پہلے کسٹمر کی ہسٹری چیک کریں اور ریٹرن کرنے والوں کو فلٹر کر کے اپنا اسٹاک محفوظ بنائیں۔)</span>
                </div>
                <div style="flex: 1; min-width: 250px;">
                    <b>2. Eliminate Two-Way Freight</b><br>
                    Stop paying double courier charges (dispatch + return) on fake orders that drain your monthly profit margins.<br>
                    <span style="color: #cbd5e1; font-size: 13px;">(فیک آرڈرز پر جانے اور واپس آنے والے دو طرفہ کوریئر کے کرایوں کے فضول خرچے سے جان چھٹائیں۔)</span>
                </div>
                <div style="flex: 1; min-width: 250px;">
                    <b>3. Save Labor & Packaging</b><br>
                    Stop wasting bubble wraps, boxes, tape, and employee hours on orders destined for rejection.<br>
                    <span style="color: #cbd5e1; font-size: 13px;">(ببل ریپ، ڈبے، ٹیپ اور لیبر کی محنت صرف ان خریداروں پر لگائیں جو واقعی پارسل لینا چاہتے ہیں۔)</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section 1: Metrics Overview
    st.markdown('<div class="section-header">01 / Operational Workspace Overview</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown("<p style='color:#78716c; font-size:12px; margin:0;'>TOTAL ATTEMPTS</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:5px 0 0 0; color:#1c1917;'>{wallet['total_attempts']}</h3>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<p style='color:#78716c; font-size:12px; margin:0;'>QUOTA USED</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:5px 0 0 0; color:#2563eb;'>{wallet['used_today']} / {wallet['daily_limit']}</h3>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<p style='color:#78716c; font-size:12px; margin:0;'>REMAINING QUOTA</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:5px 0 0 0; color:#16a34a;'>{max(remaining_quota, 0)}</h3>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<p style='color:#78716c; font-size:12px; margin:0;'>WALLET BALANCE</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:5px 0 0 0; color:#0d9488;'>Rs. {wallet['balance']}</h3>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out Securely", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
