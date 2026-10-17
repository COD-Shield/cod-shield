import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="COD Shield | Risk Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Header aur default menu chupane ke liye CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# Users Database with Status & Email
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator", "status": "Active", "email": "admin@codshield.pk"},
        "merchant_ali": {"password": "pass123", "role": "Customer", "status": "Active", "email": "ali@store.pk"},
        "merchant_sara": {"password": "pass123", "role": "Customer", "status": "Active", "email": "sara@boutique.pk"}
    }

# User Wallets, Tiers & Detailed Financial Billing Data
if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "merchant_ali": {
            "customer_id": "MERCH_01", "daily_limit": 1200, "used_today": 340, "balance": 45000.0, 
            "total_attempts": 1150, "saved_amount": 340000, "tier": "Platinum 💎", "status": "Paid",
            "base_billing": 40000.0, "ait": 1800.0, "gst": 3200.0, "previous_os": 5000.0, 
            "payment_received": 50000.0, "bill_sent_date": "2026-10-01"
        },
        "merchant_sara": {
            "customer_id": "MERCH_02", "daily_limit": 500, "used_today": 120, "balance": 18000.0, 
            "total_attempts": 650, "saved_amount": 142000, "tier": "Gold 🥇", "status": "Pending",
            "base_billing": 15000.0, "ait": 675.0, "gst": 1200.0, "previous_os": 2500.0, 
            "payment_received": 0.0, "bill_sent_date": "2026-10-05"
        }
    }

# Comprehensive Audit & System Activity Logs Database
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = [
        {"Date": "2026-10-12", "Customer_ID": "MERCH_01", "Customer_Name": "merchant_ali", "Action": "Network-wide Audit / Risk Screen", "Details": "Phone 03001234567 checked - HIGH Risk"},
        {"Date": "2026-10-12", "Customer_ID": "MERCH_02", "Customer_Name": "merchant_sara", "Action": "Dynamic Quota & Limit Enhancement", "Details": "Limit increased from 300 to 500"},
        {"Date": "2026-10-11", "Customer_ID": "MERCH_03", "Customer_Name": "merchant_hamza", "Action": "Merchant Onboarding & Account Creation", "Details": "New Bronze account created"},
        {"Date": "2026-10-10", "Customer_ID": "MERCH_04", "Customer_Name": "merchant_bad", "Action": "Account Deletion & Suspension", "Details": "Suspended due to policy violation"}
    ]

# Mock Database for Phone Lookups
if 'lookup_db' not in st.session_state:
    st.session_state.lookup_db = {
        "03001234567": {"risk": "HIGH", "score": "89%", "total": 14, "delivered": 3, "returned": 11, "comment": "Chronic returner across multiple courier networks. High COD refusal rate."},
        "03219876543": {"risk": "LOW", "score": "4%", "total": 22, "delivered": 21, "returned": 1, "comment": "Trusted buyer with clean fulfillment history. Safe for dispatch."},
        "03335554433": {"risk": "MEDIUM", "score": "45%", "total": 8, "delivered": 5, "returned": 3, "comment": "Moderate return frequency. Verify address via WhatsApp before dispatch."}
    }

# Dynamic Styling
hide_sidebar_css = """
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    .stApp {
        background-color: #f4f6f4 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 2rem !important;
    }
    .marquee-container {
        background: linear-gradient(135deg, #0e3b2e 0%, #1f6f54 100%);
        color: #a3e635;
        padding: 12px 0;
        border-radius: 8px;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 4px 15px rgba(14, 59, 46, 0.15);
        margin-bottom: 25px;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 0.03em;
    }
    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    .exec-heading {
        font-size: 30px;
        font-weight: 700;
        color: #0e3b2e;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }
    .exec-sub {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.5;
        margin-bottom: 20px;
    }
    .problem-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #ef4444;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .status-badge {
        background-color: #0e3b2e;
        color: #5fb88a;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    .footer-box {
        margin-top: 40px;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
        color: #6b7280;
        font-size: 12px;
        text-align: center;
        line-height: 1.6;
    }
"""

