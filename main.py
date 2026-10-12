import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="COD Shield | Risk Intelligence",
    page_icon="🛡️",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator"},
        "operator": {"password": "pass123", "role": "Operator"}
    }

if 'user_wallets' not in st.session_state:
    st.session_state.user_wallets = {
        "admin": {"daily_limit": 500, "used_today": 42, "balance": 7500.0, "total_attempts": 320, "saved_amount": 142000},
        "operator": {"daily_limit": 50, "used_today": 18, "balance": 450.0, "total_attempts": 85, "saved_amount": 34000}
    }

# Mock Database for Phone Lookups
if 'lookup_db' not in st.session_state:
    st.session_state.lookup_db = {
        "03001234567": {"risk": "HIGH", "score": "89%", "total": 14, "delivered": 3, "returned": 11, "comment": "Chronic returner across multiple courier networks. High COD refusal rate."},
        "03219876543": {"risk": "LOW", "score": "4%", "total": 22, "delivered": 21, "returned": 1, "comment": "Trusted buyer with clean fulfillment history. Safe for dispatch."},
        "03335554433": {"risk": "MEDIUM", "score": "45%", "total": 8, "delivered": 5, "returned": 3, "comment": "Moderate return frequency. Verify address via WhatsApp before dispatch."}
    }

