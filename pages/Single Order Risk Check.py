import streamlit as st
import pandas as pd
from utils import send_customer_email

st.set_page_config(page_title="COD Shield - Single Order Risk Check", page_icon="🛡️", layout="wide")

# Header aur default menu chupane ke liye CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ COD Shield: Single Order Risk Intelligence")
st.markdown("Check customer delivery behavior, RTO risk score, and dispatch direct alert emails.")

@st.cache_data
def load_database():
    data = {
        "Phone": ["03001234567", "03219876543", "03335554433", "03451122334"],
        "Customer_Name": ["Ali Khan", "Ahmed Raza", "Usman Malik", "Bilal Ahmed"],
        "Total_Orders": [5, 12, 2, 8],
        "Year": [2026, 2026, 2025, 2026],
        "Month": ["October", "September", "October", "August"],
        "Risk_Status": ["Green (Safe)", "Red (High Risk / RTO Fraud)", "Yellow (Frequent Returner)", "Green (Safe)"],
        "Remarks": ["Reliable customer, zero RTO history.", "Multiple fake orders flagged across network.", "Returns occasional orders, proceed with caution.", "Good delivery record."]
    }
    return pd.DataFrame(data)

df = load_database()

search_phone = st.text_input("Enter Customer Phone Number (e.g., 03001234567):", "")

if search_phone:
    clean_phone = search_phone.strip()
    match = df[df["Phone"] == clean_phone]
    
    if not match.empty:
        record = match.iloc[0]
        st.markdown("---")
        st.subheader("📊 Customer Risk Profile Found")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Customer Name", record["Customer_Name"])
            st.metric("Total Network Orders", record["Total_Orders"])
        with col2:
            st.metric("Activity Period", f"{record['Month']} {record['Year']}")
            status = record["Risk_Status"]
            if "Green" in status:
                st.success(f"Status: {status}")
            elif "Yellow" in status:
                st.warning(f"Status: {status}")
            else:
                st.error(f"Status: {status}")
                
        st.info(f"**Remarks:** {record['Remarks']}")
        
        # Email Dispatch Section
        st.markdown("---")
        st.subheader("✉️ Send Direct Email Alert to Customer")
        
        cust_email = st.text_input("Customer Email Address for Notice:")
        email_subj = st.text_input("Subject:", value="COD Shield: Order Verification Notice")
        email_body = st.text_area("Message Body:", value=f"Dear {record['Customer_Name']}, regarding your recent order under verification, please confirm your delivery details.")
        
        if st.button("Send Direct Email 🚀"):
            if cust_email:
                with st.spinner("Sending email..."):
                    success = send_customer_email(cust_email, email_subj, email_body)
                    if success:
                        st.success(f"Email successfully dispatched to {cust_email}!")
            else:
                st.warning("Please enter a valid customer email address first.")
    else:
        st.success("🟢 Clean Record: No negative history found in the network. Safe to ship!")
