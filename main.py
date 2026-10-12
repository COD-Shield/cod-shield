import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COD Shield | Spend & Cost Protection",
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
        "admin": {"daily_limit": 500, "used_today": 42, "balance": 7500.0, "total_attempts": 320, "saved_amount": 142000},
        "operator": {"daily_limit": 50, "used_today": 18, "balance": 450.0, "total_attempts": 85, "saved_amount": 34000}
    }

# Guaranteed Clean Ramp-Style CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6f4 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .ramp-hero-banner {
        background: linear-gradient(135deg, #0e3b2e 0%, #1f6f54 100%);
        padding: 35px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 30px rgba(14, 59, 46, 0.2);
        margin-bottom: 20px;
    }
    .ramp-section-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4b5563;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 6px;
    }
    .status-badge {
        background-color: #0e3b2e;
        color: #5fb88a;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 700; color: #0e3b2e;'>🛡️ COD Shield</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #4b5563; font-size: 13px;'>Protecting your margins, one delivery at a time.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In to Portal", type="primary", use_container_width=True):
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
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0, "saved_amount": 142000})
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Top Navigation Bar
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Protecting your margins, one delivery at a time.</span>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align: right;'><span class='status-badge'>● LIVE ({curr_user.upper()})</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ramp Style Hero Banner
    st.markdown("""
<div class="ramp-hero-banner">
<h1 style='margin:0; font-size: 34px; font-weight: 700; letter-spacing: -0.02em; color: white;'>Control your COD spend. Stop courier waste.</h1>
<p style='margin:10px 0 0 0; font-size: 16px; opacity: 0.9; color: white;'>Protect your gross margins by screening risky returners before dispatching packages and wasting two-way freight.</p>
<p style='margin:15px 0 0 0; font-size: 14px; font-style: italic; color: #a3e635; font-weight: 600;'>✨ "Protecting your margins, one delivery at a time."</p>
</div>
""", unsafe_allow_html=True)
    
    # Savings Counter Box
    c_box1, c_box2 = st.columns([1, 2])
    with c_box1:
        with st.container(border=True):
            st.markdown("<p style='font-size: 11px; color: #166534; text-transform: uppercase; font-weight: 700; margin:0;'>Total Estimated Budget Saved</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size: 26px; font-weight: 800; color: #0e3b2e; margin:5px 0 0 0;'>Rs. {wallet['saved_amount']:,}</h2>", unsafe_allow_html=True)

    # Section 1: Metrics Overview
    st.markdown('<div class="ramp-section-title">01 / Spend & Performance Overview</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL SCANS</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0e3b2e;'>{wallet['total_attempts']}</h2>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>QUOTA UTILIZED</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#2563eb;'>{wallet['used_today']} / {wallet['daily_limit']}</h2>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>REMAINING QUOTA</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#16a34a;'>{max(remaining_quota, 0)}</h2>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>WALLET BALANCE</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {wallet['balance']}</h2>", unsafe_allow_html=True)

    # Section 2: Financial Protection Breakdown
    st.markdown('<div class="ramp-section-title">02 / How COD Shield Protects Your Budget</div>', unsafe_allow_html=True)
    with st.container(border=True):
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            st.markdown("#### 📦 Stock Integrity")
            st.markdown("<span style='font-size: 13px; color: #4b5563;'>Prevent items from returning damaged or with torn packaging by stopping fake orders beforehand.</span>", unsafe_allow_html=True)
        with c_p2:
            st.markdown("#### 💸 Freight Savings")
            st.markdown("<span style='font-size: 13px; color: #4b5563;'>Cut down useless two-way courier shipping expenses that drain monthly operating cash flow.</span>", unsafe_allow_html=True)
        with c_p3:
            st.markdown("#### ⚡ Labor Efficiency")
            st.markdown("<span style='font-size: 13px; color: #4b5563;'>Save packing materials, bubble wrap, and team man-hours from being wasted on unverified buyers.</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
