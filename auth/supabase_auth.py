import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ensure session state
if "user" not in st.session_state:
    st.session_state.user = None

def sign_up(email: str, password: str) -> str:
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if res.user:
            st.session_state.user = {
                "email": email,
                "paid": True,   # 🔓 bypass payment
                "admin": False
            }
            return "Sign-up successful. You are logged in."
        return "Sign-up failed."
    except Exception as e:
        return str(e)

def sign_in(email: str, password: str) -> str:
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if res.user:
            st.session_state.user = {
                "email": email,
                "paid": True,   # 🔓 bypass payment
                "admin": False
            }
            return "Login successful."
        return "Login failed."
    except Exception as e:
        return str(e)

def user_logged_in():
    return st.session_state.user
