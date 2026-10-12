import streamlit as st

st.set_page_config(page_title="Single Check | COD Shield", page_icon="🔍", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f7f5f0 !important; color: #292524 !important; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #ffffff !important; border: 1px solid #e7e5e4 !important; border-radius: 12px !important; padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🔍 Phase 1: Single Customer Risk Verification")
st.markdown("<p style='color: #57534e;'>Check individual phone numbers against shared network delivery history.</p>", unsafe_allow_html=True)

if 'network_reports' not in st.session_state:
    st.session_state.network_reports = [
        {"phone": "03001234567", "outcome": "delivered", "date": "2026-10-12"},
        {"phone": "03219876543", "outcome": "refused", "date": "2026-10-11"}
    ]

with st.container(border=True):
    phone_input = st.text_input("Enter Customer Phone Number", placeholder="03XX XXXXXXX")
    if st.button("Check Network Risk", type="primary", use_container_width=True):
        if phone_input:
            found = next((r for r in st.session_state.network_reports if r['phone'] == phone_input), None)
            if found:
                if found['outcome'] == 'delivered':
                    st.markdown("<div style='background:#ecfdf5; border:1px solid #10b981; padding:15px; border-radius:8px; color:#065f46; margin-top:10px;'><b>🟢 GREEN: Low Risk</b><br>Customer has a positive verified delivery record in the network.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#fef2f2; border:1px solid #ef4444; padding:15px; border-radius:8px; color:#991b1b; margin-top:10px;'><b>🔴 RED: High Risk / Refusal History</b><br>Phone number reported for previous order refusals.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='background:#f4f4f5; border:1px solid #d4d4d8; padding:15px; border-radius:8px; color:#27272a; margin-top:10px;'><b>🟢 GREEN: Low Risk</b><br>No negative delivery history found. Safe to dispatch.</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a valid phone number.")
