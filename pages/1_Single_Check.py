import streamlit as st

st.title("🔍 Single Order Risk Check (Phase 1)")

if not st.session_state.get('logged_in', False):
    st.warning("⚠️ Pehle main page par ja kar Login karein!")
    st.stop()

st.markdown(f"Logged in as: **{st.session_state.current_user}** ({st.session_state.user_role})")

search_phone = st.text_input("Enter Customer Phone Number or Order ID", placeholder="e.g. 0300-1234567")
if st.button("Check Risk Score", type="primary"):
    if search_phone:
        st.success(f"Result for {search_phone}: 🟢 **Low Risk (Safe for COD)**")
    else:
        st.warning("Please enter a valid number.")
