import streamlit as st

st.title("💳 Admin Penal")

if not st.session_state.get('logged_in', False):
    st.warning("⚠️ Pehle main page par ja kar Login karein!")
    st.stop()

role = st.session_state.user_role
st.markdown(f"Current Role: **{role}**")

if role == "Administrator":
    st.markdown("### 👥 Admin User Management & Rights")
    with st.form("admin_user_form"):
        new_user = st.text_input("New Username")
        new_pass = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["Operator", "Administrator"])
        if st.form_submit_button("Create User"):
            if new_user and new_pass:
                st.session_state.users_db[new_user] = {"password": new_pass, "role": new_role}
                st.success(f"User '{new_user}' created successfully!")
            else:
                st.warning("Fill all fields.")
else:
    st.markdown("### 💰 Operator Wallet & Balance")
    st.info("Prepaid Balance: **Rs. 450/-**\n\nExtra Check Rate: **Rs. 10 / check**")
