from dotenv import load_dotenv
load_dotenv(override=True)

import os
import sys
import logging


from rmrbot.publisher.facebook_publisher import post_photo_to_page
from rmrbot.generator.quote_parser import parse_quote
from rmrbot.generator.image_generator import generate_image
from rmrbot.generator.post_text_generator import generate_caption
from rmrbot.database.models import get_quote_for_posting, mark_as_posted
from rmrbot.logging_config import setup_logging
setup_logging()

logging.basicConfig(level=logging.INFO)

def validate_startup():
    required_vars = ["FB_PAGE_ID", "FB_PAGE_TOKEN", "FB_APP_TOKEN"]

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"FATAL: Missing required environment variable: {var}")
            sys.exit(1)

    page_id = os.getenv("FB_PAGE_ID").strip()
    token = os.getenv("FB_PAGE_TOKEN").strip()

    # Basic structural checks
    if not page_id.isdigit():
        print("FATAL: FB_PAGE_ID must be numeric.")
        sys.exit(1)

    if not token.startswith("EAA"):
        print("FATAL: FB_PAGE_TOKEN does not look like a valid Meta access token.")
        sys.exit(1)

    if len(token) < 100:
        print("FATAL: FB_PAGE_TOKEN is suspiciously short.")
        sys.exit(1)

    print("Startup validation passed.")



import requests


def verify_token_with_meta():
    page_token = os.getenv("FB_PAGE_TOKEN").strip()
    

    app_access_token = os.getenv("FB_APP_TOKEN").strip()

    url = "https://graph.facebook.com/debug_token"

    params = {
        "input_token": page_token,
        "access_token": app_access_token,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("FATAL: Failed to verify token with Meta.")
        print(response.text)
        raise SystemExit(1)

    data = response.json()["data"]

    if not data.get("is_valid"):
        print("FATAL: Page token is not valid.")
        raise SystemExit(1)

    required_scopes = {
        "pages_manage_posts",
        "pages_read_engagement",
        "pages_show_list",
    }

    token_scopes = set(data.get("scopes", []))

    missing = required_scopes - token_scopes
    if missing:
        print(f"FATAL: Token missing required scopes: {missing}")
        raise SystemExit(1)

    print("Token verification passed.")






def main():
    validate_startup()
    verify_token_with_meta()

    row = get_quote_for_posting()

    if not row:
        print("No eligible quotes available (4-week cooldown active).")
        return

    quote_id, raw_quote = row

    parsed = parse_quote(raw_quote)
    quote = parsed["quote"]
    author = parsed["author"]

    image_path = generate_image(quote, author)
    caption = generate_caption(quote, author)

    print("Posting to Page...")
    res = post_photo_to_page(image_path, caption)
    print("Posted:", res)

    # Mark as posted only after successful publish
    mark_as_posted(quote_id)

    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Fatal error in posting pipeline")
        sys.exit(1)
