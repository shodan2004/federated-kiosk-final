# 🏥 Federated Healthcare Kiosk

A real-time federated learning system that connects patient data entry with decentralized AI model training and real-time dashboard monitoring.

---

## 🚀 Overview

This project simulates a healthcare kiosk environment where multiple decentralized clients (kiosks) train on local health data using Federated Learning (FL) and sync model updates with a central server. The system:

- Captures patient vitals
- Predicts medications using ML
- Monitors kiosk health and federated metrics
- Detects critical patients and issues alerts
- Stores and visualizes all data via Supabase + Streamlit

---

## 📁 Project Structure

federated-kiosk-final/
├── Home.py # Clean, interactive landing page
├── streamlit_app.py # (Deprecated) legacy entrypoint
├── client.py # Flower client for federated learning
├── server.py # Flower server to coordinate FL
├── med_model.pkl # Trained medication prediction model
├── med_labelizer.pkl # Label encoder for medication classes
├── synthetic_vitals_100k.csv # Synthetic dataset for training
├── train_med_model.py # Script to train medication model
├── upload_to_supabase.py # Upload synthetic data to Supabase
├── test_insert.py # Insert one training log into Supabase
├── test_insert_user_data.py # Script to test vitals insertion
├── test_insert_training_logs.py # Script to test training logs insertion
├── requirements.txt # Python dependencies
├── pages/
│ ├── 1_Enter_Vitals.py # Vitals entry + PDF + prediction + alerts
│ └── 2_Training_Logs.py # Federated learning dashboard
└── venv/ # Python virtual environment



---

## ⚙️ Features

### 🧑‍⚕️ Vitals Entry (`pages/1_Enter_Vitals.py`)
- Collect vitals: height, weight, BP, oxygen, fat %, temp, health label
- Predict medications using ML (`med_model.pkl`)
- Detects and alerts on critical conditions
- Calculates and displays BMI category
- Saves data into Supabase table: `user_data`
- Generates PDF reports with data in table format

### 📊 Training Logs (`pages/2_Training_Logs.py`)
- Visualize accuracy, loss, validation trends over time
- Show kiosk-wise performance
- Health indicators (green/yellow/red)
- Pulls data from `training_logs` table in Supabase

### 🧠 ML Model (`train_med_model.py`)
- Trains a medication recommender model from `synthetic_vitals_100k.csv`
- Outputs:
  - `med_model.pkl`: Scikit-learn classifier
  - `med_labelizer.pkl`: LabelEncoder for medications

### 🌸 Federated Learning
- Flower-based server (`server.py`) and client (`client.py`)
- Clients train local CNN models on partitioned MNIST
- Logs metrics to Supabase after each round

### ☁️ Supabase Integration
- Supabase PostgreSQL used for:
  - `user_data`: vitals, predictions, alerts
  - `training_logs`: FL metrics
- Uses `sqlalchemy` or Supabase Python client

---

## 🛠️ Setup Instructions

### 1. Clone and Setup

```bash
git clone https://github.com/shodan2004/federated-kiosk-final.git
cd federated-kiosk-final
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

##2. Train Medication Model
python train_med_model.py

##3. Run Streamlit App
streamlit run Home.py

##Federated Learning (Terminal 1 = server, Terminal 2+ = clients)
python server.py
python client.py --client_id 1
python client.py --client_id 2

##🧪 Testing Tools

| Script                         | Purpose                                 |
| ------------------------------ | --------------------------------------- |
| `test_insert.py`               | Inserts one FL log to `training_logs`   |
| `upload_to_supabase.py`        | Uploads synthetic vitals to `user_data` |
| `test_insert_user_data.py`     | Tests vitals Supabase insertion         |
| `test_insert_training_logs.py` | Tests FL training log insertion         |


###Supabase Schema
##Table: user_data

| Column             | Type        |
| ------------------ | ----------- |
| name               | text        |
| height             | float       |
| weight             | float       |
| temperature        | float       |
| blood\_pressure    | float       |
| blood\_oxygen      | float       |
| body\_fat\_percent | float       |
| bmi                | float       |
| label              | integer     |
| medications        | text        |
| timestamp          | timestamptz |

##Table: training_logs
| Column        | Type        |
| ------------- | ----------- |
| round         | int         |
| client\_id    | int         |
| loss          | float       |
| val\_loss     | float       |
| accuracy      | float       |
| val\_accuracy | float       |
| kiosk\_id     | text        |
| timestamp     | timestamptz |

##Dependencies
pip install -r requirements.txt

Includes:

streamlit

pandas

sqlalchemy

supabase

joblib

flower

scikit-learn

fpdf

psycopg2-binary

##📈 Future Enhancements
Add login with Supabase Auth

Deploy Streamlit app on secure HTTPS

Add model versioning for FL clients

Integrate WebSocket-based real-time updates

Create separate dashboards for each kiosk

Add analytics on patient trends


##👨‍💻 Author
Shodhan Vemulapalli
GitHub: @shodan2004
Streamlit App: https://federated-kiosk.streamlit.app
