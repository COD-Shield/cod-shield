import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bulk & Shield | COD Shield", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f6f4 !important; color: #111827 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .ramp-title { font-size: 26px; font-weight: 700; color: #0e3b2e; }
    .section-header { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #4b5563; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 25px; margin-bottom: 15px; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 20px !important; }
    </style>
""", unsafe_allow_html=True)

if 'network_reports' not in st.session_state:
    st.session_state.network_reports = [
        {"phone": "03001234567", "outcome": "delivered", "date": "2026-10-12"},
        {"phone": "03219876543", "outcome": "refused", "date": "2026-10-11"}
    ]

st.markdown('<p class="ramp-title">🛡️ Bulk Operations & Delivery Reports</p>', unsafe_allow_html=True)
st.markdown("<p style='color: #4b5563;'>Upload CSV sheets or submit batch delivery outcomes to strengthen the network and secure your logistics budget.</p>", unsafe_allow_html=True)

# Section 1
st.markdown('<div class="section-header">01 / Report Delivery Outcome</div>', unsafe_allow_html=True)
with st.container(border=True):
    r_phone = st.text_input("Order Phone Number", placeholder="03XX XXXXXXX")
    r_outcome = st.radio("What happened to the order?", ["Delivered", "Returned / Refused"], horizontal=True)
    if st.button("Submit Network Report", type="primary", use_container_width=True):
        if r_phone:
            val = "delivered" if r_outcome == "Delivered" else "refused"
            st.session_state.network_reports.append({"phone": r_phone, "outcome": val, "date": "2026-10-12"})
            st.success("✅ Report successfully added to shared network, protecting other merchants!")
        else:
            st.warning("Please enter a phone number.")

# Section 2
st.markdown('<div class="section-header">02 / Import CSV Sheet</div>', unsafe_allow_html=True)
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload UTF-8 CSV (columns: phone_number, outcome)", type="csv")
    if uploaded_file:
        df_csv = pd.read_csv(uploaded_file)
        st.success(f"Successfully processed {len(df_csv)} records from CSV!")
        st.dataframe(df_csv.head(3), use_container_width=True)
