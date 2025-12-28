import streamlit as st
import json


# Recon engine
from recon_engine.js_scanner import discover_js_files, fetch_js_source, beautify_js_source
from recon_engine.secret_scanner import find_secrets
from recon_engine.endpoint_scanner import find_endpoints
from recon_engine.diff_manager import load_previous_report, save_report, get_delta

# Auth (Supabase ONLY)
from auth.supabase_auth import sign_up, sign_in, user_logged_in

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(page_title="ADELL TECH Recon", layout="wide")

# ---------------------------
# Glassmorphism CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0d1b2a, #1b263b);
    color: #e0f7fa;
}
.glass-card {
    backdrop-filter: blur(10px);
    background-color: rgba(0,77,102,0.4);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.37);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}
div.stButton > button {
    background-color: #006064;
    color: white;
    border-radius: 10px;
    padding: 0.5em 1.5em;
}
div.stButton > button:hover {
    background-color: #0097a7;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>ADELL TECH – One-Click Recon</h1>",
    unsafe_allow_html=True
)

# ---------------------------
# Authentication Sidebar
# ---------------------------
with st.sidebar:
    st.header("Account")

    if not user_logged_in():
        choice = st.radio("Action", ["Login", "Sign Up"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button(choice):
            if choice == "Login":
                msg = sign_in(email, password)
            else:
                msg = sign_up(email, password)
            st.success(msg)

    else:
        st.success(f"Logged in as {st.session_state.user['email']}")

        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

        if not st.session_state.user.get("paid", False):
            st.warning("Account not activated yet.")
            st.info(
                "This is a beta system. "
                "Your account must be manually approved by the admin."
            )

# ---------------------------
# Scan Section (Activated Users)
# ---------------------------
if user_logged_in() and st.session_state.user.get("paid", False):

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        domain = st.text_input("Enter target domain (example.com)")
        start_scan = st.button("Start Scan")
        st.markdown('</div>', unsafe_allow_html=True)

    if start_scan and domain:
        with st.spinner(f"Scanning {domain} …"):
            report = {"secrets": [], "endpoints": []}

            js_files = discover_js_files(f"https://{domain}")
            for js in js_files:
                src = fetch_js_source(js)
                if not src:
                    continue

                beautified = beautify_js_source(src)
                report["secrets"].extend(find_secrets(beautified))
                report["endpoints"].extend(find_endpoints(beautified))

            previous = load_previous_report(domain)
            delta = get_delta(report, previous)
            save_report(domain, report)

        # ---------------------------
        # Results
        # ---------------------------
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Scan Complete")

        st.markdown(f"**Domain:** {domain}")

        st.subheader("New Endpoints")
        if delta["new_endpoints"]:
            for ep in delta["new_endpoints"]:
                st.code(ep)
        else:
            st.write("No new endpoints detected.")

        st.subheader("New Secrets")
        if delta["new_secrets"]:
            for s in delta["new_secrets"]:
                st.code(f"{s['type']}: {s['value']}")
        else:
            st.write("No new secrets detected.")

        st.download_button(
            "Download JSON Report",
            json.dumps(report, indent=2),
            file_name=f"report_{domain.replace('.', '_')}.json",
            mime="application/json",
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Admin Controls
# ---------------------------
if user_logged_in() and st.session_state.user.get("admin", False):
    if st.button("Run Daily Scan Now"):
        from scheduler.auto_scan import scan_domain

        with st.spinner("Running scheduled scans…"):
            for d in ["example.com", "another.com"]:
                scan_domain(d)

        st.success("Daily scans completed.")
