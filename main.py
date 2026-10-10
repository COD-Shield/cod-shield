import streamlit as st
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="COD Shield - Merchant Portal", page_icon="🛡️", layout="centered"
)

st.title("🛡️ COD Shield: E-Commerce Risk Intelligence")
st.markdown("Check customer delivery behavior and prevent Cash on Delivery (COD) RTO losses.")
st.markdown("---")

# Mock Database Generator with Green, Yellow, Red Statuses
@st.cache_data
def load_mock_network_data():
    first_names = ["Muhammad", "Ali", "Ahmed", "Fatima", "Zainab", "Usman", "Ayesha", "Bilal", "Hamza", "Sana", "Omar", "Amina"]
    last_names = ["Khan", "Malik", "Awan", "Chaudhry", "Butt", "Sheikh", "Qureshi", "Raza", "Siddiqui", "Mirza"]
    prefixes = ["0300", "0301", "0321", "0333", "0345", "0312"]
    
    risk_profiles = [
        {"status": "🟢 Green (Safe / Delivered)", "remark": "Reliable customer with zero history of RTO."},
        {"status": "🟡 Yellow (Frequent Returner)", "remark": "Returns occasional orders. Proceed with caution."},
        {"status": "🔴 Red (High Risk / RTO Fraud)", "remark": "Multiple fake orders or RTOs flagged across network."}
    ]
    
    data = []
    for i in range(1, 101):
        phone = f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        profile = random.choices(risk_profiles, weights=[70, 20, 10])[0]
        
        data.append({
            "Phone": phone,
            "Customer_Name": name,
            "Total_Orders": random.randint(1, 12),
            "Risk_Status": profile["status"],
            "Remarks": profile["remark"]
        })
    return pd.DataFrame(data)

df_network = load_mock_network_data()

# Tabs for Single Search vs Bulk Upload/Download
tab1, tab2 = st.tabs(["🔍 Single Number Search", "📂 Bulk Upload & Download"])

# ================= TAB 1: SINGLE SEARCH =================
with tab1:
    st.subheader("Instant Customer Risk Check")
    search_phone = st.text_input("Enter Complete Customer Phone Number:", placeholder="e.g. 03001234567")
    
    if search_phone:
        # Exact match check for complete phone number
        result = df_network[df_network['Phone'] == search_phone.strip()]
        
        if not result.empty:
            for _, row in result.iterrows():
                st.markdown("---")
                st.write(f"**Customer Name:** {row['Customer_Name']}")
                st.write(f"**Phone Number:** {row['Phone']}")
                st.write(f"**Total Orders in Network:** {row['Total_Orders']}")
                
                # Display Color Coded Status Box
                status = row['Risk_Status']
                if "Green" in status:
                    st.success(f"**COD Behavior:** {status}")
                elif "Yellow" in status:
                    st.warning(f"**COD Behavior:** {status}")
                else:
                    st.error(f"**COD Behavior:** {status}")
                    
                st.info(f"**Remark:** {row['Remarks']}")
        else:
            st.success("🟢 **Green (Clean / New Customer)**: No negative history found for this complete phone number in the network. Safe to ship!")

# ================= TAB 2: BULK UPLOAD & DOWNLOAD =================
with tab2:
    st.subheader("Bulk Order Verification & Report Download")
    st.markdown("Upload your CSV or Excel file containing customer phone numbers to scan them all at once.")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        user_df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:", user_df.head())
        
        if st.button("Run Bulk Scan"):
            st.success("Scan completed successfully!")
            
            user_df['Risk_Status'] = [random.choice(["🟢 Green", "🟡 Yellow", "🔴 Red"]) for _ in range(len(user_df))]
            
            st.dataframe(user_df, use_container_width=True)
            
            csv_data = user_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Risk Verified Report (CSV)",
                data=csv_data,
                file_name="cod_shield_verified_report.csv",
                mime="text/csv",
            )
