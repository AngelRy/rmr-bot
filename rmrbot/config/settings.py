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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FB_API_BASE = "https://graph.facebook.com/v19.0"

LOGO_PATH = os.path.join(BASE_DIR, "assets", "rmrtrex.png")
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "DejaVuSans.ttf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output/images")



FB_MAX_RETRIES = 3
FB_INITIAL_BACKOFF = 1
FB_REQUEST_TIMEOUT = 15