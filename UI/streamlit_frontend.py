import streamlit as st
import json
from recon_engine.js_scanner import discover_js_files, fetch_js_source, beautify_js_source
from recon_engine.secret_scanner import find_secrets
from recon_engine.endpoint_scanner import find_endpoints
from recon_engine.diff_manager import load_previous_report, save_report, get_delta
from auth.firebase_auth import sign_in, sign_up, user_logged_in
from payments.stripe_pay import create_checkout_session

# ---------------------------
# Page config and theme
# ---------------------------
st.set_page_config(page_title="ADELL TECH Recon", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0d1b2a, #1b263b); color: #e0f7fa;}
.glass-card {backdrop-filter: blur(10px); background-color: rgba(0,77,102,0.4);
border-radius: 15px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37);
border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;}
div.stButton > button {background-color: #006064; color: white; border-radius: 10px; padding: 0.5em 1.5em;}
div.stButton > button:hover { background-color: #0097a7; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>ADELL TECH - One-Click Recon</h1>", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Authentication + Payment
# ---------------------------
st.sidebar.title("User Access")
if not user_logged_in():
    choice = st.sidebar.radio("Action", ["Login", "Sign Up"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if choice == "Sign Up" and st.sidebar.button("Sign Up"):
        msg = sign_up(email, password)
        st.sidebar.success(msg)
    elif choice == "Login" and st.sidebar.button("Login"):
        msg = sign_in(email, password)
        st.sidebar.success(msg)
else:
    st.sidebar.success(f"Logged in as {user_logged_in()['email']}")
    # Show payment button if subscription not active
    if not user_logged_in().get("paid", False):
        if st.sidebar.button("Subscribe / Pay"):
            url = create_checkout_session("price_xxx", user_logged_in()["email"],
                                          "https://example.com/success",
                                          "https://example.com/cancel")
            st.sidebar.markdown(f"[Pay here]({url})")

# ---------------------------
# Main scan container
# ---------------------------
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    domain = st.text_input("Enter target domain (example.com):")
    start_scan = st.button("Start Scan")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Scan logic only if logged in and paid
# ---------------------------
user = user_logged_in()
if start_scan and domain:
    if not user or not user.get("paid", False):
        st.warning("You must be logged in and have an active subscription to start scans.")
    else:
        with st.spinner(f"Scanning {domain} ..."):
            report = {"secrets": [], "endpoints": []}
            js_files = discover_js_files(f"https://{domain}")
            for js in js_files:
                src = fetch_js_source(js)
                if src:
                    beautified = beautify_js_source(src)
                    report["secrets"].extend(find_secrets(beautified))
                    report["endpoints"].extend(find_endpoints(beautified))

            previous = load_previous_report(domain)
            delta = get_delta(report, previous)
            save_report(domain, report)

        # ---------------------------
        # Display results
        # ---------------------------
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Scan Complete ✅")
        st.markdown(f"**Domain:** {domain}")

        st.subheader("New Endpoints")
        if delta["new_endpoints"]:
            for ep in delta["new_endpoints"]:
                st.write(ep)
        else:
            st.write("No new endpoints detected.")

        st.subheader("New Secrets")
        if delta["new_secrets"]:
            for s in delta["new_secrets"]:
                st.write(f"{s['type']}: {s['value']}")
        else:
            st.write("No new secrets detected.")

        st.download_button(
            "Download Full JSON Report",
            data=json.dumps(report, indent=2),
            file_name=f"report_{domain.replace('.', '_')}.json",
            mime="application/json"
        )
        st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------
