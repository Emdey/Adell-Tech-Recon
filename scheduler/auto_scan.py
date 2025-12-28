import schedule
import time
from recon_engine.js_scanner import discover_js_files, fetch_js_source, beautify_js_source
from recon_engine.secret_scanner import find_secrets
from recon_engine.endpoint_scanner import find_endpoints
from recon_engine.diff_manager import load_previous_report, save_report, get_delta
from config import EMAIL_NOTIFICATIONS
from notifications.email_notify import send_email  # We'll create this next

TARGET_DOMAINS = ["example.com", "another.com"]  # Add your domains here

def scan_domain(domain: str):
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

    if EMAIL_NOTIFICATIONS and (delta["new_endpoints"] or delta["new_secrets"]):
        body = f"Daily Scan Report for {domain}\n\n"
        if delta["new_endpoints"]:
            body += "New Endpoints:\n" + "\n".join(delta["new_endpoints"]) + "\n\n"
        if delta["new_secrets"]:
            body += "New Secrets:\n" + "\n".join([f'{s["type"]}: {s["value"]}' for s in delta["new_secrets"]])
        send_email(f"New Security Findings for {domain}", body)

def run_scheduler():
    for domain in TARGET_DOMAINS:
        schedule.every().day.at("09:00").do(scan_domain, domain=domain)  # adjust time

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
