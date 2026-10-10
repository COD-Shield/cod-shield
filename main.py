import streamlit as st
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="COD Shield Portal", page_icon="🛡️", layout="wide"
)

# Sidebar Navigation (مینو بار)
st.sidebar.title("🛡️ COD Shield Navigation")
app_mode = st.sidebar.radio("Choose Interface:", ["🔍 Merchant Lookup Portal", "⚙️ Admin Dashboard (Moise)"])

# Shared Mock Database Generator
@st.cache_data
def generate_pakistani_mock_data(num_records=60):
    first_names = [
        "Muhammad", "Ali", "Ahmed", "Fatima", "Zainab", "Usman", "Ayesha", 
        "Bilal", "Hamza", "Sana", "Omar", "Amina", "Hassan", "Hira", 
        "Saad", "Khadija", "Talha", "Maryam", "Danyal", "Laiba", "Shahzaib"
    ]
    last_names = [
        "Khan", "Malik", "Awan", "Chaudhry", "Butt", "Sheikh", "Qureshi", 
        "Raza", "Siddiqui", "Mirza", "Gondal", "Jutt", "Rajput", "Hashmi"
    ]
    prefixes = ["0300", "0301", "0302", "0321", "0333", "0342", "0345", "0312"]
    statuses = ["Safe / Delivered", "High Risk / RTO", "Frequent Returner"]
    
    data = []
    for i in range(1, num_records + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"
        orders = random.randint(1, 10)
        
        status = random.choices(statuses, weights=[70, 20, 10])[0]
        
        if status == "Safe / Delivered":
            rto = 0
        else:
            rto = random.randint(1, orders)
            
        data.append({
            "Customer_ID": f"PK-CUST-{1000 + i}",
            "Customer_Name": name,
            "Phone": phone,
            "Total_Orders": orders,
            "RTO_Count": rto,
            "Risk_Status": status
        })
        
    return pd.DataFrame(data)

# Load database
df_db = generate_pakistani_mock_data(60)

# ==================== INTERFACE 1: MERCHANT LOOKUP ====================
if app_mode == "🔍 Merchant Lookup Portal":
    st.title("🛡️ COD Shield: Merchant Risk Verification")
    st.markdown("Check customer delivery history and RTO risk across multiple Pakistani e-commerce brands before dispatching orders.")
    st.markdown("---")

    search_query = st.text_input("Enter Customer Phone Number or Name:", placeholder="e.g. 0300 or Ali")

    if search_query:
        filtered_df = df_db[
            df_db['Phone'].str.contains(search_query, na=False) | 
            df_db['Customer_Name'].str.contains(search_query, case=False, na=False)
        ]
        if not filtered_df.empty:
            st.success(f"Found {len(filtered_df)} matching record(s) in the Shared Network!")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No risky history found. This customer appears clean in the network!")
    else:
        st.info("💡 Tip: Type a phone prefix (like 0300) or a name to check risk status.")

# ==================== INTERFACE 2: ADMIN DASHBOARD (MOISE) ====================
elif app_mode == "⚙️ Admin Dashboard (Moise)":
    st.title("👑 COD Shield: Owner & Admin Control Panel")
    st.markdown("Welcome back, Moise! Here is the high-level overview of your network performance.")
    st.markdown("---")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    total_customers = len(df_db)
    high_risk_count = len(df_db[df_db['Risk_Status'] != "Safe / Delivered"])
    safe_count = len(df_db[df_db['Risk_Status'] == "Safe / Delivered"])

    col1.metric("Total Network Records", total_customers)
    col2.metric("High Risk / RTO Flagged", high_risk_count)
    col3.metric("Safe / Delivered", safe_count)

    st.markdown("---")
    st.subheader("📋 Full Shared Database Management")
    st.dataframe(df_db, use_container_width=True)
