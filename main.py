import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COD Shield | Executive & Risk Intelligence",
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

# Ramp-Inspired Two-Column Layout Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6f4 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .exec-heading {
        font-size: 32px;
        font-weight: 700;
        color: #0e3b2e;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }
    .exec-sub {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.5;
        margin-bottom: 20px;
    }
    .problem-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #ef4444;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
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
    # Top Navigation Bar for Landing
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Protecting your margins, one delivery at a time.</span>", unsafe_allow_html=True)
    with col_nav2:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>● V2.0 LIVE</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two Column Layout: Left (Executive Summary & Core Problem) | Right (Login Window)
    left_col, right_col = st.columns([1.5, 1], gap="large")

    with left_col:
        st.markdown('<p class="exec-heading">Executive Summary & Risk Intelligence</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="exec-sub">Cash on Delivery (COD) accounts for over 85% of retail transactions in South Asian e-commerce. However, chronic returners and fake orders cause severe financial bleeding. COD Shield is a collective pre-dispatch intelligence platform designed to eliminate blind shipping.</p>',
            unsafe_allow_html=True
        )

        st.markdown("#### 🚨 The Core Problem: Where Merchants Lose Money")
        
        st.markdown("""
        <div class="problem-box">
            <b>📦 Stock & Tear Damage</b><br>
            <span style="font-size: 13px; color: #4b5563;">Returned items frequently come back with crushed boxes, torn packaging, and unserviceable inventory that cannot be resold.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="problem-box">
            <b>💸 Two-Way Freight Drain</b><br>
            <span style="font-size: 13px; color: #4b5563;">Merchants pay double courier charges (dispatch + return transit) on every failed or refused delivery.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="problem-box">
            <b>👩‍🏭 Wasted Overhead & Labor</b><br>
            <span style="font-size: 13px; color: #4b5563;">Bubble wrap, custom boxes, tape, and employee man-hours are squandered on dead-end orders.</span>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 700; color: #0e3b2e; margin-bottom: 5px;'>🛡️ Merchant Portal Login</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #4b5563; font-size: 13px; margin-bottom: 20px;'>Sign in to access your risk screening workspace.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In Securely", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

else:
    # Logged-in Dashboard View
    curr_user = st.session_state.current_user
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0, "saved_amount": 142000})
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Protecting your margins, one delivery at a time.</span>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align: right;'><span class='status-badge'>● LIVE ({curr_user.upper()})</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dashboard Header & Savings Ticker
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0e3b2e 0%, #1f6f54 100%); padding: 30px; border-radius: 14px; color: white; margin-bottom: 20px;">
            <h1 style='margin:0; font-size: 32px; font-weight: 700;'>Operational Workspace Overview</h1>
            <p style='margin:8px 0 0 0; opacity: 0.9;'>Screening returners and preserving operating cash flow.</p>
        </div>
    """, unsafe_allow_html=True)

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
            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>ESTIMATED SAVINGS</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {wallet['saved_amount']:,}</h2>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
