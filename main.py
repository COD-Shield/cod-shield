import hashlib
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="COD Shield Portal", page_icon="🛡️", layout="centered"
)

st.title("🛡️ COD Shield: Secure E-Commerce Risk Intelligence")
st.markdown(
    "A secure cloud network for e-commerce brands to prevent Cash on"
    " Delivery (COD) RTO and fake order losses."
)

# Database File Path (Persistent Storage)
DB_FILE = "cod_database.csv"


def load_db():
  if not os.path.exists(DB_FILE):
    initial_data = {
        "phone_hash": [
            hashlib.sha256("03001234567".strip().encode("utf-8")).hexdigest(),
            hashlib.sha256("03219876543".strip().encode("utf-8")).hexdigest(),
            hashlib.sha256("03335557788".strip().encode("utf-8")).hexdigest(),
        ],
        "total_orders": [5, 4, 3],
        "rto_count": [0, 4, 2],
        "status": ["GREEN", "RED", "YELLOW"],
    }
    df = pd.DataFrame(initial_data)
    df.to_csv(DB_FILE, index=False)
  return pd.read_csv(DB_FILE)


def save_db(df):
  df.to_csv(DB_FILE, index=False)


def hash_phone(phone):
  return hashlib.sha256(phone.strip().encode("utf-8")).hexdigest()


df_db = load_db()

# Tabs for Lookup, Reporting, and API Reference
tabs = st.tabs(
    ["🔍 Customer Lookup", "➕ Report Order Status", "🔌 API & Shopify Guide"]
)

with tabs[0]:
  st.subheader("Check Customer Risk Score")
  phone_input = st.text_input(
      "Enter Customer Phone Number (e.g., 03001234567):", ""
  )
  payment_type = st.selectbox(
      "Current Order Payment Type:",
      ["Cash on Delivery (COD)", "Prepaid (Full Advance)"],
  )

  if st.button("Check Score & Recommendations"):
    if phone_input:
      p_hash = hash_phone(phone_input)
      record = df_db[df_db["phone_hash"] == p_hash]

      st.markdown("---")

      # Prepaid logic: Zero financial risk, no direction required
      if payment_type == "Prepaid (Full Advance)":
        st.success(
            "⚡ **Prepaid: No Direction Required**\n\nPayment is already"
            " secured via online payment. Zero financial risk. Safe to"
            " dispatch immediately!"
        )
      elif record.empty:
        st.success(
            "🟢 **Green: Recommended**\n\nNo negative history found in the"
            " network. Safe to dispatch with COD."
        )
      else:
        total = int(record["total_orders"].values[0])
        rto = int(record["rto_count"].values[0])
        status = record["status"].values[0]

        if status == "RED":
          st.error(
              f"🔴 **Red: Fake - Not Recommended**\n\n- Total Orders:"
              f" {total}\n- Refused Parcels (RTO): {rto}\n\n⚠️ **Action:**"
              " High risk of RTO. Disable COD or require full advance"
              " payment."
          )
        elif status == "YELLOW":
          st.warning(
              f"🟡 **Yellow: Not Recommended without Advance Delivery"
              f" Charges**\n\n- Total Orders: {total}\n- Refused Parcels"
              f" (RTO): {rto}\n\n⚡ **Action:** Verify via phone/WhatsApp"
              " and collect delivery charges advance."
          )
        else:
          st.success(
              f"🟢 **Green: Recommended**\n\n- Total Orders:"
              f" {total}\n- Refused Parcels (RTO): {rto}\n\nReliable customer"
              " history. Safe to dispatch with COD."
          )
    else:
      st.warning("Please enter a valid phone number.")

with tabs[1]:
  st.subheader("Report Delivery Outcome")
  rep_phone = st.text_input("Customer Phone Number:", key="rep_phone")
  rep_method = st.selectbox("Order Payment Method Used:", ["COD", "Prepaid"])
  rep_status = st.selectbox(
      "Parcel Final Status:",
      ["Successfully Delivered", "Refused / RTO (Returned)"],
  )

  if st.button("Save Feedback & Update Score"):
    if rep_phone:
      p_hash = hash_phone(rep_phone)
      df_db = load_db()

      if p_hash in df_db["phone_hash"].values:
        idx = df_db[df_db["phone_hash"] == p_hash].index[0]
        df_db.loc[idx, "total_orders"] += 1
        if "Refused" in rep_status:
          df_db.loc[idx, "rto_count"] += 1
      else:
        new_row = pd.DataFrame({
            "phone_hash": [p_hash],
            "total_orders": [1],
            "rto_count": [1 if "Refused" in rep_status else 0],
            "status": ["GREEN"],
        })
        df_db = pd.concat([df_db, new_row], ignore_index=True)

      # Recalculate status with smart rules
      idx = df_db[df_db["phone_hash"] == p_hash].index[0]
      t = df_db.loc[idx, "total_orders"]
      r = df_db.loc[idx, "rto_count"]
      ratio = r / t if t > 0 else 0

      # Low order safety guard: if total orders < 2 and there's an RTO, keep it YELLOW instead of harsh RED
      if t < 2 and r > 0:
        df_db.loc[idx, "status"] = "YELLOW"
      elif ratio >= 0.5:
        df_db.loc[idx, "status"] = "RED"
      elif ratio > 0.2:
        df_db.loc[idx, "status"] = "YELLOW"
      else:
        df_db.loc[idx, "status"] = "GREEN"

      save_db(df_db)
      st.success(
          "Success! Network database securely updated with encrypted hash"
          " and smart risk calculation."
      )
    else:
      st.error("Please enter a phone number.")

with tabs[2]:
  st.subheader("Developer & Shopify API Integration")
  st.markdown(
      "Brands can programmatically query this risk engine during checkout"
      " via API:"
  )
  st.code(
      """
    import requests

    url = "https://your-replit-url.replit.dev/api/v1/lookup"
    headers = {"X-Brand-API-Key": "khaadi-secret-key-123"}
    payload = {"phone_number": "03001234567", "payment_method": "COD"}

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    """,
      language="python",
  )