# Dynamic Styling: Perfect top spacing, hides toolbar/sidebar when not logged in
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
    # Top Navigation Bar with Trilingual Toggle
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

    # Running Ticker Window Banner (Marquee)
    st.markdown("""
        <div class="marquee-container">
            <div class="marquee-text">
                🚨 STOP SHIPPING BLIND! &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>We Protect your margins to avoid BLIND COD shipping.</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Save your stock, labor, and courier freight before dispatch! &nbsp;&nbsp;&bull;&nbsp;&nbsp; 📦 Shield your e-commerce business today.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Two Column Layout: Left (Executive Summary & Core Problem) | Right (Login Window)
    left_col, right_col = st.columns([1.5, 1], gap="large")

    with left_col:
        if st.session_state.lang == "English":
            st.markdown('<p class="exec-heading">Executive Summary & Risk Intelligence</p>', unsafe_allow_html=True)
            st.markdown(
                '<p class="exec-sub">Cash on Delivery (COD) accounts for over 85% of retail transactions in South Asian e-commerce. However, chronic returners and fake orders cause severe financial bleeding. COD Shield is a collective pre-dispatch intelligence platform designed to eliminate blind shipping.</p>',
                unsafe_allow_html=True
            )
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
            st.markdown("""
            <div class="problem-box">
                <b>👩‍🏭 Wasted Overhead & Labor</b><br>
                <span style="font-size: 13px; color: #4b5563;">Bubble wrap, custom boxes, tape, and employee man-hours are squandered on dead-end orders.</span>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.lang == "اردو":
            st.markdown('<p class="exec-heading" style="direction: rtl; text-align: right;">خلاصہ اور رسک انٹیلی جنس</p>', unsafe_allow_html=True)
            st.markdown(
                '<p class="exec-sub" style="direction: rtl; text-align: right;">پاکستان اور جنوبی ایشیا میں ای کامرس کا 85 فیصد سے زائد کاروبار کیش آن ڈلیوری (COD) پر ہوتا ہے۔ لیکن اندھا دھند پارسل بھیجنے (Blind Shipping) کی وجہ سے بار بار پارسل واپس آنے سے مرچنٹ کو شدید مالی نقصان اٹھانا پڑتا ہے۔</p>',
                unsafe_allow_html=True
            )
            st.markdown("<h4 style='direction: rtl; text-align: right;'>🚨 اصل نقصان کہاں ہوتا ہے؟</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>📦 اسٹاک اور ڈبہ پھٹنے کا نقصان</b><br>
                <span style="font-size: 13px; color: #4b5563;">واپس آنے والے پارسلز کے اکثر ڈبے پھٹ جاتے ہیں اور پروڈکٹ ناقابلِ فروخت ہو جاتی ہے۔</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>💸 دو طرفہ کوریئر کا کرایہ</b><br>
                <span style="font-size: 13px; color: #4b5563;">فیک آرڈر بھیجنے اور واپس آنے پر مرچنٹ کو ڈبل کوریئر چارجز دینے پڑتے ہیں۔</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>👩‍🏭 برباد لیبر اور پیکنگ</b><br>
                <span style="font-size: 13px; color: #4b5563;">ببل ریپ، ڈبے، ٹیپ اور ملازمین کا وقت ان آرڈرز پر ضائع ہوتا ہے جو کبھی ڈلیور نہیں ہوتے۔</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p class="exec-heading" style="direction: rtl; text-align: right;">الملخص التنفيذي وذكاء المخاطر</p>', unsafe_allow_html=True)
            st.markdown(
                '<p class="exec-sub" style="direction: rtl; text-align: right;">تمثل الدفع عند الاستلام نسبة كبيرة من المعاملات التجارية. ومع ذلك، فإن العملاء المتسببين في الارتجاع المتكرر والطلبات الوهمية تسبب خسائر مالية جسيمة. منصة COD Shield مصممة للقضاء على الشحن الأعمى وحماية هوامش أرباح التجار.</p>',
                unsafe_allow_html=True
            )
            st.markdown("<h4 style='direction: rtl; text-align: right;'>🚨 المشكلة الأساسية: أين يخسر التجار أموالهم؟</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>📦 تلف المخزون والعبوات</b><br>
                <span style="font-size: 13px; color: #4b5563;">تودع المرتجعات غالباً بعبوات ممزقة وبضائع غير صالحة لإعادة البيع.</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>💸 استنزاف رسوم الشحن ذات الاتجاهين</b><br>
                <span style="font-size: 13px; color: #4b5563;">يدفع التجار رسوم شحن مضاعفة (إرسال + إرجاع) لكل تسليم فاشل.</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="problem-box" style="direction: rtl; text-align: right;">
                <b>👩‍🏭 هدر العمالة والتكاليف العامة</b><br>
                <span style="font-size: 13px; color: #4b5563;">يتم إهدار مواد التغليف ووقت الموظفين على طلبات وهمية لن يتم تسليمها أبداً.</span>
            </div>
            """, unsafe_allow_html=True)

    with right_col:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='font-weight: 700; color: #0e3b2e; margin-bottom: 5px;'>🛡️ Merchant Login</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #4b5563; font-size: 13px; margin-bottom: 20px;'>Sign in to access your risk screening workspace.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In Securely", type="primary", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b><br>
            COD Shield provides pre-dispatch risk intelligence based on historical data. We do not guarantee 100% delivery success or replace direct buyer confirmation. Merchants retain sole discretion over order dispatch decisions.
        </div>
    """, unsafe_allow_html=True)

else:
    # Logged-in Workspace with Sidebar Navigation
    curr_user = st.session_state.current_user
    wallet = st.session_state.user_wallets.get(curr_user, {"daily_limit": 50, "used_today": 0, "balance": 500.0, "total_attempts": 0, "saved_amount": 142000})
    remaining_quota = wallet['daily_limit'] - wallet['used_today']

    with st.sidebar:
        st.markdown("### 🛡️ COD SHIELD")
        st.markdown(f"<span style='color: #4b5563; font-size: 12px;'>Logged in as: <b>{curr_user.upper()}</b></span>", unsafe_allow_html=True)
        st.markdown("---")
        
        nav_choice = st.radio("Navigation", ["Dashboard Overview", "Single Order Risk Check", "Wallet & Quota"])
        
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if nav_choice == "Dashboard Overview":
        col_h1, col_h2 = st.columns([4, 1])
        with col_h1:
            st.markdown("**🛡️ COD SHIELD Workspace** &nbsp;<span style='color: #4b5563; font-size: 13px;'>— Operational Overview</span>", unsafe_allow_html=True)
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
                st.markdown(f"<h2 style='margin:4px 0 0 0; color:#16a34a;'>{max(remaining_quota, 0)}</h2>", unsafe_allow_html=True)
        with m4:
            with st.container(border=True):
                st.markdown("<p style='color:#4b5563; font-size:11px; font-weight:700;'>ESTIMATED SAVINGS</p>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='margin:4px 0 0 0; color:#0d9488;'>Rs. {wallet['saved_amount']:,}</h2>", unsafe_allow_html=True)

    elif nav_choice == "Single Order Risk Check":
        st.markdown("## 🔍 Single Order Risk Intelligence")
        st.markdown("Enter customer phone number or order ID to screen historical refusal patterns before dispatch.")
        
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
            else:
                # Check quota
                if remaining_quota <= 0:
                    st.error("Daily quota exhausted! Please top up your wallet.")
                else:
                    # Deduct quota
                    wallet['used_today'] += 1
                    wallet['total_attempts'] += 1
                    
                    # Lookup result
                    result = st.session_state.lookup_db.get(search_query.strip(), {
                        "risk": "UNKNOWN", "score": "15%", "total": 2, "delivered": 1, "returned": 1, "comment": "New buyer with limited historical footprint. Proceed with standard verification."
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

    elif nav_choice == "Wallet & Quota":
        st.markdown("## 💳 Wallet & Quota Management")
        st.markdown("Monitor your screening quota balance and account usage.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        w1, w2 = st.columns(2)
        with w1:
            with st.container(border=True):
                st.markdown("### Account Balance")
                st.markdown(f"<h1 style='color: #16a34a;'>Rs. {wallet['balance']:,.2f}</h1>", unsafe_allow_html=True)
                st.markdown(f"**Daily Limit:** {wallet['daily_limit']} Scans")
                st.markdown(f"**Used Today:** {wallet['used_today']} Scans")
        with w2:
            with st.container(border=True):
                st.markdown("### Top-up Quota")
                st.selectbox("Select Top-up Package", ["Starter Pack (+500 Scans) - Rs. 3,000", "Growth Pack (+2,000 Scans) - Rs. 10,000"])
                if st.button("Top-up Instantly", type="primary"):
                    st.success("Top-up request initiated successfully!")

    # Footer for Dashboard
    st.markdown(f"""
        <div class="footer-box">
            <b>© {current_year} COD Shield. All rights reserved.</b> &bull; Pre-dispatch Risk Intelligence Workspace.
        </div>
    """, unsafe_allow_html=True)
