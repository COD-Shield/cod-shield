import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="COD Risk Assessment Portal",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

# Users database mock
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator"},
        "operator": {"password": "pass123", "role": "Operator"}
    }

# Wallet & Quotas mock data
if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "admin": {"daily_limit": 500, "used_today": 42, "balance": 7500.0, "total_attempts": 320},
        "operator": {"daily_limit": 50, "used_today": 18, "balance": 450.0, "total_attempts": 85}
    }

# Login Gate
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛡️ Portal Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("🔑 Secure Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("❌ Incorrect username or password.")
else:
    # ==========================================
    # INTERACTIVE & COLORFUL PORTFOLIO / DASHBOARD
    # ==========================================
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Custom CSS for Colorful Cards
    st.markdown("""
        <style>
        .metric-card {
            background: linear-gradient(135deg, #1f4068 0%, #162447 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-card h3 { margin: 0; font-size: 16px; color: #e4e4e4; }
        .metric-card h2 { margin: 10px 0 0 0; font-size: 28px; color: #00adb5; }
        </style>
    """, unsafe_allow_html=True)

    # Header Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 25px; border-radius: 14px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style='margin:0; font-size: 28px;'>🌟 Interactive Customer & Operator Portfolio</h1>
            <p style='margin:8px 0 0 0; font-size: 15px;'>Welcome back, <b>{curr_user.upper()}</b> | Role: <b>{curr_role}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # Colorful Metrics Grid
    st.markdown("### 📊 Live Performance & Quota Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #ff2e63;">
                <h3>🔥 Total Attempts</h3>
                <h2>{wallet['total_attempts']}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #00adb5;">
                <h3>⚡ Free Quota Used</h3>
                <h2>{wallet['used_today']} / {wallet['daily_limit']}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #ffbf00;">
                <h3>🛡️ Remaining Quota</h3>
                <h2>{max(remaining_quota, 0)}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #00ff87;">
                <h3>💰 Wallet Balance</h3>
                <h2>Rs. {wallet['balance']}</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Visual Breakdown Section
    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("#### 📈 Risk Assessment Analytics Trend")
            chart_data = pd.DataFrame({
                'Category': ['Safe / Low Risk', 'Medium Risk', 'High Risk / Returners'],
                'Percentage': [70, 20, 10]
            })
            st.bar_chart(chart_data.set_index('Category'))

    with c_right:
        with st.container(border=True):
            st.markdown("#### ⚡ Quick Navigation Guidance")
            st.info("👈 **Left Sidebar** se aap apne alag-alag pages access kar sakte hain:\n"
                    "- **1_Single_Check:** Single customer verification ke liye.\n"
                    "- **2_Bulk_Check:** Bulk file upload aur Anti-Scraping shield ke liye.\n"
                    "- **3_Wallet_Admin:** Wallet balance aur user management ke liye.")
            
            if st.button("🚪 Logout Portal", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