if not st.session_state.logged_in:
    hide_sidebar_css += """
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    """

hide_sidebar_css += "</style>"
st.markdown(hide_sidebar_css, unsafe_allow_html=True)

current_year = datetime.now().year

if not st.session_state.logged_in:
    # Landing Page Top Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([2.8, 1.4, 0.8])
    with col_nav1:
        st.markdown("**🛡️ COD SHIELD** &nbsp;<span style='color: #4b5563; font-size: 12px;'>— <b>We Protect your margins to avoid BLIND COD shipping.</b></span>", unsafe_allow_html=True)
    with col_nav2:
        selected_lang = st.selectbox("Language / زبان / لغة", ["English", "اردو", "العربية"], index=["English", "اردو", "العربية"].index(st.session_state.lang), label_visibility="collapsed")
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()
    with col_nav3:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>● V2.0 LIVE</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="marquee-container">
            <div class="marquee-text">
                🚨 STOP SHIPPING BLIND! &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>We Protect your margins to avoid BLIND COD shipping.</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Save your stock, labor, and courier freight before dispatch! &nbsp;&nbsp;&bull;&nbsp;&nbsp; 📦 Shield your e-commerce business today.
            </div>
        </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([1.5, 1], gap="large")

    with left_col:
        st.markdown('<p class="exec-heading">Executive Summary & Risk Intelligence</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="exec-sub">Cash on Delivery (COD) accounts for over 85% of retail transactions in South Asian e-commerce. However, chronic returners and fake orders cause severe financial bleeding. COD Shield is a collective pre-dispatch intelligence platform designed to eliminate blind shipping.</p>',
            unsafe_allow_html=True
        )
        
        # --- بڑا اور نمایاں ویژول ایلیمنٹ: Fake-COD = Profit Margin BLEED ---
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 2px solid #ef4444; padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);">
            <span style="font-size: 36px;">📦 ➔ ❌ ➔ 💸</span><br><br>
            <b style="color: #dc2626; font-size: 20px; letter-spacing: 0.02em;">Fake-COD = Profit Margin BLEED</b><br>
            <p style="font-size: 14px; color: #7f1d1d; margin-top: 8px; margin-bottom: 0px;">Unverified orders ➔ Return-to-Origin (RTO) ➔ Zero Profit!</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🚨 The Core Problem: Where Merchants Lose Money")
        st.markdown("""
        <div class="problem-box">
            <b>📦 Stock & Tear Damage</b><br>
            <span style="font-size: 13px; color: #4b5563;">Returned items frequently come back with crushed boxes, torn packaging, and unserviceable inventory that cannot be resold.</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="problem-box">
            <b>💸 Two-Way Freight Drain</b><br>
            <span style="font-size: 13px; color: #4b5563;">Merchants pay double courier charges (dispatch + return transit) on every failed or refused delivery.</span>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 700; color: #0e3b2e; margin-bottom: 5px;'>🛡️ Portal Login</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #4b5563; font-size: 13px; margin-bottom: 20px;'>Sign in as Admin or Merchant.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In Securely", type="primary", use_container_width=True):
                if username in st.session_state.users_db:
                    user_info = st.session_state.users_db[username]
                    if user_info["status"] == "Disabled":
                        st.error("This account has been disabled by Admin.")
                    elif user_info["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_role = user_info["role"]
                        st.rerun()
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("User not found.")

    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b><br>
            Disclaimer: We COD Shield provides pre-dispatch risk intelligence based on historical data. We do not guarantee 100% delivery success or replace direct buyer confirmation. Merchants retain sole discretion over order dispatch decisions.
        </div>
    """, unsafe_allow_html=True)

