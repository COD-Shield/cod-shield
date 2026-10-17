import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

def send_customer_email(recipient_email, subject, body_text):
    try:
        # یہ Streamlit Secrets سے آپ کا جی میل اور ایپ پاسورڈ اٹھائے گا
        sender_email = st.secrets["email"]["sender"]
        app_password = st.secrets["email"]["password"]
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body_text, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"ای میل بھیجنے میں خرابی: {e}")
        return False
