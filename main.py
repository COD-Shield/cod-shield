import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator"},
        "operator": {"password": "pass123", "role": "Operator"}
    }
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "admin": {"daily_limit": 50, "used_today": 12, "balance": 5000.0, "charges_per_check": 10.0},
        "operator": {"daily_limit": 20, "used_today": 5, "balance": 450.0, "charges_per_check": 10.0}
    }

if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": "10:15 AM", "User": "admin", "Action": "Single Check", "Cost": "Free Quota", "Status": "Success"},
        {"Timestamp": "10:40 AM", "User": "operator", "Action": "Bulk Check", "Cost": "Rs. 150 Deducted", "Status": "Success"},
    ]

# ================= 1. SECURE LOGIN GATE =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ COD Risk Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Secure Access & Role Management</p>", unsafe_allow_html=True)
            
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
    # ================= 2. DASHBOARD HEADER & SIDEBAR =================
    current_usr = st.session_state.current_user
    current_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(current_usr, {"daily_limit": 20, "used_today": 0, "balance": 500.0, "charges_per_check": 10.0})
    remaining_free = wallet['daily_limit'] - wallet['used_today']

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 22px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style='margin:0; font-size: 26px;'>🛡️ COD Risk Intelligence Portal</h1>
            <p style='margin:5px 0 0 0; font-size: 14px;'>Active User: <b>{current_usr}</b> ({current_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"### 👤 Profile: {current_usr}")
    st.sidebar.markdown(f"**Role:** {current_role}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 Wallet & Quota Status")
    st.sidebar.info(f"**Free Quota Left:** {max(remaining_free, 0)} / {wallet['daily_limit']}")
    st.sidebar.success(f"**Prepaid Balance:** Rs. {wallet['balance']}/-")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # TABS SETUP
    if current_role == "Administrator":
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Single Search (Access)", "📁 Bulk Upload & Download (Access)", "⚙️ Audit Logs", "👥 User Management"])
    else:
        # Operator Rights: Single Search Access + Bulk Upload Access (Download Restricted)
        tab1, tab2 = st.tabs(["🔍 Single Search Access", "📁 Bulk Upload Access (Restricted Download)"])

    # --- TAB 1: SINGLE SEARCH ACCESS (Both Admin & Operator) ---
    with tab1:
        with st.container(border=True):
            st.markdown("### 🔍 Single Order / Customer Risk Check")
            col1, col2 = st.columns([2, 1])
            with col1:
                search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                single_btn = st.button("🚀 Check Risk Score", type="primary", use_container_width=True)

        if single_btn:
            if search_phone:
                if remaining_free > 0:
                    wallet['used_today'] += 1
                else:
                    wallet['balance'] -= wallet['charges_per_check']
                
                st.session_state.audit_logs.insert(0, {"Timestamp": datetime.now().strftime("%I:%M %p"), "User": current_usr, "Action": f"Single Search ({search_phone})", "Cost": "Processed", "Status": "Success"})
                
                mock_db = {
                    "0300-1234567": {"name": "Ali Khan", "city": "Lahore", "risk": "Low Risk", "returns": 1, "delivered": 25},
                    "0300-7654321": {"name": "Usman Ahmed", "city": "Karachi", "risk": "High Risk", "returns": 12, "delivered": 5},
                }
                
                st.markdown("<br>", unsafe_allow_html=True)
                if search_phone in mock_db:
                    data = mock_db[search_phone]
                    res1, res2 = st.columns(2)
                    with res1:
                        with st.container(border=True):
                            st.markdown("#### 📋 Customer Summary")
                            st.write(f"**Name:** {data['name']}")
                            st.write(f"**City:** {data['city']}")
                            st.write(f"**Delivered:** {data['delivered']} | **Returns:** {data['returns']}")
                    with res2:
                        with st.container(border=True):
                            st.markdown("#### ⚡ Result")
                            if data['risk'] == "Low Risk":
                                st.success(f"🟢 **{data['risk']}** - Safe for COD.")
                            else:
                                st.error(f"🔴 **{data['risk']}** - High return ratio!")
                else:
                    st.info("ℹ️ No prior record found. Neutral status assigned.")
                st.rerun()
            else:
                st.warning("⚠️ Please enter a valid phone number.")

    # --- TAB 2: BULK UPLOADING / DOWNLOADING RIGHTS CONTROL ---
    if current_role == "Administrator":
        with tab2:
            st.markdown("### 📁 Bulk Verification, Processing & Report Downloading (Admin Full Access)")
            uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"], key="admin_bulk")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.success(f"✅ Total rows detected: {len(df)}")
                res_df = pd.DataFrame([{"Row": i+1, "Status": "Low Risk" if i%2==0 else "High Risk"} for i in range(len(df))])
                st.dataframe(res_df, use_container_width=True)
                # Admin has full downloading rights
                st.download_button("📥 Download Full Report (Admin Privilege)", data=res_df.to_csv(index=False).encode('utf-8'), file_name="risk_report.csv", mime="text/csv")

        with tab3:
            st.markdown("### ⚙️ System Audit Logs")
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True, hide_index=True)

        with tab4:
            st.markdown("### 👥 User Creation & Rights Management")
            with st.form("create_user"):
                u_name = st.text_input("Username")
                u_pass = st.text_input("Password", type="password")
                u_role = st.selectbox("Role", ["Operator", "Administrator"])
                if st.form_submit_button("Create User"):
                    if u_name and u_pass:
                        st.session_state.users_db[u_name] = {"password": u_pass, "role": u_role}
                        st.session_state.user_wallets[u_name] = {"daily_limit": 30, "used_today": 0, "balance": 500.0, "charges_per_check": 10.0}
                        st.success(f"User '{u_name}' created successfully!")
    else:
        # Operator View for Tab 2 (Bulk Uploading allowed, Downloading restricted)
        with tab2:
            st.markdown("### 📁 Bulk Uploading Access (Operator View)")
            st.markdown("You can upload files for batch risk evaluation. **Report downloading is restricted** for operator roles.")
            uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"], key="op_bulk")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.success(f"✅ Successfully processed {len(df)} records for verification.")
                res_df = pd.DataFrame([{"Row": i+1, "Status": "Low Risk" if i%2==0 else "High Risk"} for i in range(len(df))])
                st.dataframe(res_df, use_container_width=True)
                st.warning("🔒 **Download Restricted:** Operators cannot download raw report files. Contact Administrator for exports.")
