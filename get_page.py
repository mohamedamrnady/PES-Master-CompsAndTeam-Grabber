import requests
requests.adapters.DEFAULT_RETRIES = 100


def get_page(url):
    r = requests.get(url, headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})
    return r
