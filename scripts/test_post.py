import os
import logging
import requests
from dotenv import load_dotenv

# Load .env explicitly from project root
dotenv_path = "/home/angels/rmr-bot/.env"
if not load_dotenv(dotenv_path=dotenv_path):
    logging.error(f"Failed to load .env from {dotenv_path}")
    exit(1)

# Read environment variables
PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_TOKEN")
IMAGE_PATH = "/home/angels/rmr-bot/output/images/quote_20260303_200040.png"
CAPTION = "Test post from bot"

# Verify env variables
if not PAGE_ID:
    logging.error("FB_PAGE_ID not set or empty in .env")
    exit(1)
if not TOKEN:
    logging.error("FB_PAGE_TOKEN not set or empty in .env")
    exit(1)

logging.basicConfig(level=logging.INFO)
logging.info(f"Using Page ID: {PAGE_ID}")
logging.info(f"Using Token (first 10 chars): {TOKEN[:10]}...")

# Check image file
if not os.path.isfile(IMAGE_PATH):
    logging.error(f"Image file does not exist: {IMAGE_PATH}")
    exit(1)

# Prepare request
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
files = {"source": open(IMAGE_PATH, "rb")}
data = {"caption": CAPTION, "access_token": TOKEN}

try:
    response = requests.post(url, files=files, data=data)
    # Print status and full response for debugging
    logging.info(f"HTTP Status: {response.status_code}")
    logging.info(f"Response Body: {response.text}")

    response.raise_for_status()
    logging.info("Photo posted successfully: %s", response.json().get("id"))

except requests.exceptions.HTTPError as e:
    logging.error("Facebook API returned an error")
    logging.error(response.text)
    raise e

finally:
    files["source"].close()