else:
    curr_user = st.session_state.current_user
    user_role = st.session_state.user_role

    # ==================== ADMIN PORTAL ====================
    if user_role == "Administrator":
        with st.sidebar:
            st.markdown("### 👑 ADMIN CONTROL PANEL")
            st.markdown(f"<span style='color: #4b5563; font-size: 12px;'>Logged in as: <b>ADMIN</b></span>", unsafe_allow_html=True)
            st.markdown("---")
            admin_nav = st.radio("Admin Menu", ["Merchant Management & Bulk", "Add New Merchant", "Comprehensive Billing Report", "Invoice Generator & Email", "System Activity Logs"])
            st.markdown("---")
            
            send_customer_email = st.checkbox("Send Auto-Email to Customer on Action", value=True)
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

        total_merchants = len(st.session_state.user_wallets)
        total_net_scans = sum(w['total_attempts'] for w in st.session_state.user_wallets.values())
        total_net_savings = sum(w['saved_amount'] for w in st.session_state.user_wallets.values())

        k1, k2, k3 = st.columns(3)
        with k1:
            with st.container(border=True):
                st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL ACTIVE MERCHANTS</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='margin:4px 0 0 0; color:#0e3b2e;'>{total_merchants}</h3>", unsafe_allow_html=True)
        with k2:
            with st.container(border=True):
                st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>NETWORK TOTAL SCANS</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='margin:4px 0 0 0; color:#2563eb;'>{total_net_scans:,}</h3>", unsafe_allow_html=True)
        with k3:
            with st.container(border=True):
                st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL NETWORK SAVINGS</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {total_net_savings:,}</h3>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if admin_nav == "Merchant Management & Bulk":
            st.markdown("## 👥 Merchant Account Management & Bulk Controls")
            st.markdown("Search merchants globally, update individual/bulk limits, toggle payment statuses, or suspend accounts.")
            
            st.markdown("<br>", unsafe_allow_html=True)

            s_col1, s_col2 = st.columns([2, 2])
            with s_col1:
                search_term = st.text_input("🔍 Global Search Merchant (Username or ID)").lower()
            with s_col2:
                bulk_tier_target = st.selectbox("Target Tier for Bulk Quota Upgrade", ["All Tiers", "Platinum 💎", "Gold 🥇", "Silver 🥈", "Bronze 🥉"])
                bulk_add_limit = st.number_input("Add Extra Scans in Bulk", value=100, step=50)
                if st.button("Apply Bulk Quota Upgrade", type="primary"):
                    for m_key, m_val in st.session_state.user_wallets.items():
                        if bulk_tier_target == "All Tiers" or m_val['tier'] == bulk_tier_target:
                            m_val['daily_limit'] += bulk_add_limit
                    
                    st.session_state.audit_logs.insert(0, {
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Customer_ID": "BULK_SYS",
                        "Customer_Name": "Admin",
                        "Action": "Dynamic Quota & Limit Enhancement",
                        "Details": f"Bulk added {bulk_add_limit} scans to {bulk_tier_target}"
                    })
                    st.success(f"Successfully upgraded daily limit for `{bulk_tier_target}`!")
                    st.rerun()

            st.markdown("---")

            for merchant_id in list(st.session_state.user_wallets.keys()):
                if search_term and search_term not in merchant_id.lower() and search_term not in st.session_state.user_wallets[merchant_id]['customer_id'].lower():
                    continue

                data = st.session_state.user_wallets[merchant_id]
                m_status = st.session_state.users_db[merchant_id]["status"]
                m_email = st.session_state.users_db[merchant_id]["email"]

                with st.container(border=True):
                    col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1.5, 1.5, 2])
                    with col_m1:
                        st.markdown(f"**Merchant:** `{merchant_id}` (`{data['customer_id']}`)")
                        st.markdown(f"Email: `{m_email}`<br>Status: **{m_status}** | Tier: **{data['tier']}**", unsafe_allow_html=True)
                    with col_m2:
                        new_limit = st.number_input(f"Limit ({merchant_id})", value=data['daily_limit'], step=50, key=f"lim_{merchant_id}")
                        pay_status = st.selectbox(f"Payment ({merchant_id})", ["Paid", "Pending"], index=0 if data['status']=='Paid' else 1, key=f"pay_{merchant_id}")
                        data['status'] = pay_status
                    with col_m3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Update Details", key=f"upd_{merchant_id}", use_container_width=True):
                            st.session_state.user_wallets[merchant_id]['daily_limit'] = new_limit
                            st.session_state.audit_logs.insert(0, {
                                "Date": datetime.now().strftime("%Y-%m-%d"),
                                "Customer_ID": data['customer_id'],
                                "Customer_Name": merchant_id,
                                "Action": "Tier & Wallet Overview",
                                "Details": f"Limit set to {new_limit}, Payment: {pay_status}"
                            })
                            st.success("Updated successfully!")
                            if send_customer_email:
                                st.toast(f"✉️ Notification email sent to {m_email}", icon="✅")
                            st.rerun()
                    with col_m4:
                        st.markdown("<br>", unsafe_allow_html=True)
                        c_btn1, c_btn2 = st.columns(2)
                        with c_btn1:
                            if m_status == "Active":
                                if st.button("Disable", key=f"dis_{merchant_id}"):
                                    st.session_state.users_db[merchant_id]["status"] = "Disabled"
                                    st.session_state.audit_logs.insert(0, {
                                        "Date": datetime.now().strftime("%Y-%m-%d"),
                                        "Customer_ID": data['customer_id'],
                                        "Customer_Name": merchant_id,
                                        "Action": "Account Deletion & Suspension",
                                        "Details": "Account disabled by admin"
                                    })
                                    if send_customer_email:
                                        st.toast(f"✉️ Suspension alert sent to {m_email}", icon="⚠️")
                                    st.rerun()
                            else:
                                if st.button("Enable", key=f"enb_{merchant_id}"):
                                    st.session_state.users_db[merchant_id]["status"] = "Active"
                                    st.rerun()
                        with c_btn2:
                            if st.button("Delete", key=f"del_{merchant_id}", type="primary"):
                                del st.session_state.users_db[merchant_id]
                                del st.session_state.user_wallets[merchant_id]
                                st.success("Deleted!")
                                st.rerun()

        elif admin_nav == "Add New Merchant":
            st.markdown("## ➕ Onboard New Merchant Account")
            st.markdown("Create a new merchant profile with customized login credentials and screening limits.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(border=True):
                new_m_user = st.text_input("New Merchant Username")
                new_m_pass = st.text_input("New Merchant Password", type="password")
                new_m_email = st.text_input("Merchant Email Address")
                new_m_limit = st.number_input("Initial Daily Screening Limit", value=200, step=50)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Create Merchant Account", type="primary", use_container_width=True):
                    if not new_m_user or not new_m_pass or not new_m_email:
                        st.error("Please provide username, password, and email address.")
                    elif new_m_user in st.session_state.users_db:
                        st.error("Merchant username already exists!")
                    else:
                        cust_id = f"MERCH_0{len(st.session_state.user_wallets) + 1}"
                        st.session_state.users_db[new_m_user] = {"password": new_m_pass, "role": "Customer", "status": "Active", "email": new_m_email}
                        st.session_state.user_wallets[new_m_user] = {
                            "customer_id": cust_id, "daily_limit": new_m_limit, "used_today": 0, 
                            "balance": 10000.0, "total_attempts": 5, "saved_amount": 1500, "tier": "Bronze 🥉", "status": "Pending",
                            "base_billing": 8000.0, "ait": 360.0, "gst": 640.0, "previous_os": 0.0, "payment_received": 0.0, "bill_sent_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        st.session_state.audit_logs.insert(0, {
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Customer_ID": cust_id,
                            "Customer_Name": new_m_user,
                            "Action": "Merchant Onboarding & Account Creation",
                            "Details": f"New merchant onboarded with email {new_m_email}"
                        })
                        st.success(f"Merchant `{new_m_user}` created successfully!")

        elif admin_nav == "Comprehensive Billing Report":
            st.markdown("## 💳 Comprehensive Accounting & Billing Report")
            st.markdown("Detailed financial statement including Base Billing, AIT, GST, Previous OS, Payment Received, and Total Payable.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            billing_records = []
            for m_name, m_data in st.session_state.user_wallets.items():
                m_email = st.session_state.users_db[m_name]["email"]
                base = m_data.get('base_billing', 10000.0)
                ait = m_data.get('ait', 450.0)
                gst = m_data.get('gst', 800.0)
                prev_os = m_data.get('previous_os', 0.0)
                paid = m_data.get('payment_received', 0.0)
                
                total_payable = (base + ait + gst + prev_os) - paid
                
                billing_records.append({
                    "Customer Name": m_name,
                    "Package / Tier": m_data['tier'],
                    "Customer ID": m_data['customer_id'],
                    "Base Billing (Rs.)": base,
                    "AIT (Rs.)": ait,
                    "GST (Rs.)": gst,
                    "Payable (Rs.)": base + ait + gst,
                    "Previous OS (Rs.)": prev_os,
                    "Payment Received (Rs.)": paid,
                    "Total Payable (Rs.)": total_payable,
                    "Email ID": m_email,
                    "Bill Sent Date": m_data.get('bill_sent_date', '2026-10-01')
                })
            
            df_comp_billing = pd.DataFrame(billing_records)
            st.dataframe(df_comp_billing, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            csv_comp = df_comp_billing.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Comprehensive Billing Report (Excel/CSV format)",
                data=csv_comp,
                file_name=f"COD_Shield_Comprehensive_Billing_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

        elif admin_nav == "Invoice Generator & Email":
            st.markdown("## 🧾 Corporate Invoice Generator, PDF & Automated Email")
            st.markdown("Select a merchant, view billing details, download as PDF, and dispatch invoice via automated email.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            selected_merchant = st.selectbox("Select Merchant for Invoice", list(st.session_state.user_wallets.keys()))
            
            if selected_merchant:
                m_info = st.session_state.user_wallets[selected_merchant]
                m_email = st.session_state.users_db[selected_merchant].get("email", "merchant@store.pk")
                invoice_no = f"INV-{datetime.now().strftime('%Y%m')}-{m_info['customer_id']}"
                
                st.markdown("<br>", unsafe_allow_html=True)
                with st.container(border=True):
                    col_inv1, col_inv2 = st.columns(2)
                    with col_inv1:
                        st.markdown("### **COD Shield (Pvt) Ltd**")
                        st.markdown("Pre-dispatch Risk Intelligence Platform<br>Islamabad, Pakistan", unsafe_allow_html=True)
                    with col_inv2:
                        st.markdown(f"<div style='text-align: right;'><b>Invoice Number:</b> {invoice_no}<br><b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}<br><b>Billing Period:</b> {datetime.now().strftime('%B %Y')}</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown(f"**Billed To:** `{selected_merchant}` | **Email:** `{m_email}` (Customer ID: `{m_info['customer_id']}`)")
                    st.markdown(f"**Account Tier:** {m_info['tier']}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    base = m_info.get('base_billing', 10000.0)
                    ait = m_info.get('ait', 450.0)
                    gst = m_info.get('gst', 800.0)
                    total_p = base + ait + gst

                    inv_items = pd.DataFrame([
                        {"Description": f"Subscription Base Billing ({m_info['tier']})", "Amount (Rs.)": base},
                        {"Description": "AIT (Advance Income Tax)", "Amount (Rs.)": ait},
                        {"Description": "GST (General Sales Tax)", "Amount (Rs.)": gst}
                    ])
                    st.dataframe(inv_items, use_container_width=True)
                    
                    st.markdown(f"<div style='text-align: right;'><h4>Total Net Payable: Rs. {total_p:,.2f}</h4></div>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("*Note: Verified accounting statement generated via COD Shield Enterprise Gateway.*")

                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    invoice_text = f"COD Shield Invoice: {invoice_no}\nMerchant: {selected_merchant}\nTotal Payable: Rs. {total_p:,.2f}\nStatus: {m_info['status']}"
                    st.download_button(
                        label="📄 Download Invoice PDF",
                        data=invoice_text,
                        file_name=f"{invoice_no}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                with b_col2:
                    if st.button("✉️ Send Invoice via Automated Email", use_container_width=True):
                        st.session_state.audit_logs.insert(0, {
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Customer_ID": m_info['customer_id'],
                            "Customer_Name": selected_merchant,
                            "Action": "Automated Email Invoice Dispatch",
                            "Details": f"Invoice {invoice_no} successfully sent to {m_email}"
                        })
                        st.success(f"Invoice {invoice_no} successfully emailed to `{m_email}`!")

        elif admin_nav == "System Activity Logs":
            st.markdown("## 📊 System Activity & Audit Logs")
            st.markdown("Filter network activities by date range and export complete audit reports.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                start_date = st.date_input("Start Date", value=datetime.strptime("2026-10-01", "%Y-%m-%d").date())
            with f_col2:
                end_date = st.date_input("End Date", value=datetime.now().date())

            df_logs = pd.DataFrame(st.session_state.audit_logs)
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(df_logs, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Audit Report (Excel/CSV format)",
                data=csv_data,
                file_name=f"COD_Shield_Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

    # ==================== CUSTOMER PORTAL ====================
    else:
        wallet = st.session_state.user_wallets.get(curr_user, {"customer_id": "MERCH_99", "daily_limit": 500, "used_today": 0, "balance": 5000.0, "total_attempts": 0, "saved_amount": 10000, "tier": "Bronze 🥉", "status": "Pending"})
        
        if wallet['total_attempts'] >= 1000:
            wallet['tier'] = "Platinum 💎"
        elif wallet['total_attempts'] >= 300:
            wallet['tier'] = "Gold 🥇"
        elif wallet['total_attempts'] >= 100:
            wallet['tier'] = "Silver 🥈"
        else:
            wallet['tier'] = "Bronze 🥉"

        with st.sidebar:
            st.markdown("### 🛡️ COD SHIELD WORKSPACE")
            st.markdown(f"<span style='color: #4b5563; font-size: 12px;'>Merchant: <b>{curr_user.upper()}</b><br>Tier: <b>{wallet['tier']}</b></span>", unsafe_allow_html=True)
            st.markdown("---")
            
            nav_choice = st.radio("Navigation", ["Dashboard Overview", "Single Order Risk Check", "Bulk CSV Upload", "Wallet & Quota"])
            
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

        if nav_choice == "Dashboard Overview":
            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.markdown(f"**🛡️ Welcome Back, {curr_user.upper()}** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Tier: {wallet['tier']}</span>", unsafe_allow_html=True)
            with col_h2:
                st.markdown(f"<div style='text-align: right;'><span class='status-badge'>● LIVE</span></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class="marquee-container" style="margin-bottom: 20px;">
                    <div class="marquee-text">
                        🛡️ ACTIVE PROTECTION MODE &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>We Protect your margins to avoid BLIND COD shipping.</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Screen your orders before dispatch to save courier freight.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                with st.container(border=True):
                    st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL SCANS</p>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0e3b2e;'>{wallet['total_attempts']}</h2>", unsafe_allow_html=True)
            with m2:
                with st.container(border=True):
                    st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>QUOTA UTILIZED</p>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#2563eb;'>{wallet['used_today']} / {wallet['daily_limit']}</h2>", unsafe_allow_html=True)
            with m3:
                with st.container(border=True):
                    st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>REMAINING QUOTA</p>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#16a34a;'>{max(wallet['daily_limit'] - wallet['used_today'], 0)}</h2>", unsafe_allow_html=True)
            with m4:
                with st.container(border=True):
                    st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>ESTIMATED SAVINGS</p>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {wallet['saved_amount']:,}</h2>", unsafe_allow_html=True)

        elif nav_choice == "Single Order Risk Check":
            st.markdown("## 🔍 Single Order Risk Intelligence")
            st.markdown("Enter customer phone number to screen historical refusal patterns before dispatch.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.container(border=True):
                col_inp1, col_inp2 = st.columns([3, 1])
                with col_inp1:
                    search_query = st.text_input("Customer Phone Number (e.g. 03001234567 or try 03219876543)")
                with col_inp2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    search_btn = st.button("Screen Order", type="primary", use_container_width=True)

            if search_btn:
                if not search_query:
                    st.warning("Please enter a valid phone number.")
                elif wallet['used_today'] >= wallet['daily_limit']:
                    st.error("Daily quota exhausted! Please contact Admin for a limit upgrade.")
                else:
                    wallet['used_today'] += 1
                    wallet['total_attempts'] += 1
                    
                    result = st.session_state.lookup_db.get(search_query.strip(), {
                        "risk": "UNKNOWN", "score": "15%", "total": 2, "delivered": 1, "returned": 1, "comment": "New buyer with limited historical footprint. Proceed with standard verification."
                    })

                    st.session_state.audit_logs.insert(0, {
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Customer_ID": wallet['customer_id'],
                        "Customer_Name": curr_user,
                        "Action": "Network-wide Audit & Activity Logs",
                        "Details": f"Single lookup for {search_query} - Result: {result['risk']}"
                    })

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Risk Screening Result")

                    r1, r2, r3 = st.columns(3)
                    with r1:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>RISK LEVEL</p>", unsafe_allow_html=True)
                            risk_color = "#dc2626" if result['risk'] == "HIGH" else ("#16a34a" if result['risk'] == "LOW" else "#d97706")
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:{risk_color};'>{result['risk']} RISK</h2>", unsafe_allow_html=True)
                    with r2:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>PREDICTED REFUSAL RATE</p>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#2563eb;'>{result['score']}</h2>", unsafe_allow_html=True)
                    with r3:
                        with st.container(border=True):
                            st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>TOTAL FULFILLMENTS</p>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0e3b2e;'>{result['delivered']} Delivered / {result['returned']} Returned</h2>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown("#### 📝 Network Intelligence Note")
                        st.markdown(f"<p style='color: #4b5563; font-size: 14px;'>{result['comment']}</p>", unsafe_allow_html=True)

        elif nav_choice == "Bulk CSV Upload":
            st.markdown("## 📦 Bulk Order Risk Upload")
            st.markdown("Upload your order manifest CSV file to screen hundreds of phone numbers instantly.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload CSV file containing phone numbers", type=["csv"])
            if uploaded_file is not None:
                df_upload = pd.read_csv(uploaded_file)
                st.success(f"Successfully uploaded {len(df_upload)} records for screening!")
                st.dataframe(df_upload.head(), use_container_width=True)
                if st.button("Run Bulk Risk Screening", type="primary"):
                    st.session_state.audit_logs.insert(0, {
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Customer_ID": wallet['customer_id'],
                        "Customer_Name": curr_user,
                        "Action": "Network-wide Audit & Activity Logs",
                        "Details": f"Bulk CSV screening executed for {len(df_upload)} rows"
                    })
                    st.balloons()
                    st.info("Bulk scanning simulation complete: 85% safe orders identified for dispatch.")

        elif nav_choice == "Wallet & Quota":
            st.markdown("## 💳 Wallet & Quota Management")
            st.markdown(f"Your Account Classification: **{wallet['tier']}**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            w1, w2 = st.columns(2)
            with w1:
                with st.container(border=True):
                    st.markdown("### Account Details")
                    st.markdown(f"<h1 style='color: #16a34a;'>Rs. {wallet['balance']:,.2f}</h1>", unsafe_allow_html=True)
                    st.markdown(f"**Daily Screening Limit:** {wallet['daily_limit']} Scans")
                    st.markdown(f"**Used Today:** {wallet['used_today']} Scans")
            with w2:
                with st.container(border=True):
                    st.markdown("### Request Limit Enhancement")
                    st.markdown("Need a higher tier or increased daily limit? Request an upgrade directly from Admin.")
                    if st.button("Request Limit Upgrade", type="primary"):
                        st.session_state.audit_logs.insert(0, {
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Customer_ID": wallet['customer_id'],
                            "Customer_Name": curr_user,
                            "Action": "Tier & Wallet Overview",
                            "Details": "Requested limit enhancement from admin"
                        })
                        st.success("Upgrade request sent to Admin successfully!")

    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b> &bull; Pre-dispatch Risk Intelligence Workspace.
        </div>
    """, unsafe_allow_html=True)
