# rmrbot/scheduler/scheduler.py

import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# --- Load .env before anything else ---
load_dotenv()

from rmrbot.pipeline import run_pipeline

# --- Logging setup ---
log_file = os.path.join(os.path.dirname(__file__), "scheduler.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logging.info("Scheduler started")

# --- Skip backlog logic ---
# The pipeline itself should select one quote per run,
# respecting the 4-week cooldown, so no missed posts accumulate.

if __name__ == "__main__":
    try:
        logging.info("pipeline_start")
        run_pipeline()
        logging.info("pipeline_end")
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.exception("Pipeline failed with exception")