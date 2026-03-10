import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
APP_TOKEN = os.getenv("FB_APP_TOKEN")  # app_id|app_secret

if not PAGE_TOKEN or not APP_TOKEN:
    raise RuntimeError("Missing FB_PAGE_TOKEN or FB_APP_TOKEN")

url = "https://graph.facebook.com/debug_token"

params = {
    "input_token": PAGE_TOKEN,
    "access_token": APP_TOKEN
}

r = requests.get(url, params=params)
r.raise_for_status()

print(r.json())
