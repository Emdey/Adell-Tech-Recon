import json
import os
from config import REPORT_DIR
from typing import Dict, Any
# Ensure report directory exists
os.makedirs(REPORT_DIR, exist_ok=True)


def load_previous_report(domain: str) -> Dict[str, Any]:
    """
    Load the previous JSON report for a given domain.

    Args:
        domain (str): Target domain (example.com)

    Returns:
        dict: Previous report containing 'secrets' and 'endpoints'.
              Returns empty lists if no report exists.
    """
    path = os.path.join(REPORT_DIR, f"report_{domain.replace('.', '_')}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"secrets": [], "endpoints": []}


def save_report(domain: str, report: Dict[str, Any]) -> None:
    """
    Save the JSON report for a domain.

    Args:
        domain (str): Target domain (example.com)
        report (dict): Report dictionary containing secrets and endpoints
    """
    path = os.path.join(REPORT_DIR, f"report_{domain.replace('.', '_')}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)


def get_delta(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare current and previous reports and return new findings.

    Args:
        current (dict): Current scan report
        previous (dict): Previous scan report

    Returns:
        dict: Delta report containing:
              - 'new_secrets': List of newly discovered secrets
              - 'new_endpoints': List of newly discovered endpoints
    """
    new_secrets = [s for s in current.get("secrets", []) 
                   if s not in previous.get("secrets", [])]

    new_endpoints = [e for e in current.get("endpoints", []) 
                     if e not in previous.get("endpoints", [])]

    return {
        "new_secrets": new_secrets,
        "new_endpoints": new_endpoints
    }
