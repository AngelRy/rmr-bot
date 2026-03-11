import os
import requests
import logging

logger = logging.getLogger(__name__)

def post_photo_to_page(image_path: str, caption: str):
    """
    Post an image with caption to the Facebook Page using the system user token.
    Returns JSON on success, None on failure.
    """
    page_id = os.getenv("FB_PAGE_ID")
    page_token = os.getenv("FB_PAGE_TOKEN")  # Must be system user Page token

    if not page_id or not page_token:
        logger.error("Missing FB_PAGE_ID or FB_PAGE_TOKEN")
        return None

    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"

    try:
        with open(image_path, "rb") as f:
            files = {"source": f}
            data = {"caption": caption, "access_token": page_token}
            r = requests.post(url, files=files, data=data)

        if r.status_code >= 400:
            logger.error(f"facebook_4xx_error: {r.status_code} {r.text}")
            return None

        logger.info(f"Successfully posted: {r.json()}")
        return r.json()

    except Exception as e:
        logger.exception("pipeline_facebook_post_failed")
        return None