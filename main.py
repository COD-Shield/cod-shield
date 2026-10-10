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
    "A secure cloud network for e-commerce brands to prevent Cash on "
    "Delivery (COD) RTO and fake order losses."
)

# Database File Path (Persistent Storage)
DB_FILE = "cod_database.csv"
