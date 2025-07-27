import re
import requests

def extract_and_validate_links(text):
    url_pattern = r"https?://[^\s)]+"
    urls = re.findall(url_pattern, text)
    validated = []

    for url in urls:
        try:
            response = requests.head(url, timeout=5)
            valid = response.status_code == 200
        except Exception:
            valid = False
        validated.append((url, valid))
    
    return validated
