import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="COD Risk Intelligence | Stripe Style",
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

# Login Gate - Stripe Style Clean Glass Card
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a2540 0%, #020617 100%);
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #635bff; font-weight: 800; letter-spacing: -0.5px;'>🛡️ Stripe-Grade Portal</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Secure Financial Infrastructure Login</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign in to Dashboard", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
else:
    # ==========================================
    # STRIPE-INSPIRED MODERN FINTECH UI
    # ==========================================
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Custom Stripe-Inspired CSS (Deep Navy, Indigo Glow, Smooth Radius)
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(180deg, #0a2540 0%, #071728 50%, #020617 100%);
            color: #e2e8f0;
        }
        .stripe-hero {
            background: linear-gradient(135deg, #635bff 0%, #00d4ff 100%);
            padding: 32px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 20px 40px rgba(99, 91, 255, 0.25);
            margin-bottom: 25px;
        }
        .stripe-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 4px solid #635bff;
            padding: 24px;
            border-radius: 14px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            text-align: left;
        }
        .stripe-card-alt {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 4px solid #00d4ff;
            padding: 24px;
            border-radius: 14px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            text-align: left;
        }
        .stripe-card-warn {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 4px solid #f59e0b;
            padding: 24px;
            border-radius: 14px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            text-align: left;
        }
        .stripe-card-success {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 4px solid #10b981;
            padding: 24px;
            border-radius: 14px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            text-align: left;
        }
        .metric-title {
            font-size: 13px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 0;
        }
        .metric-val {
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            margin: 8px 0 0 0;
            letter-spacing: -0.03em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown(f"""
        <div class="stripe-hero">
            <h1 style='margin:0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;'>Financial Risk Infrastructure</h1>
            <p style='margin:8px 0 0 0; font-size: 15px; opacity: 0.9;'>Operator: <b style='color:#fff;'>{curr_user.upper()}</b> &bull; Access Profile: <b style='color:#fff;'>{curr_role}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # Metrics Grid (Stripe Fintech Style)
    st.markdown("### 📊 Performance & Revenue Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="stripe-card">
                <p class="metric-title">Total Attempts</p>
                <p class="metric-val" style="color: #818cf8;">{wallet['total_attempts']}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stripe-card-alt">
                <p class="metric-title">Quota Utilized</p>
                <p class="metric-val" style="color: #38bdf8;">{wallet['used_today']} <span style="font-size:16px; color:#64748b;">/ {wallet['daily_limit']}</span></p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="stripe-card-warn">
                <p class="metric-title">Remaining Quota</p>
                <p class="metric-val" style="color: #fbbf24;">{max(remaining_quota, 0)}</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="stripe-card-success">
                <p class="metric-title">Wallet Balance</p>
                <p class="metric-val" style="color: #34d399;">Rs. {wallet['balance']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Lower Section: Chart and Sidebar Navigation Guide
    c_left, c_right = st.columns([1.3, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("#### Risk Analytics Distribution")
            chart_df = pd.DataFrame({
                'Risk Category': ['Low Risk / Verified', 'Medium Risk', 'High Returners'],
                'Share (%)': [72, 18, 10]
            })
            st.bar_chart(chart_df.set_index('Risk Category'))

    with c_right:
        with st.container(border=True):
            st.markdown("#### Multi-Page Modules")
            st.info("👈 **Left Sidebar** open karein aur apne specific phases access karein:\n"
                    "- **1_Single_Check**: Single customer lookup.\n"
                    "- **2_Bulk_Check**: Batch verification & shielding.\n"
                    "- **3_Wallet_Admin**: Billing & monetization.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign out securely", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
