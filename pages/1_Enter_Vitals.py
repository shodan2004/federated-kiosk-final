import streamlit as st
import pandas as pd
import joblib
from supabase import create_client
from datetime import datetime, timezone
from fpdf import FPDF
import random
import os

# --- Supabase config ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- Load ML Model for Medication Prediction ---
@st.cache_resource
def load_model():
    model = joblib.load("med_model.pkl")
    labelizer = joblib.load("med_labelizer.pkl")
    return model, labelizer

model, labelizer = load_model()
def predict_medications(data):
    X = pd.DataFrame([{
        "height": data["height"],
        "weight": data["weight"],
        "temperature": data["temperature"],
        "blood_pressure": data["blood_pressure"],
        "blood_oxygen": data["blood_oxygen"],
        "body_fat_percent": data["body_fat_percent"],
        "bmi": data["bmi"],
        "label": data["label"]
    }])
    preds = model.predict(X)
    meds = labelizer.inverse_transform(preds)
    return meds[0] if meds else []

def is_critical(v):
    return (
        v["temperature"] > 39 or
        v["blood_pressure"] > 160 or
        v["blood_oxygen"] < 90
    )

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def generate_pdf_report(data, meds):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Patient Vitals Report", ln=True, align="C")
    for key, val in data.items():
        pdf.cell(200, 10, txt=f"{key}: {val}", ln=True)
    pdf.cell(200, 10, txt=f"BMI Category: {bmi_category(data['bmi'])}", ln=True)
    pdf.cell(200, 10, txt=f"Medications: {', '.join(meds)}", ln=True)
    filename = f"patient_report_{random.randint(1000, 9999)}.pdf"
    pdf.output(filename)
    return filename

# --- Vitals entry form ---
st.title("📥 Enter Patient Vitals")
with st.form("vitals_form"):
    name = st.text_input("Patient Name")
    height = st.number_input("Height (cm)", 50.0, 250.0)
    weight = st.number_input("Weight (kg)", 10.0, 300.0)
    temperature = st.number_input("Temperature (°C)", 30.0, 45.0)
    blood_pressure = st.number_input("Blood Pressure (Sys)", 50.0, 200.0)
    blood_oxygen = st.number_input("Oxygen Level (%)", 50.0, 100.0)
    body_fat = st.number_input("Body Fat %", 5.0, 60.0)
    label = st.selectbox("Health Label", [0, 1], format_func=lambda x: "Healthy" if x == 0 else "At Risk")
    submit = st.form_submit_button("Submit")

if submit:
    bmi = round(weight / ((height / 100) ** 2), 2)
    timestamp = datetime.now(timezone.utc).isoformat()

    data = {
        "name": name,
        "height": height,
        "weight": weight,
        "temperature": temperature,
        "blood_pressure": blood_pressure,
        "blood_oxygen": blood_oxygen,
        "body_fat_percent": body_fat,
        "bmi": bmi,
        "label": label,
        "timestamp": timestamp
    }

    res = supabase.table("user_data").insert(data).execute()

    if res.data:
        st.success(f"✅ Data saved! BMI: {bmi} ({bmi_category(bmi)})")

        meds = predict_medications(data)
        st.markdown(f"### 💊 Predicted Medications: {', '.join(meds)}")

        if is_critical(data):
            st.error("🚨 Critical vitals detected!")

        pdf_file = generate_pdf_report(data, meds)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download PDF Report", f, file_name=pdf_file)
        os.remove(pdf_file)
    else:
        st.error("❌ Failed to insert data")

# --- Kiosk Monitoring Dashboard ---
st.title("📊 Kiosk Health Dashboard")
data_resp = supabase.table("user_data").select("*").order("timestamp", desc=True).limit(100).execute()

if data_resp.data:
    df = pd.DataFrame(data_resp.data)
    st.line_chart(df.set_index("timestamp")["bmi"], use_container_width=True)
    st.area_chart(df.set_index("timestamp")["temperature"], use_container_width=True)

    kiosk_status = "🟢 Healthy"
    if any(df["label"] == 1):
        kiosk_status = "🔴 Attention Needed"
    st.markdown(f"### 📍 Kiosk Status: {kiosk_status}")

    st.dataframe(df)
else:
    st.info("No vitals data found.")
