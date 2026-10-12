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
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #ff2e63;'>🛡️ Portal Secure Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Login to Workspace", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
else:
    # ==========================================
    # VIBRANT & COLORFUL MODERN ARTWORK THEME
    # ==========================================
    curr_user = st.session_state.current_user
    curr_role = st.session_state.user_role
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0})
    
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    # Custom Vibrant Styling with rich gradients and colored borders
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #090d16 100%);
            color: #ffffff;
        }
        .main-header {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            padding: 30px;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
            margin-bottom: 25px;
        }
        .vibrant-card-1 {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-top: 5px solid #6366f1;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }
        .vibrant-card-2 {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-top: 5px solid #a855f7;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }
        .vibrant-card-3 {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(236, 72, 153, 0.3);
            border-top: 5px solid #ec4899;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }
        .vibrant-card-4 {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-top: 5px solid #22c55e;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }
        .card-label {
            font-size: 13px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 0;
        }
        .card-val-1 { font-size: 28px; font-weight: 800; color: #818cf8; margin: 8px 0 0 0; }
        .card-val-2 { font-size: 28px; font-weight: 800; color: #c084fc; margin: 8px 0 0 0; }
        .card-val-3 { font-size: 28px; font-weight: 800; color: #f472b6; margin: 8px 0 0 0; }
        .card-val-4 { font-size: 28px; font-weight: 800; color: #4ade80; margin: 8px 0 0 0; }
        </style>
    """, unsafe_allow_html=True)

    # Header Banner
    st.markdown(f"""
        <div class="main-header">
            <h1 style='margin:0; font-size: 28px; font-weight: 800;'>⚡ COD Risk Intelligence Workspace</h1>
            <p style='margin:6px 0 0 0; font-size: 15px; opacity: 0.9;'>Welcome, <b>{curr_user.upper()}</b> &nbsp;|&nbsp; Access Tier: <b>{curr_role}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # Color-coded Performance Metrics Cards
    st.markdown("### 🔥 Live Performance Dashboard")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="vibrant-card-1">
                <p class="card-label">Total Attempts</p>
                <p class="card-val-1">{wallet['total_attempts']}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="vibrant-card-2">
                <p class="card-label">Quota Used Today</p>
                <p class="card-val-2">{wallet['used_today']} / {wallet['daily_limit']}</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="vibrant-card-3">
                <p class="card-label">Remaining Quota</p>
                <p class="card-val-3">{max(remaining_quota, 0)}</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="vibrant-card-4">
                <p class="card-label">Wallet Balance</p>
                <p class="card-val-4">Rs. {wallet['balance']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Lower Section: Chart & Navigation Guide
    c_left, c_right = st.columns([1.3, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("#### 📊 Risk Distribution Analytics")
            chart_data = pd.DataFrame({
                'Risk Category': ['Safe / Low Risk', 'Medium Risk', 'High Returners'],
                'Distribution (%)': [72, 18, 10]
            })
            st.bar_chart(chart_data.set_index('Risk Category'))

    with c_right:
        with st.container(border=True):
            st.markdown("#### 🧭 Quick Navigation Guide")
            st.info("👈 **Left Sidebar** se apne alag-alag modules open karein:\n"
                    "- **1_Single_Check**: Single customer lookup.\n"
                    "- **2_Bulk_Check**: Batch verification & anti-scraping.\n"
                    "- **3_Wallet_Admin**: Monetization & user rights.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Logout Workspace", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
                
