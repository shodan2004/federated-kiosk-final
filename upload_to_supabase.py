import pandas as pd
from supabase import create_client, Client
import streamlit as st
from datetime import datetime

# Load Supabase credentials from secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load training log CSV
df = pd.read_csv("training_logs.csv")

# Ensure timestamp column is parsed and formatted correctly
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"]).apply(lambda x: x.isoformat())
else:
    df["timestamp"] = datetime.utcnow().isoformat()

# Convert to list of dictionaries
records = df.to_dict(orient="records")

# Upload each record to Supabase
for record in records:
    response = supabase.table("training_logs").insert(record).execute()
    print("Inserted:", response)
