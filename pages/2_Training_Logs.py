# File: pages/2_Training_Logs.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt
import time

# Polling frequency (in seconds)
POLL_INTERVAL = 10

# URL param for auto-refresh
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh Charts", value=False)

if auto_refresh:
    # Sleep for a short time then rerun the app
    time.sleep(POLL_INTERVAL)
    st.experimental_rerun()

SUPABASE_DB_URL = st.secrets["SUPABASE_DB_URL"]
engine = create_engine(SUPABASE_DB_URL)

st.set_page_config(page_title="Training Logs", layout="wide")
st.title("📊 Federated Training Dashboard")

# Load data
@st.cache_data(ttl=10)
def load_data():
    query = "SELECT * FROM training_logs ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Failed to load training logs from Supabase.")
    st.exception(e)
    st.stop()


# Filters
kiosks = df["kiosk_id"].unique().tolist()
selected_kiosks = st.multiselect("Select Kiosk(s):", kiosks, default=kiosks)

rounds = sorted(df["round"].unique())
if len(rounds) > 1 and min(rounds) < max(rounds):
    selected_rounds = st.slider("Filter by Round Range:", min_value=min(rounds), max_value=max(rounds), value=(min(rounds), max(rounds)))
else:
    st.warning("Not enough round data to display range slider.")
    selected_rounds = (min(rounds) if rounds else 0, max(rounds) if rounds else 0)

# Filter data based on selection
filtered_df = df[
    (df["kiosk_id"].isin(selected_kiosks)) &
    (df["round"] >= selected_rounds[0]) &
    (df["round"] <= selected_rounds[1])
]

# Charts
if not filtered_df.empty:
    acc_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x="round:Q",
        y="val_accuracy:Q",
        color="kiosk_id:N",
        tooltip=["kiosk_id", "round", "val_accuracy"]
    ).properties(title="Validation Accuracy per Round")
    
    loss_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x="round:Q",
        y="val_loss:Q",
        color="kiosk_id:N",
        tooltip=["kiosk_id", "round", "val_loss"]
    ).properties(title="Validation Loss per Round")

    st.altair_chart(acc_chart, use_container_width=True)
    st.altair_chart(loss_chart, use_container_width=True)

    st.markdown("### 📋 Raw Training Logs")
    st.dataframe(filtered_df)

    # Accuracy alert
    recent = filtered_df[filtered_df["round"] == filtered_df["round"].max()]
    if recent["val_accuracy"].mean() < 0.75:
        st.error("⚠️ Model validation accuracy is below 75%!")
else:
    st.info("No logs match the selected filters.")
