import streamlit as st

# Supabase secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Recon engine settings
HEADERS = {"User-Agent": "ADELL-TECH-Recon/1.0"}
TIMEOUT = 10

# Directory for JSON reports (used by diff_manager)
REPORT_DIR = "previous_reports"


