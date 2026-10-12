import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal - Phase 1",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States for Phase 1
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator"}
    }
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

# ================= 1. SECURE LOGIN GATE (Phase 1) =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ COD Risk Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Phase 1: Core Secure Access</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db:
                    u_info = st.session_state.users_db[username]
                    if u_info["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_role = u_info["role"]
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password.")
                else:
                    st.error("❌ User not found.")
else:
    # ================= 2. MAIN DASHBOARD (Phase 1) =================
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
            <h2>COD Risk Assessment & Verification Portal</h2>
            <p>Phase 1: Single Order Verification & Secure Engine | Logged in as: <b>{st.session_state.current_user}</b> ({st.session_state.user_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"### 👤 User: {st.session_state.current_user}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Phase 1 Layout: Single Search / Verification Interface
    with st.container(border=True):
        st.markdown("### 🔍 Single Order / Customer Risk Check")
        col1, col2 = st.columns([2, 1])
        with col1:
            search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            check_btn = st.button("🚀 Check Risk Score", type="primary", use_container_width=True)

    if check_btn:
        if search_phone:
            # Dummy backend risk database check for Phase 1
            mock_db = {
                "0300-1234567": {"name": "Ali Khan", "city": "Lahore", "risk": "Low Risk", "returns": 1, "delivered": 25},
                "0300-7654321": {"name": "Usman Ahmed", "city": "Karachi", "risk": "High Risk", "returns": 12, "delivered": 5},
            }
            
            if search_phone in mock_db:
                data = mock_db[search_phone]
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Result Display Box
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    with st.container(border=True):
                        st.markdown("#### 📋 Customer Details")
                        st.write(f"**Name:** {data['name']}")
                        st.write(f"**City:** {data['city']}")
                        st.write(f"**Total Delivered:** {data['delivered']}");
                        st.write(f"**Total Returns:** {data['returns']}")
                
                with res_col2:
                    with st.container(border=True):
                        st.markdown("#### ⚡ Risk Assessment Result")
                        if data['risk'] == "Low Risk":
                            st.success(f"🟢 **Status: {data['risk']}**\n\nCustomer history is clean. Safe for COD.")
                        else:
                            st.error(f"🔴 **Status: {data['risk']}**\n\nHigh return ratio detected! Proceed with caution.")
            else:
                st.info("ℹ️ No prior record found for this number. Neutral status assigned.")
        else:
                st.warning("⚠️ Please enter a valid phone number or order ID to check.")
            
