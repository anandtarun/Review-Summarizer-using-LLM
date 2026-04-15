import time

# Standard headers to prevent immediate blocking by e-commerce sites
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def safe_api_call(func, *args, retries=3):
    for i in range(retries):
        try:
            return func(*args)
        except Exception:
            time.sleep(2 ** i)
    return None