import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "user" not in st.session_state:
    st.session_state.user = None


def sign_up(email: str, password: str) -> str:
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if res.user:
            supabase.table("profiles").insert({
                "id": res.user.id,
                "email": email,
                "paid": False,
                "role": "user"
            }).execute()

            return "Account created. Please log in."

        return "Sign up failed."

    except Exception as e:
        return str(e)


def sign_in(email: str, password: str) -> str:
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not res.user:
            return "Invalid credentials."

        profile = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", res.user.id)
            .single()
            .execute()
        )

        st.session_state.user = {
            "id": res.user.id,
            "email": email,
            "paid": profile.data["paid"],
            "admin": profile.data["role"] == "admin"
        }

        return "Login successful."

    except Exception as e:
        return str(e)


def user_logged_in():
    return st.session_state.user
