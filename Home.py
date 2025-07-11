# File: Home.py

import streamlit as st

st.set_page_config(page_title="🏥 Federated Healthcare Kiosk", layout="wide")

st.title("🏥 Federated Healthcare Kiosk")

st.markdown("""
Welcome to the **Federated Healthcare Kiosk** dashboard.

---

📥 **Submit new patient vitals**  
Enter real-time health data like height, weight, temperature, BP, and more.

📊 **View training metrics**  
Monitor federated learning performance across all kiosk clients.

---

This platform connects patient-facing data entry with live AI model training and monitoring using federated learning principles.
""")
