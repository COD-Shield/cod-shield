import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="COD Risk Portal",
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

# Login Gate
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; font-weight: 600; letter-spacing: -0.5px;'>🛡️ COD Shield Portal</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #888; font-size: 13px;'>Secure Authentication Gateway</p>", unsafe_allow_html=True)
            
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
    # ==========================================
    # LATEST TRENDY MINIMALIST ARTWORK DESIGN
    # ==========================================
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Trendy Modern Vercel/Linear Style CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #09090b;
            color: #fafafa;
        }
        .trendy-banner {
            background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 28px;
            border-radius: 16px;
            backdrop-filter: blur(20px);
            margin-bottom: 24px;
        }
        .metric-tile {
            background: #121215;
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            transition: all 0.2s ease-in-out;
        }
        .metric-tile:hover {
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        .metric-title {
            font-size: 13px;
            font-weight: 500;
            color: #a1a1aa;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 0;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            margin: 8px 0 0 0;
            letter-spacing: -0.02em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Top Trendy Banner
    st.markdown(f"""
        <div class="trendy-banner">
            <h2 style='margin:0; font-size: 24px; font-weight: 600; letter-spacing: -0.03em;'>Risk Intelligence Workspace</h2>
            <p style='margin:6px 0 0 0; color: #a1a1aa; font-size: 14px;'>Logged in as <span style='color: #fff; font-weight: 500;'>{curr_user}</span> &bull; Role: <span style='color: #38bdf8;'>{curr_role}</span></p>
        </div>
    """, unsafe_allow_html=True)

    # Modern Metric Cards Grid
    st.markdown("### Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-tile">
                <p class="metric-title">Total Attempts</p>
                <p class="metric-value">{wallet['total_attempts']}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-tile">
                <p class="metric-title">Quota Used</p>
                <p class="metric-value">{wallet['used_today']}<span style='font-size: 16px; color: #71717a;'>/{wallet['daily_limit']}</span></p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-tile">
                <p class="metric-title">Remaining Quota</p>
                <p class="metric-value">{max(remaining_quota, 0)}</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-tile">
                <p class="metric-title">Wallet Balance</p>
                <p class="metric-value" style='color: #4ade80;'>Rs. {wallet['balance']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Lower Section: Chart & Navigation Help
    c_left, c_right = st.columns([1.3, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("#### Risk Distribution Analytics")
            chart_df = pd.DataFrame({
                'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
                'Share': [75, 15, 10]
            })
            st.bar_chart(chart_df.set_index('Risk Level'))

    with c_right:
        with st.container(border=True):
            st.markdown("#### Navigation Guide")
            st.markdown("Use the **left sidebar** to access your structured modules:")
            st.markdown("- **1_Single_Check**: Individual customer lookups.")
            st.markdown("- **2_Bulk_Check**: Batch verification & anti-scraping shield.")
            st.markdown("- **3_Wallet_Admin**: Billing, monetization, & controls.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
