import requests
from time import sleep
requests.adapters.DEFAULT_RETRIES = 100
FAILED_ATTEMPTS = 0


def get_page(url):
    global FAILED_ATTEMPTS
    r = requests.get(url, headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})
    if r.status_code != 200:
        print(f"Failed to get page {url}, status code: {r.status_code}")
        FAILED_ATTEMPTS += 1
        if FAILED_ATTEMPTS < 5:
            sleep(10)
            return get_page(url)
        else:
            print(f"Failed to get page {url} after 5 attempts, skipping.")
            return None
    return r
