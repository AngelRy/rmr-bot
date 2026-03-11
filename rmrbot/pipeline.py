'''
import logging
from rmrbot.database.models import get_quote_for_posting, mark_as_posted
from rmrbot.generator.post_text_generator import generate_caption
from rmrbot.generator.image_generator import generate_quote_image
from rmrbot.publisher.facebook_publisher import post_photo_to_page
import os

logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Full RMR Bot quote posting pipeline:
    1. Select quote
    2. Generate caption
    3. Generate image
    4. Post to Facebook (system user Page token)
    5. Mark as posted
    """

    logger.info("pipeline_start")

    # 1️⃣ Select quote
    quote_row = get_quote_for_posting()
    if not quote_row:
        logger.warning("pipeline_no_eligible_quote")
        return

    quote_id, quote_text = quote_row
    author = None  # Extend if author stored in DB

    # 2️⃣ Generate caption
    caption = generate_caption(quote_text, author)

    # 3️⃣ Generate image
    try:
        image_path = generate_quote_image(quote_text, author)
    except Exception as e:
        logger.error(
            "pipeline_image_generation_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )
        raise

    # 4️⃣ Post image to Facebook
    result = None
    try:
        result = post_photo_to_page(image_path, caption)
        if result is None:
            logger.error(
                "pipeline_facebook_post_failed",
                extra={
                    "quote_id": quote_id,
                    "image_path": image_path,
                    "note": "Facebook API returned None; check system user token and Page ID",
                },
            )
        else:
            logger.info(
                "pipeline_facebook_post_success",
                extra={"quote_id": quote_id, "facebook_response": result},
            )
    except Exception as e:
        logger.exception(
            "pipeline_facebook_post_exception",
            extra={"error": str(e), "quote_id": quote_id, "image_path": image_path},
        )

    # 5️⃣ Mark as posted only if image was generated
    try:
        mark_as_posted(quote_id)
    except Exception as e:
        logger.error(
            "pipeline_mark_posted_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )

    # 6️⃣ Pipeline completion log
    logger.info(
        "pipeline_end",
        extra={
            "quote_id": quote_id,
            "image_path": image_path,
            "facebook_post_result": result,
        },
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
'''

import logging
from rmrbot.database.models import get_quote_for_posting, mark_as_posted
from rmrbot.generator.post_text_generator import generate_caption
from rmrbot.generator.image_generator import generate_quote_image
from rmrbot.publisher.facebook_publisher import post_photo_to_page

logger = logging.getLogger(__name__)


def run_pipeline():
    """
    Orchestrates the full quote posting pipeline:
    1. Select quote
    2. Generate caption
    3. Generate image
    4. Post to Facebook
    5. Update database
    """

    logger.info("pipeline_start")

    # Fetch a quote from the database
    quote_row = get_quote_for_posting()
    if not quote_row:
        logger.warning("pipeline_no_eligible_quote")
        return

    # Extract values correctly from the dictionary
    quote_id = quote_row['id']
    quote_text = quote_row['text']
    author = None  # Extend if you store author in DB

    # 1️⃣ Generate caption
    caption = generate_caption(quote_text, author)

    # 2️⃣ Generate image
    try:
        image_path = generate_quote_image(quote_text, author)
    except Exception as e:
        logger.error(
            "pipeline_image_generation_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )
        raise

    # 3️⃣ Post image to Facebook
    result = None
    try:
        result = post_photo_to_page(image_path, caption)
        if result is None:
            logger.error(
                "pipeline_facebook_post_failed",
                extra={
                    "quote_id": quote_id,
                    "image_path": image_path,
                    "note": "Facebook API returned None, check permissions/token",
                },
            )
    except Exception as e:
        logger.exception(
            "pipeline_facebook_post_exception",
            extra={"error": str(e), "quote_id": quote_id, "image_path": image_path},
        )

    # 4️⃣ Mark as posted
    try:
        mark_as_posted(quote_id)
    except Exception as e:
        logger.error(
            "pipeline_mark_posted_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )

    # 5️⃣ Log pipeline completion
    logger.info(
        "pipeline_end",
        extra={
            "quote_id": quote_id,
            "image_path": image_path,
            "facebook_post_result": result,
        },
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()