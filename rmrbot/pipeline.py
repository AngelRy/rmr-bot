import logging
import time

from rmrbot.database.models import get_quote_for_posting, mark_as_posted
from rmrbot.generator.post_text_generator import generate_caption
from rmrbot.generator.image_generator import generate_quote_image
from rmrbot.generator.comment_generator import generate_first_comment
from rmrbot.publisher.facebook_publisher import post_photo_to_page, post_first_comment

logger = logging.getLogger(__name__)


def run_pipeline():
    """
    Orchestrates the full quote posting pipeline:
    1. Select quote
    2. Generate caption
    3. Generate image
    4. Post to Facebook
    5. Post first comment
    6. Update database
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

    # 2️⃣ Generate first comment
    try:
        comment_text = generate_first_comment(quote_text)
    except Exception as e:
        logger.error(
            "pipeline_comment_generation_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )
        comment_text = None

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
                    "note": "Facebook API returned None, check permissions/token",
                },
            )
    except Exception as e:
        logger.exception(
            "pipeline_facebook_post_exception",
            extra={"error": str(e), "quote_id": quote_id, "image_path": image_path},
        )

    # 5️⃣ Post first comment (if post succeeded)
    if result and "post_id" in result and comment_text:
        try:
            post_id = result["post_id"]

            # Wait before commenting for more natural behavior
            time.sleep(90)

            post_first_comment(post_id, comment_text)

        except Exception as e:
            logger.error(
                "pipeline_comment_post_failed",
                extra={"error": str(e), "quote_id": quote_id},
            )

    # 6️⃣ Mark as posted
    try:
        mark_as_posted(quote_id)
    except Exception as e:
        logger.error(
            "pipeline_mark_posted_failed",
            extra={"error": str(e), "quote_id": quote_id},
        )

    # 7️⃣ Log pipeline completion
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