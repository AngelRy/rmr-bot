import time
import logging
import json
from dotenv import load_dotenv

load_dotenv()

from rmrbot.scraper.quotes_scraper import scrape
from rmrbot.ml.relevance import classify_quotes_batch
from rmrbot.database.models import insert_quote
from rmrbot.database.db import init_db, get_connection

logging.basicConfig(level=logging.INFO)


def main():
    start = time.time()

    init_db()

    scraped = scrape()
    scraped_count = len(scraped)

    logging.info(json.dumps({
        "event": "scrape_complete",
        "count": scraped_count
    }))

    # 1️⃣ Batch classify (single model call)
    results = classify_quotes_batch(scraped)

    # 2️⃣ Single DB connection
    conn = get_connection()
    inserted = 0
    duplicates = 0
    rejected = 0

    try:
        for text, (score, is_relevant) in zip(scraped, results):
            success, error = insert_quote(
                text,
                score,
                is_relevant,
                conn=conn  # ← reuse connection
            )

            if success:
                inserted += 1
            else:
                if error and "duplicate" in error.lower():
                    duplicates += 1
                else:
                    rejected += 1

        conn.commit()  # commit once

    finally:
        conn.close()  # close once

    duration = round(time.time() - start, 2)

    summary = {
        "event": "ingestion_summary",
        "scraped": scraped_count,
        "inserted": inserted,
        "duplicates": duplicates,
        "rejected": rejected,
        "duration_sec": duration
    }

    logging.info(json.dumps(summary))


if __name__ == "__main__":
    main()