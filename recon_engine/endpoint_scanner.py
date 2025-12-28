import re
from config import ENDPOINT_PATTERN

def find_endpoints(js_code: str) -> list[str]:
    """
    Scan JavaScript code for endpoints (URLs or relative paths).

    Args:
        js_code (str): JavaScript source code.

    Returns:
        list[str]: Unique endpoints found in the JS code.
    """
    if not js_code:
        return []
    return list(set(re.findall(ENDPOINT_PATTERN, js_code, re.VERBOSE)))
