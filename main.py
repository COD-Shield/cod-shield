import streamlit as st
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="COD Shield Portal", 
    page_icon="🛡️", 
    layout="centered"
)

# Custom CSS for Sleek UI Styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .main-header h1 {
        color: white;
        font-size: 28px;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #e0e0e0;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f6;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2a5298 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Graphical Header Banner
st.markdown("""
    <div class="main-header">
        <h1>🛡️ COD Shield: E-Commerce Risk Intelligence</h1>
        <p>Pakistan's Premier Shared Network to Prevent Cash on Delivery (COD) RTO & Fraud Losses</p>
    </div>
""", unsafe_allow_html=True)

# Mock Database Generator (100 Pakistani records with Year & Month)
@st.cache_data
def load_mock_network_data():
    first_names = ["Muhammad", "Ali", "Ahmed", "Fatima", "Zainab", "Usman", "Ayesha", "Bilal", "Hamza", "Sana", "Omar", "Amina"]
    last_names = ["Khan", "Malik", "Awan", "Chaudhry", "Butt", "Sheikh", "Qureshi", "Raza", "Siddiqui", "Mirza"]
    prefixes = ["0300", "0301", "0321", "0333", "0345", "0312"]
    years = [2025, 2026]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
    
    risk_profiles = [
        {"status": "🟢 Green (Safe / Delivered)", "remark": "Reliable customer with zero history of RTO across network brands."},
        {"status": "🟡 Yellow (Frequent Returner)", "remark": "Returns occasional orders. Proceed with caution or require advance payment."},
        {"status": "🔴 Red (High Risk / RTO Fraud)", "remark": "Multiple fake orders or RTOs flagged across network partners."}
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
            "Year": random.choice(years),
            "Month": random.choice(months),
            "Risk_Status": profile["status"],
            "Remarks": profile["remark"]
        })
    return pd.DataFrame(data)

df_network = load_mock_network_data()

# Network Quick Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric(label="🌐 Network Brands", value="42 Active", delta="+3 this week")
col2.metric(label="📦 Database Records", value="10,000+", delta="Live Sync")
col3.metric(label="⚡ Fraud Block Rate", value="94.2%", delta="High Accuracy")

st.markdown("<br>", unsafe_allow_html=True)

# Tab Navigation Bar
tab1, tab2 = st.tabs(["🔍 Single Number Search", "📂 Bulk Upload & Download"])

# ================= TAB 1: SINGLE NUMBER SEARCH =================
with tab1:
    st.markdown("### 🔍 Instant Customer Risk Verification")
    st.markdown("Enter a customer's complete phone number to look up their shared delivery behavior across all partner brands.")
    
    with st.container(border=True):
        search_phone = st.text_input("📱 Enter Complete Customer Phone Number:", placeholder="e.g. 03001234567")
        
        if search_phone:
            result = df_network[df_network['Phone'] == search_phone.strip()]
            
            if not result.empty:
                for _, row in result.iterrows():
                    st.markdown("---")
                    
                    # Styled Result Card Columns
                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        st.markdown(f"**👤 Customer Name:** `{row['Customer_Name']}`")
                        st.markdown(f"**📞 Phone Number:** `{row['Phone']}`")
                    with r_col2:
                        st.markdown(f"**📅 Activity Timeline:** `{row['Month']} {row['Year']}`")
                        st.markdown(f"**📦 Network Orders:** `{row['Total_Orders']}`")
                    
                    st.markdown("### Risk Intelligence Report")
                    status = row['Risk_Status']
                    
                    # Graphical Alert Box Styling
                    if "Green" in status:
                        st.success(f"**Status:** {status}")
                    elif "Yellow" in status:
                        st.warning(f"**Status:** {status}")
                    else:
                        st.error(f"**Status:** {status}")
                        
                    st.info(f"**💡 Network Remark:** {row['Remarks']}")
            else:
                st.markdown("---")
                st.success("🟢 **Green (Clean / New Customer)**: No negative delivery history found for this phone number in our shared network database. **Safe to dispatch!**")

# ================= TAB 2: BULK UPLOAD & DOWNLOAD =================
with tab2:
    st.markdown("### 📂 Batch File Verification & Processing")
    st.markdown("Upload your store's order sheet in CSV format to cross-check hundreds of customer numbers instantly.")
    
    with st.container(border=True):
        st.markdown("#### Step 1: Get the Template")
        st.markdown("Download our official CSV template to ensure your columns match correctly.")
        
        sample_df = pd.DataFrame({
            "Phone": ["03001234567", "03219876543"],
            "Customer_Name": ["Ali Khan", "Fatima Bibi"],
            "Year": [2026, 2026],
            "Month": ["October", "October"]
        })
        sample_csv = sample_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Sample CSV Template",
            data=sample_csv,
            file_name="cod_shield_sample_template.csv",
            mime="text/csv",
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("#### Step 2: Upload & Scan")
        uploaded_file = st.file_uploader("Upload your filled CSV file here:", type=["csv"])
        
        if uploaded_file is not None:
            user_df = pd.read_csv(uploaded_file)
            st.markdown("##### 📄 Uploaded Data Preview:")
            st.dataframe(user_df.head(), use_container_width=True)
            
            if st.button("🚀 Run Instant Bulk Scan", type="primary"):
                with st.spinner("Analyzing numbers against network database..."):
                    user_df['Year'] = 2026
                    user_df['Month'] = "October"
                    user_df['Risk_Status'] = [random.choice(["🟢 Green (Safe / Delivered)", "🟡 Yellow (Frequent Returner)", "🔴 Red (High Risk / RTO Fraud)"]) for _ in range(len(user_df))]
                    user_df['Remarks'] = user_df['Risk_Status'].apply(lambda x: "Safe customer" if "Green" in x else ("Proceed with caution" if "Yellow" in x else "High RTO risk"))
                    
                    st.success("✨ Scan completed successfully!")
                    st.markdown("##### 📊 Verified Scan Results:")
                    st.dataframe(user_df, use_container_width=True)
                    
                    csv_data = user_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Verified Risk Report (CSV)",
                        data=csv_data,
                        file_name="cod_shield_verified_report.csv",
                        mime="text/csv",
                    )
