import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="COD Shield | Risk Intelligence",
    page_icon="🛡️",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# Users Database with Status
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator", "status": "Active"},
        "merchant_ali": {"password": "pass123", "role": "Customer", "status": "Active"},
        "merchant_sara": {"password": "pass123", "role": "Customer", "status": "Active"}
    }

# User Wallets & Tiers Database
if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "merchant_ali": {"daily_limit": 1200, "used_today": 340, "balance": 45000.0, "total_attempts": 1150, "saved_amount": 340000, "tier": "Platinum 💎"},
        "merchant_sara": {"daily_limit": 500, "used_today": 120, "balance": 18000.0, "total_attempts": 650, "saved_amount": 142000, "tier": "Gold 🥇"}
    }

# Mock Database for Phone Lookups
if 'lookup_db' not in st.session_state:
    st.session_state.lookup_db = {
        "03001234567": {"risk": "HIGH", "score": "89%", "total": 14, "delivered": 3, "returned": 11, "comment": "Chronic returner across multiple courier networks. High COD refusal rate."},
        "03219876543": {"risk": "LOW", "score": "4%", "total": 22, "delivered": 21, "returned": 1, "comment": "Trusted buyer with clean fulfillment history. Safe for dispatch."},
        "03335554433": {"risk": "MEDIUM", "score": "45%", "total": 8, "delivered": 5, "returned": 3, "comment": "Moderate return frequency. Verify address via WhatsApp before dispatch."}
    }

# Dynamic Styling
hide_sidebar_css = """
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    .stApp {
        background-color: #f4f6f4 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 2rem !important;
    }
    .marquee-container {
        background: linear-gradient(135deg, #0e3b2e 0%, #1f6f54 100%);
        color: #a3e635;
        padding: 12px 0;
        border-radius: 8px;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 4px 15px rgba(14, 59, 46, 0.15);
        margin-bottom: 25px;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 0.03em;
    }
    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    .exec-heading {
        font-size: 30px;
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
    .footer-box {
        margin-top: 40px;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
        color: #6b7280;
        font-size: 12px;
        text-align: center;
        line-height: 1.6;
    }
"""

if not st.session_state.logged_in:
    hide_sidebar_css += """
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    """

hide_sidebar_css += "</style>"
st.markdown(hide_sidebar_css, unsafe_allow_html=True)

current_year = datetime.now().year

if not st.session_state.logged_in:
    # Landing Page Top Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([2.8, 1.4, 0.8])
    with col_nav1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #4b5563; font-size: 12px;'>— <b>We Protect your margins to avoid BLIND COD shipping.</b></span>", unsafe_allow_html=True)
    with col_nav2:
        selected_lang = st.selectbox("Language / زبان / لغة", ["English", "اردو", "العربية"], index=["English", "اردو", "العربية"].index(st.session_state.lang), label_visibility="collapsed")
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()
    with col_nav3:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>● V2.0 LIVE</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="marquee-container">
            <div class="marquee-text">
                🚨 STOP SHIPPING BLIND! &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>We Protect your margins to avoid BLIND COD shipping.</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Save your stock, labor, and courier freight before dispatch! &nbsp;&nbsp;&bull;&nbsp;&nbsp; 📦 Shield your e-commerce business today.
            </div>
        </div>
    """, unsafe_allow_html=True)

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

    with right_col:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 700; color: #0e3b2e; margin-bottom: 5px;'>🛡️ Portal Login</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #4b5563; font-size: 13px; margin-bottom: 20px;'>Sign in as Admin or Merchant.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In Securely", type="primary", use_container_width=True):
                if username in st.session_state.users_db:
                    user_info = st.session_state.users_db[username]
                    if user_info["status"] == "Disabled":
                        st.error("This account has been disabled by Admin.")
                    elif user_info["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_role = user_info["role"]
                        st.rerun()
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("User not found.")

    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b><br>
            COD Shield provides pre-dispatch risk intelligence based on historical data. We do not guarantee 100% delivery success or replace direct buyer confirmation. Merchants retain sole discretion over order dispatch decisions.
        </div>
    """, unsafe_allow_html=True)

