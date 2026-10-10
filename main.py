import pandas as pd
import random

# Pakistani Mock Database Generator
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

st.markdown("---")
st.subheader("🔍 Merchant Network Lookup")

# Search bar widget
search_query = st.text_input("Search Customer by Phone Number or Name:", placeholder="e.g. 0300 or Ali")

if search_query:
    filtered_df = df_db[
        df_db['Phone'].str.contains(search_query, na=False) | 
        df_db['Customer_Name'].str.contains(search_query, case=False, na=False)
    ]
    if not filtered_df.empty:
        st.success(f"Found {len(filtered_df)} matching record(s) in the Shared Network!")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No records found. This customer is clean / new to the network!")
else:
    st.info("Sample network database preview (Showing first 10 records):")
    st.dataframe(df_db.head(10), use_container_width=True)
