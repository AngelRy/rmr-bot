###for testing only, remove before production
from dotenv import load_dotenv
load_dotenv()
###for testing only, remove before production

import os
import time
import logging
import requests


MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds


def post_photo_to_page(image_path: str, caption: str):
    """
    Posts a photo to a Facebook Page using the Graph API.

    Retries on transient failures (network errors, timeouts, HTTP 5xx).
    Does NOT retry on client errors (HTTP 4xx).
    """

    page_id = os.getenv("FB_PAGE_ID")
    page_token = os.getenv("FB_PAGE_TOKEN")

    if not page_id or not page_token:
        raise RuntimeError("FB_PAGE_ID or FB_PAGE_TOKEN not set in environment")

    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"

    attempt = 0
    backoff = INITIAL_BACKOFF

    while attempt < MAX_RETRIES:
        try:
            with open(image_path, "rb") as f:
                files = {
                    "source": (
                        os.path.basename(image_path),
                        f,
                        "image/png",
                    )
                }

                data = {
                    "caption": caption,
                    "access_token": page_token,
                }

                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    timeout=15,  # prevent hanging forever
                )

            status_code = response.status_code

            # Retry on 5xx only
            if 500 <= status_code < 600:
                raise requests.exceptions.HTTPError(
                    f"Server error {status_code}",
                    response=response,
                )

            # Raise for 4xx (non-retryable)
            response.raise_for_status()

            result = response.json()

            logging.info(
                "facebook_post_success",
                extra={
                    "event": "facebook_post_success",
                    "status_code": status_code,
                    "post_id": result.get("id"),
                    "page_id": page_id,
                },
            )

            return result

        except requests.exceptions.Timeout as e:
            logging.warning(
                "facebook_timeout",
                extra={
                    "event": "facebook_timeout",
                    "attempt": attempt + 1,
                    "max_retries": MAX_RETRIES,
                    "error": str(e),
                },
            )

        except requests.exceptions.ConnectionError as e:
            logging.warning(
                "facebook_connection_error",
                extra={
                    "event": "facebook_connection_error",
                    "attempt": attempt + 1,
                    "max_retries": MAX_RETRIES,
                    "error": str(e),
                },
            )

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else None

            if status and 500 <= status < 600:
                logging.warning(
                    "facebook_5xx_error",
                    extra={
                        "event": "facebook_5xx_error",
                        "status_code": status,
                        "attempt": attempt + 1,
                        "max_retries": MAX_RETRIES,
                    },
                )
            else:
                logging.error(
                    "facebook_4xx_error",
                    extra={
                        "event": "facebook_4xx_error",
                        "status_code": status,
                        "response_body": e.response.text if e.response else None,
                    },
                )
                raise

        attempt += 1

        if attempt < MAX_RETRIES:
            logging.warning(
                "facebook retry",
                extra={
                    "event": "facebook_retry",
                    "attempt": attempt,
                    "max_retries": MAX_RETRIES,
                    "wait_seconds": backoff,
                },

            )
        
            time.sleep(backoff)
            backoff *= 2

    logging.error(
    "facebook_max_retries_exceeded",
    extra={
        "event": "facebook_max_retries_exceeded",
        "max_retries": MAX_RETRIES,
    },
)