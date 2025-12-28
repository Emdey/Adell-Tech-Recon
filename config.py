import os

# ---------------------------
# General Recon Settings
# ---------------------------
HEADERS = {"User-Agent": "ADELL-TECH-Recon/1.0"}
TIMEOUT = 10

REPORT_DIR = "previous_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------------------
# Secret patterns
# ---------------------------
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API Key": r"(?i)(api_key|apikey|secret|token)\s*[:=]\s*['\"][0-9a-zA-Z_-]{16,}['\"]",
}

# ---------------------------
# Supabase config (do NOT import streamlit here!)
# ---------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
