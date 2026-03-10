import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=(5, 10),  # (connect_timeout, read_timeout)
        )
        r.raise_for_status()
        return r.text

    except requests.Timeout:
        print(f"[TIMEOUT] {url}")
        return None

    except requests.RequestException as e:
        print(f"[WARN] Failed to fetch {url}: {e}")
        return None