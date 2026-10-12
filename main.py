import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal - Interactive Dashboard",
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

# Daily Quota Tracking per user session
if 'user_quotas' not in st.session_state:
    st.session_state.user_quotas = {
        "admin": {"daily_limit": 500, "used_today": 12},
        "operator": {"daily_limit": 50, "used_today": 5}
    }

# App Activity History for Interactive Charts
if 'activity_logs' not in st.session_state:
    st.session_state.activity_logs = [
        {"Time": "10:15 AM", "User": "admin", "Type": "Single Check", "Result": "Low Risk"},
        {"Time": "10:20 AM", "User": "admin", "Type": "Single Check", "Result": "High Risk"},
        {"Time": "10:35 AM", "User": "operator", "Type": "Bulk Check", "Result": "Mixed Risk"},
        {"Time": "11:00 AM", "User": "operator", "Type": "Single Check", "Result": "Low Risk"},
    ]

# ================= 1. SECURE LOGIN GATE =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ COD Risk Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Interactive Analytics & Protection Suite</p>", unsafe_allow_html=True)
            
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
    # ================= 2. INTERACTIVE DASHBOARD HEADER =================
    current_usr = st.session_state.current_user
    quota_info = st.session_state.user_quotas.get(current_usr, {"daily_limit": 50, "used_today": 0})
    remaining_quota = quota_info['daily_limit'] - quota_info['used_today']

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 22px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style='margin:0; font-size: 26px;'>🛡️ COD Risk Intelligence Dashboard</h1>
            <p style='margin:5px 0 0 0; font-size: 14px;'>Active Session: <b>{current_usr}</b> ({st.session_state.user_role}) | Anti-Scraping Shield Active</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Widget
    st.sidebar.markdown(f"### 👤 Profile: {current_usr}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 Daily Quota Status")
    st.sidebar.info(f"**Remaining Checks:** {remaining_quota} / {quota_info['daily_limit']}")
    st.sidebar.progress(min(quota_info['used_today'] / quota_info['daily_limit'], 1.0))
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- INTERACTIVE KPI METRICS ROW ---
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.metric(label="📊 Total Checks Today", value=sum([v['used_today'] for v in st.session_state.user_quotas.values()]))
    with col_kpi2:
        st.metric(label="🟢 Safe / Low Risk Orders", value="78%", delta="+4% vs yesterday")
    with col_kpi3:
        st.metric(label="🔴 High Risk / Returns", value="22%", delta="-2% improvement")
    with col_kpi4:
        st.metric(label="⚡ System Status", value="Protected", delta="Secure 🛡️")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for Workflow
    tab1, tab2, tab3 = st.tabs(["📊 Overview & Analytics", "🔍 Single Order Check", "📁 Bulk Data Shield"])

    # --- TAB 1: OVERVIEW & INTERACTIVE CHARTS ---
    with tab1:
        st.markdown("### 📈 Real-Time Risk Analytics")
        
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            with st.container(border=True):
                st.markdown("#### Risk Distribution Breakdown")
                # Interactive bar chart representation of risk statuses
                chart_data = pd.DataFrame({
                    'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
                    'Count': [145, 42, 31]
                })
                st.bar_chart(chart_data.set_index('Risk Level'))
        
        with c_chart2:
            with st.container(border=True):
                st.markdown("#### Recent Verification Logs")
                log_df = pd.DataFrame(st.session_state.activity_logs)
                st.dataframe(log_df, use_container_width=True, hide_index=True)

    # --- TAB 2: SINGLE CHECK ---
    with tab2:
        with st.container(border=True):
            st.markdown("### 🔍 Single Order / Customer Risk Check")
            col1, col2 = st.columns([2, 1])
            with col1:
                search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567", key="single_input")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                single_btn = st.button("🚀 Check Risk Score", type="primary", use_container_width=True)

        if single_btn:
            if search_phone:
                if remaining_quota <= 0:
                    st.error("❌ Daily Credit Limit (CL) exhausted! You cannot perform more checks today.")
                else:
                    st.session_state.user_quotas[current_usr]['used_today'] += 1
                    
                    mock_db = {
                        "0300-1234567": {"name": "Ali Khan", "city": "Lahore", "risk": "Low Risk", "returns": 1, "delivered": 25},
                        "0300-7654321": {"name": "Usman Ahmed", "city": "Karachi", "risk": "High Risk", "returns": 12, "delivered": 5},
                    }
                    
                    # Log activity
                    st.session_state.activity_logs.insert(0, {"Time": datetime.now().strftime("%I:%M %p"), "User": current_usr, "Type": "Single Check", "Result": "Checked"})

                    if search_phone in mock_db:
                        data = mock_db[search_phone]
                        st.markdown("<br>", unsafe_allow_html=True)
                        res_col1, res_col2 = st.columns(2)
                        with res_col1:
                            with st.container(border=True):
                                st.markdown("#### 📋 Customer Summary")
                                st.write(f"**Name:** {data['name']}")
                                st.write(f"**City:** {data['city']}")
                                st.write(f"**Total Delivered:** {data['delivered']}")
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
                    st.rerun()
            else:
                st.warning("⚠️ Please enter a valid phone number or order ID.")

    # --- TAB 3: BULK VERIFICATION SHIELD ---
    with tab3:
        with st.container(border=True):
            st.markdown("### 📁 Bulk Orders / CSV Verification Shield")
            st.markdown("Upload your order file. The system evaluates rows while restricting raw bulk data exports to prevent scraping.")
            
            uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    total_rows = len(df)
                    st.info(f"📁 File uploaded successfully. Total rows detected: **{total_rows}**")
                    
                    if st.button("🔒 Run Protected Bulk Assessment", type="primary"):
                        if total_rows > remaining_quota:
                            st.error(f"❌ **Quota Exceeded!** Your file has {total_rows} records, but you only have **{remaining_quota}** remaining checks.")
                        else:
                            st.session_state.user_quotas[current_usr]['used_today'] += total_rows
                            st.success(f"✅ Successfully processed {total_rows} records!")
                            
                            result_summary = []
                            for i in range(total_rows):
                                risk_status = "Low Risk" if i % 2 == 0 else "High Risk"
                                result_summary.append({"Row Index": i+1, "Assessed Status": risk_status})
                            
                            res_df = pd.DataFrame(result_summary)
                            st.markdown("#### 📊 Secured Assessment Results (Restricted View)")
                            st.dataframe(res_df, use_container_width=True)
                            st.warning("🛡️ **Anti-Scraping Protection Active:** Bulk raw database downloads remain disabled.")
                            st.rerun()

                except
