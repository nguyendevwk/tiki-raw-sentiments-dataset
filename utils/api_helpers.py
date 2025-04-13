import time
import requests

HEADERS = {
    # headers như cũ
}

session = requests.Session()
session.headers.update(HEADERS)

def get_with_retry(url, params=None, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            response = session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
