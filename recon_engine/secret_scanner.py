import re
from config import SECRET_PATTERNS

def find_secrets(js_code: str) -> list[dict]:
    """
    Scan JS code for potential secrets.

    Args:
        js_code (str): JavaScript source code.

    Returns:
        list[dict]: List of findings, each a dict with 'type' and 'value'.
    """
    findings = []
    for name, pattern in SECRET_PATTERNS.items():
        matches = re.findall(pattern, js_code)
        for match in matches:
            findings.append({"type": name, "value": match})
    return findings