else:
    curr_user = st.session_state.current_user
    user_role = st.session_state.user_role

    # ==================== ADMIN PORTAL ====================
    if user_role == "Administrator":
        with st.sidebar:
            st.markdown("### 👑 ADMIN CONTROL PANEL")
            st.markdown(f"<span style='color: #4b5563; font-size: 12px;'>Logged in as: <b>ADMIN</b></span>", unsafe_allow_html=True)
            st.markdown("---")
            admin_nav = st.radio("Admin Menu", ["Merchant Management", "Add New Merchant", "System Activity Logs"])
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

        if admin_nav == "Merchant Management":
            st.markdown("## 👥 Merchant Account Management")
            st.markdown("Monitor customer activities, adjust daily screening limits, disable/enable accounts, or delete merchants.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            for merchant_id in list(st.session_state.user_wallets.keys()):
                data = st.session_state.user_wallets[merchant_id]
                m_status = st.session_state.users_db[merchant_id]["status"]
                with st.container(border=True):
                    col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1.5, 1.5, 2])
                    with col_m1:
                        st.markdown(f"**Merchant:** `{merchant_id}`")
                        st.markdown(f"Status: **{m_status}** | Tier: **{data['tier']}**")
                    with col_m2:
                        new_limit = st.number_input(f"Limit ({merchant_id})", value=data['daily_limit'], step=50, key=f"lim_{merchant_id}")
                    with col_m3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Update Limit", key=f"upd_{merchant_id}", use_container_width=True):
                            st.session_state.user_wallets[merchant_id]['daily_limit'] = new_limit
                            st.success("Limit updated!")
                            st.rerun()
                    with col_m4:
                        st.markdown("<br>", unsafe_allow_html=True)
                        c_btn1, c_btn2, c_btn3 = st.columns(3)
                        with c_btn1:
                            if m_status == "Active":
                                if st.button("Disable", key=f"dis_{merchant_id}"):
                                    st.session_state.users_db[merchant_id]["status"] = "Disabled"
                                    st.rerun()
                            else:
                                if st.button("Enable", key=f"enb_{merchant_id}"):
                                    st.session_state.users_db[merchant_id]["status"] = "Active"
                                    st.rerun()
                        with c_btn2:
                            pass # spacing
                        with c_btn3:
                            if st.button("Delete", key=f"del_{merchant_id}", type="primary"):
                                del st.session_state.users_db[merchant_id]
                                del st.session_state.user_wallets[merchant_id]
                                st.success("Merchant deleted successfully!")
                                st.rerun()

        elif admin_nav == "Add New Merchant":
            st.markdown("## ➕ Onboard New Merchant Account")
            st.markdown("Create a new merchant profile with customized login credentials and screening limits.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(border=True):
                new_m_user = st.text_input("New Merchant Username")
                new_m_pass = st.text_input("New Merchant Password", type="password")
                new_m_limit = st.number_input("Initial Daily Screening Limit", value=200, step=50)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Create Merchant Account", type="primary", use_container_width=True):
                    if not new_m_user or not new_m_pass:
                        st.error("Please provide both username and password.")
                    elif new_m_user in st.session_state.users_db:
                        st.error("Merchant username already exists!")
                    else:
                        st.session_state.users_db[new_m_user] = {"password": new_m_pass, "role": "Customer", "status": "Active"}
                        st.session_state.user_wallets[new_m_user] = {"daily_limit": new_m_limit, "used_today": 0, "balance": 10000.0, "total_attempts": 5, "saved_amount": 1500, "tier": "Bronze 🥉"}
                        st.success(f"Merchant `{new_m_user}` created successfully!")

        elif admin_nav == "System Activity Logs":
            st.markdown("## 📊 System Activity & Audit Logs")
            st.markdown("Recent screening attempts across the network.")
            st.dataframe(pd.DataFrame([
                {"Time": "2026-10-12 20:15", "Merchant": "merchant_ali", "Phone": "03001234567", "Risk": "HIGH"},
                {"Time": "2026-10-12 19:42", "Merchant": "merchant_sara", "Phone": "03219876543", "Risk": "LOW"}
            ]), use_container_width=True)

    # ==================== CUSTOMER PORTAL ====================
    else:
        wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 500, "used_today": 0, "balance": 5000.0, "total_attempts": 0, "saved_amount": 10000, "tier": "Bronze 🥉"})
        
        # Automatic Tier Calculation
        if wallet['total_attempts'] >= 1000:
            wallet['tier'] = "Platinum 💎"
        elif wallet['total_attempts'] >= 300:
            wallet['tier'] = "Gold 🥇"
        elif wallet['total_attempts'] >= 100:
            wallet['tier'] = "Silver 🥈"
        else:
            wallet['tier'] = "Bronze 🥉"

        with st.sidebar:
            st.markdown("### 🛡️ COD SHIELD WORKSPACE")
            st.markdown(f"<span style='color: #4b5563; font-size: 12px;'>Merchant: <b>{curr_user.upper()}</b><br>Tier: <b>{wallet['tier']}</b></span>", unsafe_allow_html=True)
            st.markdown("---")
            
            nav_choice = st.radio("Navigation", ["Dashboard Overview", "Single Order Risk Check", "Bulk CSV Upload", "Wallet & Quota"])
            
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

        if nav_choice == "Dashboard Overview":
            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.markdown(f"**🛡️ Welcome Back, {curr_user.upper()}** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Tier: {wallet['tier']}</span>", unsafe_allow_html=True)
            with col_h2:
                st.markdown(f"<div style='text-align: right;'><span class='status-badge'>● LIVE</span></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class="marquee-container" style="margin-bottom: 20px;">
                    <div class="marquee-text">
                        🛡️ ACTIVE PROTECTION MODE &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>We Protect your margins to avoid BLIND COD shipping.</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Screen your orders before dispatch to save courier freight.
                    </div>
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
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#16a34a;'>{max(wallet['daily_limit'] - wallet['used_today'], 0)}</h2>", unsafe_allow_html=True)
            with m4:
                with st.container(border=True):
                    st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>ESTIMATED SAVINGS</p>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {wallet['saved_amount']:,}</h2>", unsafe_allow_html=True)

        elif nav_choice == "Single Order Risk Check":
            st.markdown("## 🔍 Single Order Risk Intelligence")
            st.markdown("Enter customer phone number to screen historical refusal patterns before dispatch.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.container(border=True):
                col_inp1, col_inp2 = st.columns([3, 1])
                with col_inp1:
                    search_query = st.text_input("Customer Phone Number (e.g. 03001234567 or try 03219876543)")
                with col_inp2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    search_btn = st.button("Screen Order", type="primary", use_container_width=True)

            if search_btn:
                if not search_query:
                    st.warning("Please enter a valid phone number.")
                elif wallet['used_today'] >= wallet['daily_limit']:
                    st.error("Daily quota exhausted! Please contact Admin for a limit upgrade.")
                else:
                    wallet['used_today'] += 1
                    wallet['total_attempts'] += 1
                    
                    result = st.session_state.lookup_db.get(search_query.strip(), {
                        "risk": "UNKNOWN", "score": "15%", "total": 2, "delivered": 1, "returned": 1, "comment": "New buyer with limited historical footprint. Proceed with standard verification."
                    })

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Risk Screening Result")

                    r1, r2, r3 = st.columns(3)
                    with r1:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>RISK LEVEL</p>", unsafe_allow_html=True)
                            risk_color = "#dc2626" if result['risk'] == "HIGH" else ("#16a34a" if result['risk'] == "LOW" else "#d97706")
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:{risk_color};'>{result['risk']} RISK</h2>", unsafe_allow_html=True)
                    with r2:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>PREDICTED REFUSAL RATE</p>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#2563eb;'>{result['score']}</h2>", unsafe_allow_html=True)
                    with r3:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL FULFILLMENTS</p>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0e3b2e;'>{result['delivered']} Delivered / {result['returned']} Returned</h2>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown("#### 📝 Network Intelligence Note")
                        st.markdown(f"<p style='color: #4b5563; font-size: 14px;'>{result['comment']}</p>", unsafe_allow_html=True)

        elif nav_choice == "Bulk CSV Upload":
            st.markdown("## 📦 Bulk Order Risk Upload")
            st.markdown("Upload your order manifest CSV file to screen hundreds of phone numbers instantly.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload CSV file containing phone numbers", type=["csv"])
            if uploaded_file is not None:
                df_upload = pd.read_csv(uploaded_file)
                st.success(f"Successfully uploaded {len(df_upload)} records for screening!")
                st.dataframe(df_upload.head(), use_container_width=True)
                if st.button("Run Bulk Risk Screening", type="primary"):
                    st.balloons()
                    st.info("Bulk scanning simulation complete: 85% safe orders identified for dispatch.")

        elif nav_choice == "Wallet & Quota":
            st.markdown("## 💳 Wallet & Quota Management")
            st.markdown(f"Your Account Classification: **{wallet['tier']}**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            w1, w2 = st.columns(2)
            with w1:
                with st.container(border=True):
                    st.markdown("### Account Details")
                    st.markdown(f"<h1 style='color: #16a34a;'>Rs. {wallet['balance']:,.2f}</h1>", unsafe_allow_html=True)
                    st.markdown(f"**Daily Screening Limit:** {wallet['daily_limit']} Scans")
                    st.markdown(f"**Used Today:** {wallet['used_today']} Scans")
            with w2:
                with st.container(border=True):
                    st.markdown("### Request Limit Enhancement")
                    st.markdown("Need a higher tier or increased daily limit? Request an upgrade directly from Admin.")
                    if st.button("Request Limit Upgrade", type="primary"):
                        st.success("Upgrade request sent to Admin successfully!")

    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b> &bull; Pre-dispatch Risk Intelligence Workspace.
        </div>
    """, unsafe_allow_html=True)
