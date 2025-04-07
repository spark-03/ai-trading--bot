import streamlit as st
import pandas as pd
import requests

SUPABASE_URL = "https://nrdiwysldrartenliqjb.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2eWdqaW5jcGF5aHhvbGN3bWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5Nzg2MDEsImV4cCI6MjA1OTU1NDYwMX0.q5n3qYkSEb9deJ61FYiY2WEg1WybVpexkzMvvtEr9-Y"  # Replace with your key

st.set_page_config(page_title="AI Trading Bot - Dashboard", layout="wide")

st.title("📊 AI Trading Bot Dashboard")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}"
}

def fetch_data(status):
    url = f"{SUPABASE_URL}/rest/v1/paper_trades?status=eq.{status}&select=*"
    response = requests.get(url, headers=headers)
    return pd.DataFrame(response.json())

tab1, tab2 = st.tabs(["📄 Paper Trades", "💰 Real Trades"])

with tab1:
    df = fetch_data("paper")
    st.dataframe(df.sort_values("entry_time", ascending=False))

with tab2:
    df = fetch_data("real")
    st.dataframe(df.sort_values("entry_time", ascending=False))

st.info("✅ This dashboard shows trades done by the AI trading bot.")
