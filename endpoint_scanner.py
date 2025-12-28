import re
from config import ENDPOINT_PATTERN

def find_endpoints(js_code: str) -> list[str]:
    return list(set(re.findall(ENDPOINT_PATTERN, js_code, re.VERBOSE)))
