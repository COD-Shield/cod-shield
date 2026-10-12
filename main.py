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

# Consistent Warm Paper Theme & Custom Styling
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
    .hero-motto {
        font-size: 18px;
        font-weight: 700;
        color: #b91c1c;
        margin-top: 8px;
    }
    .hero-urdu {
        font-size: 15px;
        color: #57534e;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #78716c;
        font-weight: 700;
        border-bottom: 1px solid #e7e5e4;
        padding-bottom: 8px;
        margin-top: 30px;
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
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Header Bar
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("**🛡️ COD Shield Portal** &nbsp; <span style='color: #78716c; font-size: 13px;'>Merchant Protection Network</span>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align: right;'><span class='top-badge'>{curr_user.upper()}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hero Introduction & Bilingual Motto
    st.markdown('<p class="hero-title">Better decisions, fewer returns.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-motto">"Stop shipping blind. Save your stock, labor, and courier freight from chronic returners before dispatch."</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-urdu"><b>اردو:</b> اندھا دھند پارسل بھیجنا بند کریں۔ روانہ کرنے سے پہلے بار بار آرڈر واپس کرنے والوں سے اپنا اسٹاک، لیبر اور کوریئر کا خرچہ بچائیں۔</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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

    # Section 2: Why COD Shield Saves Merchant Money (Bilingual Impact Box)
    st.markdown('<div class="section-header">02 / Why Merchants Lose Money on COD & How We Save It</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        col_eng, col_urd = st.columns(2)
        with col_eng:
            st.markdown("#### 📉 Merchant Loss Factors")
            st.markdown("- **📦 Stock & Tear Damage:** Returned parcels often come back with torn boxes and crushed unsellable items.")
            st.markdown("- **💸 Two-Way Freight:** Paying double shipping charges on fake orders eats profit margins.")
            st.markdown("- **👩‍🏭 Wasted Labor:** Packing materials and employee time are wasted on fake orders.")
        with col_urd:
            st.markdown("#### 🇵🇰 مرچنٹ کا اصل نقصان اور بچت")
            st.markdown("- **📦 اسٹاک اور ڈبہ پھٹنے کا نقصان:** ریٹرن پارسل اکثر پھٹے ہوئے ڈبے اور ضائع شدہ مال کے ساتھ واپس آتے ہیں۔")
            st.markdown("- **💸 ڈبل کوریئر فریٹ:** فیک آرڈر پر آنے اور جانے کا دو طرفہ کرایہ پرافٹ کھا جاتا ہے۔")
            st.markdown("- **👩‍🏭 برباد لیبر اور پیکنگ:** پیکنگ کا سامان اور ٹیم کی محنت ضائع ہونے سے بچتی ہے۔")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out Securely", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
