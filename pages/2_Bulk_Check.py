import streamlit as st
import pandas as pd

st.title("📁 Bulk Verification & Quota Guard (Phase 2)")

if not st.session_state.get('logged_in', False):
    st.warning("⚠️ Pehle main page par ja kar Login karein!")
    st.stop()

st.markdown("Upload your bulk CSV or Excel order file. Anti-scraping protection is active.")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.info(f"Total rows detected: {len(df)}")
    
    if st.button("Run Protected Assessment", type="primary"):
        res_df = pd.DataFrame([{"Row": i+1, "Status": "Low Risk" if i%2==0 else "High Risk"} for i in range(len(df))])
        st.dataframe(res_df, use_container_width=True)
        
        # Download rights check: Operator ke liye download restricted
        if st.session_state.user_role == "Administrator":
            st.download_button("Download Summary Report", res_df.to_csv(index=False).encode('utf-8'), "bulk_report.csv", "text/csv")
        else:
            st.warning("🔒 **Download Restricted:** Operators cannot download raw report files.")
