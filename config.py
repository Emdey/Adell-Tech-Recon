import os
import streamlit as st

# Supabase credentials: Cloud secrets first, fallback to local env
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

# HTTP headers and timeout
HEADERS = {"User-Agent": "ADELL-TECH-Recon/1.0"}
TIMEOUT = 10
# Report directory
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)
