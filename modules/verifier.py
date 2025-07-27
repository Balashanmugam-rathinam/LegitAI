import requests

def validate_links(url_list):
    validated = []
    for url in url_list:
        try:
            r = requests.head(url, allow_redirects=True, timeout=5)
            validated.append((url, r.status_code < 400))
        except Exception:
            validated.append((url, False))
    return validated
