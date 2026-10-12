import streamlit as st

st.set_page_config(
    page_title="COD Risk Assessment Portal",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "Admin": {"password": "admin123", "role": "Administrator"},
        "operator": {"password": "pass123", "role": "Operator"}
    }
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

st.markdown("""
    <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 30px; border-radius: 12px; color: white; text-align: center;">
        <h1>🛡️ COD Risk Assessment & Monetization Portal</h1>
        <p>Multi-Page Professional Suite (Phase 1, 2 & 3)</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🔑 Portal Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.success("Login successful! Please select a page from the sidebar.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
else:
    st.success(f"Welcome back, **{st.session_state.current_user}** ({st.session_state.user_role})!")
    st.info("Aap left sidebar se apni zaroorat ke mutabiq page (Single Check, Bulk Check, ya Wallet/Admin) select kar sakte hain.")
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
