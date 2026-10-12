import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal - Phase 3 (Monetization)",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States for Phase 3
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

# Wallet & Dynamic Credit Limit System per user (Phase 3)
if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "admin": {"daily_limit": 50, "used_today": 12, "balance": 5000.0, "charges_per_check": 10.0},
        "operator": {"daily_limit": 20, "used_today": 5, "balance": 450.0, "charges_per_check": 10.0}
    }

# Advanced Audit Logs for Admin Monitoring
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": "10:15 AM", "User": "admin", "Action": "Single Check", "Cost": "Free Quota", "Status": "Success"},
        {"Timestamp": "10:40 AM", "User": "operator", "Action": "Bulk Check (15 rows)", "Cost": "Rs. 150 Deducted", "Status": "Success"},
    ]

# ================= 1. SECURE LOGIN GATE =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ COD Risk Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Phase 3: Wallet & Commercial Monetization</p>", unsafe_allow_html=True)
            
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
    # ================= 2. DASHBOARD HEADER & WALLET SIDEBAR =================
    current_usr = st.session_state.current_user
    wallet = st.session_state.user_wallets[current_usr]
    remaining_free = wallet['daily_limit'] - wallet['used_today']

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 22px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style='margin:0; font-size: 26px;'>🛡️ COD Risk & Monetization Portal</h1>
            <p style='margin:5px 0 0 0; font-size: 14px;'>Active User: <b>{current_usr}</b> ({st.session_state.user_role}) | Wallet & Quota Active</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Wallet & Balance Widget
    st.sidebar.markdown(f"### 👤 Profile: {current_usr}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 Wallet & Quota Status")
    st.sidebar.info(f"**Free Quota Left:** {max(remaining_free, 0)} / {wallet['daily_limit']}")
    st.sidebar.success(f"**Prepaid Balance:** Rs. {wallet['balance']}/-")
    st.sidebar.caption((f"Extra check rate: Rs. {wallet['charges_per_check']} / check"))
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Tabs for Workflow
    if st.session_state.user_role == "Administrator":
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🔍 Single Check", "📁 Bulk Verification Shield", "⚙️ Admin Audit Logs"])
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🔍 Single Check", "📁 Bulk Verification Shield"])

    # --- TAB 1: ANALYTICS ---
    with tab1:
        st.markdown("### 📈 Performance & Usage Overview")
        col_k1, col_k2, col_k3 = st.columns(3)
        with col_k1:
            st.metric(label="📊 Free Quota Used Today", value=wallet['used_today'])
        with col_k2:
            st.metric(label="💰 Current Balance", value=f"Rs. {wallet['balance']}")
        with col_k3:
            st.metric(label="⚡ System Security", value="Active 🛡️")

    # --- TAB 2: SINGLE CHECK ---
    with tab2:
        with st.container(border=True):
            st.markdown("### 🔍 Single Order Risk Check")
            col1, col2 = st.columns([2, 1])
            with col1:
                search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                single_btn = st.button("🚀 Check Risk", type="primary", use_container_width=True)

        if single_btn:
            if search_phone:
                cost_incurred = "Free Quota"
                # Check Quota vs Wallet Balance Logic
                if remaining_free > 0:
                    wallet['used_today'] += 1
                else:
                    required_fee = wallet['charges_per_check']
                    if wallet['balance'] >= required_fee:
                        wallet['balance'] -= required_fee
                        cost_incurred = f"Rs. {required_fee} Deducted"
                    else:
                        st.error(f"❌ Insufficient Balance! You need Rs. {required_fee} for this check. Please top up your wallet.")
                        st.stop()

                # Log activity
                st.session_state.audit_logs.insert(0, {
                    "Timestamp": datetime.now().strftime("%I:%M %p"),
                    "User": current_usr,
                    "Action": f"Single Check ({search_phone})",
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
                st.warning("⚠️ Please enter a phone number.")

    # --- TAB 3: BULK VERIFICATION SHIELD ---
    with tab3:
        with st.container(border=True):
            st.markdown("### 📁 Bulk Data Verification & Monetization Shield")
            uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    total_rows = len(df)
                    st.info(f"📁 Total rows detected: **{total_rows}**")
                    
                    if st.button("🔒 Run Paid & Protected Assessment", type="primary"):
                        # Calculate free vs paid rows
                        free_available = max(remaining_free, 0)
                        if total_rows <= free_available:
                            wallet['used_today'] += total_rows
                            total_cost = 0
                            cost_label = "Free Quota"
                        else:
                            excess = total_rows - free_available
                            wallet['used_today'] = wallet['daily_limit'] # Exhaust free limit
                            total_cost = excess * wallet['charges_per_check']
                            
                            if wallet['balance'] >= total_cost:
                                wallet['balance'] -= total_cost
                                cost_label = f"Rs. {total_cost} Deducted"
                            else:
                                st.error(f"❌ Insufficient Balance! Processing {total_rows} records requires Rs. {total_cost}. Please top up.")
                                st.stop()

                        # Log activity
                        st.session_state.audit_logs.insert(0, {
                            "Timestamp": datetime.now().strftime("%I:%M %p"),
                            "User": current_usr,
                            "Action": f"Bulk Check ({total_rows} rows)",
                            "Cost": cost_label,
                            "Status": "Success"
                        })

                        st.success(f"✅ Successfully processed {total_rows} records! Cost: {cost_label}")
                        
                        # Restricted view output (Anti-scraping protection)
                        res_summary = [{"Row": i+1, "Assessed Status": "Low Risk" if i%2==0 else "High Risk"} for i in range(total_rows)]
                        st.dataframe(pd.DataFrame(res_summary), use_container_width=True)
                        st.warning("🛡️ **Anti-Scraping Active:** Raw database downloads are disabled.")
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # --- TAB 4: ADMIN AUDIT LOGS ---
    if st.session_state.user_role == "Administrator":
        with tab4:
            st.markdown("### ⚙️ System Audit Logs & Transaction History")
            st.markdown("Monitor all user activities, queries, and wallet balance deductions across the portal.")
            log_table = pd.DataFrame(st.session_state.audit_logs)
            st.dataframe(log_table, use_container_width=True, hide_index=True)
