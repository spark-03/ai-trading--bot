# dashboard/dashboard.py

import streamlit as st
import pandas as pd
from backend.supabase_client import supabase

st.set_page_config(layout="wide", page_title="Trading Bot Dashboard")

st.title("📊 AI Trading Bot Dashboard")

tab1, tab2 = st.tabs(["🔁 Trade Logs", "📈 Strategy Performance"])

with tab1:
    st.subheader("All Trades")
    response = supabase.table("trade_logs").select("*").order("timestamp_entry", desc=True).limit(100).execute()
    trades = pd.DataFrame(response.data)
    st.dataframe(trades)

with tab2:
    st.subheader("Daily Performance")
    perf = supabase.table("performance_metrics").select("*").order("date", desc=True).limit(30).execute()
    perf_df = pd.DataFrame(perf.data)
    st.dataframe(perf_df)
