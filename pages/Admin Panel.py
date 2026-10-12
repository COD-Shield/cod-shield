import streamlit as st

st.set_page_config(page_title="Wallet & Admin | COD Shield", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f7f5f0 !important; color: #292524 !important; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #ffffff !important; border: 1px solid #e7e5e4 !important; border-radius: 12px !important; padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 💳 Phase 3: Wallet, Monetization & Admin Controls")
st.markdown("<p style='color: #57534e;'>Manage balance, usage quotas, and system-wide configurations.</p>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### 💰 Account Balance & Top-up")
    st.markdown("Current Available Balance: **Rs. 7,500.0**")
    topup_amt = st.number_input("Top-up Amount (PKR)", min_value=500, step=500, value=1000)
    if st.button("Proceed to Top-up Gateway", type="primary", use_container_width=True):
        st.success(f"Successfully initiated invoice for Rs. {topup_amt}!")

with st.container(border=True):
    st.markdown("#### ⚙️ Administrator Settings")
    st.checkbox("Enable Anti-Scraping Rate Limiter", value=True)
    st.checkbox("Strict Verification Mode", value=False)
    if st.button("Save System Configurations"):
        st.success("Settings updated successfully.")
