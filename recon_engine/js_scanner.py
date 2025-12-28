import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import jsbeautifier
from config import HEADERS, TIMEOUT


def is_valid_js(url: str) -> bool:
    """Check if the URL points to a JS file."""
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and url.endswith(".js")


def discover_js_files(target_url: str) -> list[str]:
    """
    Discover all JS files linked in a webpage.
    Returns a sorted list of valid JS URLs.
    """
    discovered = set()
    try:
        response = requests.get(target_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup.find_all("script"):
            src = script.get("src")
            if src:
                absolute_url = urljoin(target_url, src)
                if is_valid_js(absolute_url):
                    discovered.add(absolute_url)
    except requests.RequestException:
        # Could log this in production
        pass
    return sorted(discovered)


def fetch_js_source(js_url: str) -> str | None:
    """Fetch JS source code from a URL."""
    try:
        response = requests.get(js_url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None


def beautify_js_source(js_code: str) -> str:
    """Beautify JS source code for easier parsing."""
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    return jsbeautifier.beautify(js_code, opts)
