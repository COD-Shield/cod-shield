import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal - Complete System",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# INITIALIZE SESSION STATES (Phases 1, 2 & 3 Combined)
# ==========================================
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

# Phase 2 & 3: Quotas & Wallets
if 'user_quotas' not in st.session_state:
    st.session_state.user_quotas = {
        "admin": {"daily_limit": 500, "used_today": 12},
        "operator": {"daily_limit": 50, "used_today": 5}
    }

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

# ==========================================
# PHASE 1: SECURE LOGIN GATE
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ COD Risk Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Phase 1 + Phase 2 + Phase 3 Combined</p>", unsafe_allow_html=True)
            
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
    # ==========================================
    # DASHBOARD HEADER & SIDEBAR WIDGETS
    # ==========================================
    current_usr = st.session_state.current_user
    current_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(current_usr, {"daily_limit": 20, "used_today": 0, "balance": 500.0, "charges_per_check": 10.0})
    remaining_free = wallet['daily_limit'] - wallet['used_today']

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 22px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style='margin:0; font-size: 26px;'>🛡️ COD Risk Intelligence Portal</h1>
            <p style='margin:5px 0 0 0; font-size: 14px;'>Active User: <b>{current_usr}</b> ({current_role}) | All Phases Active</p>
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

    # ==========================================
    # TABS SETUP (Role Based Access)
    # ==========================================
    if current_role == "Administrator":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Interactive Analytics", 
            "🔍 Single Search Check", 
            "📁 Bulk Verification & Shield", 
            "⚙️ Audit Logs", 
            "👥 User Management"
        ])
    else:
        tab1, tab2, tab3 = st.tabs([
            "📊 Interactive Analytics", 
            "🔍 Single Search Access", 
            "📁 Bulk Upload Access (Restricted Download)"
        ])

    # --- TAB 1: INTERACTIVE ANALYTICS (Phase 2 & 3) ---
    with tab1:
        st.markdown("### 📈 Real-Time Performance & Risk Analytics")
        
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            st.metric(label="📊 Free Quota Used", value=wallet['used_today'])
        with col_k2:
            st.metric(label="💰 Wallet Balance", value=f"Rs. {wallet['balance']}")
        with col_k3:
            st.metric(label="🟢 Safe / Low Risk", value="78%", delta="+4%")
        with col_k4:
            st.metric(label="⚡ Security Shield", value="Active 🛡️")

        st.markdown("<br>", unsafe_allow_html=True)

        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            with st.container(border=True):
                st.markdown("#### Risk Distribution Breakdown")
                risk_chart_data = pd.DataFrame({
                    'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
                    'Count': [145, 42, 31]
                })
                st.bar_chart(risk_chart_data.set_index('Risk Level'))
        
        with c_chart2:
            with st.container(border=True):
                st.markdown("#### Recent System Logs")
                log_preview_df = pd.DataFrame(st.session_state.audit_logs)[['Timestamp', 'User', 'Action', 'Cost']]
                st.dataframe(log_preview_df, use_container_width=True, hide_index=True)

    # --- TAB 2: SINGLE SEARCH CHECK (Phase 1 + Phase 3 Wallet Deductions) ---
    with tab2:
        with st.container(border=True):
            st.markdown("### 🔍 Single Order / Customer Risk Check")
            col1, col2 = st.columns([2, 1])
            with col1:
                search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567", key="single_search_input")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                single_btn = st.button("🚀 Check Risk Score", type="primary", use_container_width=True)

        if single_btn:
            if search_phone:
                cost_incurred = "Free Quota"
                if remaining_free > 0:
                    wallet['used_today'] += 1
                else:
                    required_fee = wallet['charges_per_check']
                    if wallet['balance'] >= required_fee:
                        wallet['balance'] -= required_fee
                        cost_incurred = f"Rs. {required_fee} Deducted"
                    else:
                        st.error(f"❌ Insufficient Balance! You need Rs. {required_fee} for this check.")
                        st.stop()

                st.session_state.audit_logs.insert(0, {
                    "Timestamp": datetime.now().strftime("%I:%M %p"),
                    "User": current_usr,
                    "Action": f"Single Search ({search_phone})",
                    "Cost": cost_incurred,
                    "Status": "Success"
                })

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

    # --- TAB 3: BULK VERIFICATION & SHIELD (Phase 2 + Operator Rights) ---
    with tab3:
        with st.container(border=True):
            st.markdown("### 📁 Bulk Data Verification & Anti-Scraping Shield")
            st.markdown("Upload your order file for batch assessment. Raw database downloads are protected.")
            
            uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    total_rows = len(df)
                    st.info(f"📁 Total rows detected: **{total_rows}**")
                    
                    if st.button("🔒 Run Protected Bulk Assessment", type="primary"):
                        free_available = max(remaining_free, 0)
                        if total_rows <= free_available:
                            wallet['used_today'] += total_rows
                            total_cost = 0
                            cost_label = "Free Quota"
                        else:
                            excess = total_rows - free_available
                            wallet['used_today'] = wallet['daily_limit']
                            total_cost = excess * wallet['charges_per_check']
                            
                            if wallet['balance'] >= total_cost:
                                wallet['balance'] -= total_cost
                                cost_label = f"Rs. {total_cost} Deducted"
                            else:
                                st.error(f"❌ Insufficient Balance! Processing requires Rs. {total_cost}.")
                                st.stop()

                        st.session_state.audit_logs.insert(0, {
                            "Timestamp": datetime.now().strftime("%I:%M %p"),
                            "User": current_usr,
                            "Action": f"Bulk Check ({total_rows} rows)",
                            "Cost": cost_label,
                            "Status": "Success"
                        })

                        st.success(f"✅ Successfully processed {total_rows} records! Cost: {cost_label}")
                        
                        res_summary = [{"Row": i+1, "Assessed Status": "Low Risk" if i%2==0 else "High Risk"} for i in range(total_rows)]
                        res_df = pd.DataFrame(res_summary)
                        st.dataframe(res_df, use_container_width=True)
                        
                        # Download rights check: Admin gets download, Operator gets restriction notice
                        if current_role == "Administrator":
                            st.download_button(
                                label="📥 Download Assessment Summary Report",
                                data=res_df.to_csv(index=False).encode('utf-8'),
                                file_name='risk_assessment_summary.csv',
                                mime='text/csv'
                            )
                        else:
                            st.warning("🔒 **Download Restricted:** Operators cannot download raw report files. Contact Administrator for exports.")
                        
                        st.warning("🛡️ **Anti-Scraping Active:** Raw database downloads are permanently disabled.")
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Error reading file: {e}")

    # --- TAB 4 & 5: ADMIN EXCLUSIVE TABS ---
    if current_role == "Administrator":
        with tab4:
            st.markdown("### ⚙️ System Audit Logs & Transaction History")
            st.markdown("Monitor all user activities, queries, and wallet balance deductions.")
            log_table = pd.DataFrame(st.session_state.audit_logs)
            st.dataframe(log_table, use_container_width=True, hide_index=True)

        with tab5:
            st.markdown("### 👥 Create New User & Assign Rights")
            st.markdown("Add new operators or administrators, set passwords, and allocate limits.")
            
            with st.form("new_user_form_combined"):
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    new_username = st.text_input("New Username")
                    new_password = st.text_input("Password", type="password")
                with col_u2:
                    new_role = st.selectbox("Assign Role (Rights)", ["Operator", "Administrator"])
                    init_balance = st.number_input("Initial Wallet Balance (PKR)", min_value=0.0, value=500.0, step=100.0)
                
                init_limit = st.slider("Daily Free Check Limit (CL)", min_value=10, max_value=500, value=50)
                
                st.markdown("<br>", unsafe_allow_html=True)
                create_btn = st.form_submit_button("➕ Create User Profile", type="primary")
                
                if create_btn:
                    if new_username and new_password:
                        if new_username in st.session_state.users_db:
                            st.error("❌ Username already exists!")
                        else:
                            st.session_state.users_db[new_username] = {
                                "password": new_password,
                                "role": new_role
                            }
                            st.session_state.user_wallets[new_username] = {
                                "daily_limit": init_limit,
                                "used_today": 0,
                                "balance": init_balance,
                                "charges_per_check": 10.0
                            }
                            st.success(f"✅ User '{new_username}' created successfully!")
                    else:
                        st.warning("⚠️ Please provide both username and password.")

            st.markdown("---")
            st.markdown("#### 📋 Active System Users")
            user_list_data = []
            for u, info in st.session_state.users_db.items():
                w_info = st.session_state.user_wallets.get(u, {"balance": 0, "daily_limit": 0})
                user_list_data.append({
                    "Username": u,
                    "Role": info["role"],
                    "Daily Quota": w_info["daily_limit"],
                    "Wallet Balance (PKR)": w_info["balance"]
                })
            st.dataframe(pd.DataFrame(user_list_data), use_container_width=True, hide_index=True)
