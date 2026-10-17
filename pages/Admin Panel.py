import streamlit as st
import pandas as pd

st.set_page_config(page_title="COD Shield - Admin Panel", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ COD Shield System Admin Panel")
st.markdown("Monitor system audit logs, customer correspondence, and network quotas.")

tab1, tab2 = st.tabs(["📋 Customer Correspondence Logs", "🛡️ Network Audit & Settings"])

with tab1:
    st.subheader("Customer Interaction & Call/WhatsApp Logs")
    log_data = pd.DataFrame({
        "Timestamp": ["2026-10-17 18:30", "2026-10-17 19:15"],
        "Customer_Phone": ["03001234567", "03219876543"],
        "Channel": ["WhatsApp", "Call"],
        "Agent_Status": ["Confirmed", "Unresponsive / Cancelled"],
        "Action_Taken": ["Dispatched order", "Returned to Origin (RTO)"]
    })
    st.dataframe(log_data, use_container_width=True)

with tab2:
    st.subheader("System Control & Configuration")
    st.text_input("Admin API Key", type="password", value="••••••••••••")
    st.checkbox("Enable Real-time Fraud Alerts", value=True)
    st.checkbox("Network-wide Database Sync", value=True)
    if st.button("Save Admin Settings"):
        st.success("Admin settings updated successfully!")
