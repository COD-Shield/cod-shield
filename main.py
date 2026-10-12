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
            st.markdown("<h2 style='text-align: center; color: #ff2e63;'>🛡️ 3D Portal Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("🔑 Secure 3D Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("❌ Incorrect username or password.")
else:
    # ==========================================
    # ULTRA-COLORFUL & 3D GLASSMORPHISM UI
    # ==========================================
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Custom 3D & Glowing Neon CSS Styling
    st.markdown("""
        <style>
        .stApp {
            background: radial-gradient(circle at 50% 10%, #1a1a2e 0%, #16213e 50%, #0f0f1a 100%);
        }
        .hero-banner {
            background: linear-gradient(135deg, #ff2e63 0%, #08d9d6 50%, #252a34 100%);
            padding: 30px;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 15px 35px rgba(255, 46, 99, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 30px;
        }
        .card-3d-1 {
            background: linear-gradient(145deg, #1f2937, #111827);
            padding: 25px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 10px 25px rgba(255, 46, 99, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
            border-top: 4px solid #ff2e63;
            text-align: center;
        }
        .card-3d-2 {
            background: linear-gradient(145deg, #1f2937, #111827);
            padding: 25px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 10px 25px rgba(8, 217, 214, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
            border-top: 4px solid #08d9d6;
            text-align: center;
        }
        .card-3d-3 {
            background: linear-gradient(145deg, #1f2937, #111827);
            padding: 25px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 10px 25px rgba(255, 191, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
            border-top: 4px solid #ffbf00;
            text-align: center;
        }
        .card-3d-4 {
            background: linear-gradient(145deg, #1f2937, #111827);
            padding: 25px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 10px 25px rgba(0, 255, 135, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
            border-top: 4px solid #00ff87;
            text-align: center;
        }
        .card-3d-1 h3, .card-3d-2 h3, .card-3d-3 h3, .card-3d-4 h3 { margin: 0; font-size: 15px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; }
        .card-3d-1 h2 { margin: 12px 0 0 0; font-size: 32px; color: #ff2e63; font-weight: 800; text-shadow: 0 0 10px rgba(255,46,99,0.5); }
        .card-3d-2 h2 { margin: 12px 0 0 0; font-size: 32px; color: #08d9d6; font-weight: 800; text-shadow: 0 0 10px rgba(8,217,214,0.5); }
        .card-3d-3 h2 { margin: 12px 0 0 0; font-size: 32px; color: #ffbf00; font-weight: 800; text-shadow: 0 0 10px rgba(255,191,0,0.5); }
        .card-3d-4 h2 { margin: 12px 0 0 0; font-size: 32px; color: #00ff87; font-weight: 800; text-shadow: 0 0 10px rgba(0,255,135,0.5); }
        </style>
    """, unsafe_allow_html=True)

    # 3D Glowing Header Banner
    st.markdown(f"""
        <div class="hero-banner">
            <h1 style='margin:0; font-size: 32px; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.4);'>🌟 COD Risk Intelligence 3D Portal</h1>
            <p style='margin:8px 0 0 0; font-size: 16px; font-weight: 500;'>Active Operator: <b>{curr_user.upper()}</b> &nbsp;|&nbsp; Role Tier: <b>{curr_role}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # 3D Colorful Metric Cards
    st.markdown("### 🔥 Live 3D Performance Analytics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="card-3d-1">
                <h3>Total Attempts</h3>
                <h2>{wallet['total_attempts']}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card-3d-2">
                <h3>Quota Used</h3>
                <h2>{wallet['used_today']} / {wallet['daily_limit']}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card-3d-3">
                <h3>Remaining Quota</h3>
                <h2>{max(remaining_quota, 0)}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="card-3d-4">
                <h3>Wallet Balance</h3>
                <h2>Rs. {wallet['balance']}</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Analytics & Navigation Box
    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("#### 📊 Risk Distribution Spectrum")
            chart_data = pd.DataFrame({
                'Risk Category': ['Safe / Low Risk', 'Medium Risk', 'High Returners'],
                'Share (%)': [72, 18, 10]
            })
            st.bar_chart(chart_data.set_index('Risk Category'))

    with c_right:
        with st.container(border=True):
            st.markdown("#### ⚡ Sidebar Multi-Page Navigation")
            st.info("👈 **Left Sidebar** open karein aur apne alag-alag phases access karein:\n"
                    "- **1_Single_Check:** Single phone/order verification.\n"
                    "- **2_Bulk_Check:** Bulk upload & anti-scraping guard.\n"
                    "- **3_Wallet_Admin:** Wallet monetization & user rights.")
            
            if st.button("🚪 Logout 3D Portal", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
