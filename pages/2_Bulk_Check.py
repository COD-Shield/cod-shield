import streamlit as st
import pandas as pd

st.set_page_config(page_title="COD Shield - Bulk Verification", page_icon="📦", layout="wide")

st.title("📦 Bulk Order Verification & Batch Scan")
st.markdown("Upload your CSV file containing customer phone numbers to verify batch RTO risk status.")

# سیمپل ٹیمپلیٹ ڈاؤن لوڈ
sample_data = pd.DataFrame({
    "Phone": ["03001234567", "03219876543"],
    "Customer_Name": ["Ali Khan", "Ahmed Raza"],
    "Year": [2026, 2026],
    "Month": ["October", "October"]
})
csv_sample = sample_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Sample CSV Template",
    data=csv_sample,
    file_name="cod_shield_sample_template.csv",
    mime="text/csv"
)

st.markdown("---")
uploaded_file = st.file_uploader("Upload Filled CSV File", type=["csv"])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:", input_df.head())
    
    if st.button("Run Bulk Scan 🔍"):
        # فرضی اسکین لاجک
        input_df["Risk_Status"] = "Green (Safe)"
        input_df["Remarks"] = "No matching fraud risk detected in network."
        
        st.success("Bulk scan completed successfully!")
        st.dataframe(input_df)
        
        # رزلٹ ڈاؤن لوڈ بٹن
        result_csv = input_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Verified Risk Report (CSV)",
            data=result_csv,
            file_name="cod_shield_verified_report.csv",
            mime="text/csv"
        )
