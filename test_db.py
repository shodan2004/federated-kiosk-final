import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

SUPABASE_DB_URL = st.secrets["SUPABASE_DB_URL"]
engine = create_engine(SUPABASE_DB_URL)

try:
    df = pd.read_sql("SELECT * FROM training_logs LIMIT 5", engine)
    st.write("✅ Connection Successful!")
    st.dataframe(df)
except Exception as e:
    st.error("❌ Failed to connect to Supabase DB")
    st.exception(e)

