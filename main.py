import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COD Shield | Intelligence & Merchant Protection",
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

# Anthropic-Inspired Minimalist Editorial Theme (Warm Cream, Sharp Typography, Clean Borders)
st.markdown("""
    <style>
    /* Anthropic Cream/Off-White Background */
    .stApp {
        background-color: #faf9f5 !important;
        color: #191919 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Top Minimalist Header */
    .anthropic-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e6e4dc;
        padding-bottom: 15px;
        margin-bottom: 30px;
    }
    
    /* Editorial Hero Title */
    .hero-headline {
        font-size: 48px;
        font-weight: 500;
        color: #111111;
        letter-spacing: -0.04em;
        line-height: 1.1;
        margin-bottom: 15px;
    }
    
    .hero-sub {
        font-size: 18px;
        color: #66635b;
        max-width: 750px;
        line-height: 1.5;
        margin-bottom: 30px;
    }

    /* Anthropic Style Cards (Clean, Subtle Border, No heavy shadows) */
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #e6e4dc !important;
        border-radius: 6px !important;
        padding: 20px !important;
        box-shadow: none !important;
    }

    /* Section Subheadings */
    .anthropic-section-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #8c887f;
        font-weight: 600;
        margin-top: 40px;
        margin-bottom: 15px;
        border-bottom: 1px solid #e6e4dc;
        padding-bottom: 8px;
    }

    /* Status Pill */
    .status-pill {
        background-color: #143825;
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.1, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 500; color: #111;'>🛡️ COD Shield</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #66635b; font-size: 13px;'>Secure Merchant Authentication</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In", type="primary", use_container_width=True):
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

    # Minimalist Top Nav Bar
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #8c887f; font-size: 13px;'>— Shared Trust & Risk Intelligence Network</span>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align: right;'><span class='status-pill'>● LIVE ({curr_user.upper()})</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Editorial Hero Section (Anthropic Style)
    st.markdown('<p class="hero-headline">Better decisions, fewer returns.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Stop shipping blind. Protect your stock, labor, and courier freight from chronic returners through collective network intelligence before dispatch.</p>', unsafe_allow_html=True)

    # Cost-Saving Insight Banner (Editorial Style)
    with st.container(border=True):
        st.markdown("#### 💡 Merchant Impact: How COD Shield Saves Your Capital")
        c_i1, c_i2, c_i3 = st.columns(3)
        with c_i1:
            st.markdown("**1. Pre-Dispatch Check**")
            st.markdown("<span style='font-size: 13px; color: #666;'>Filter out chronic returners before packing to save stock from torn boxes and waste.</span>", unsafe_allow_html=True)
        with c_i2:
            st.markdown("**2. Zero Two-Way Freight**")
            st.markdown("<span style='font-size: 13px; color: #666;'>Eliminate double courier shipping expenses on fake or unverified orders.</span>", unsafe_allow_html=True)
        with c_i3:
            st.markdown("**3. Protect Labor & Materials**")
            st.markdown("<span style='font-size: 13px; color: #666;'>Ensure bubble wrap, boxes, and team hours go only to genuine buyers.</span>", unsafe_allow_html=True)

    # Section 1: Metrics Overview
    st.markdown('<div class="anthropic-section-title">01 / Operational Workspace Metrics</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown("<p style='color:#8c887f; font-size:11px; font-weight:600;'>TOTAL ATTEMPTS</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:4px 0 0 0; font-weight:500;'>{wallet['total_attempts']}</h3>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<p style='color:#8c887f; font-size:11px; font-weight:600;'>QUOTA UTILIZED</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:4px 0 0 0; font-weight:500;'>{wallet['used_today']} / {wallet['daily_limit']}</h3>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<p style='color:#8c887f; font-size:11px; font-weight:600;'>REMAINING QUOTA</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:4px 0 0 0; font-weight:500; color:#16a34a;'>{max(remaining_quota, 0)}</h3>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<p style='color:#8c887f; font-size:11px; font-weight:600;'>WALLET BALANCE</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:4px 0 0 0; font-weight:500; color:#0d9488;'>Rs. {wallet['balance']}</h3>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
