import os

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

DB_NAME = "quotes.db"
POSTS_PER_DAY = 3

RUNNING_HASHTAGS = [
    "#running",
    "#runners",
    "#runnerslife",
    "#runningmotivation",
    "#runinspiration",
    "#instarunners",
    "#marathon",
    "#trailrunning",
    "#runhappy",
    "#runday",
]


FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
FB_API_BASE = "https://graph.facebook.com/v19.0"

IMAGE_OUTPUT_DIR = "output/images"
LOGO_PATH = "assets/rmrtrex.png"
FONT_PATH = "assets/fonts/DejaVuSans.ttf"


FB_MAX_RETRIES = 3
FB_INITIAL_BACKOFF = 1
FB_REQUEST_TIMEOUT = 15