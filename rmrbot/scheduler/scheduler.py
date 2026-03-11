# rmrbot/scheduler.py

import logging
from datetime import datetime, timedelta
from pathlib import Path

from rmrbot.pipeline import run_pipeline

# --- CONFIGURATION ---
SCHEDULE_TIMES = ["08:00", "16:00", "00:00"]  # 3× daily posting
LAST_RUN_FILE = Path(__file__).parent / "last_run.txt"
LOG_FILE = Path(__file__).parent / "scheduler.log"

# --- SETUP LOGGING ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# --- HELPER FUNCTIONS ---
def load_last_run() -> datetime:
    if LAST_RUN_FILE.exists():
        try:
            return datetime.fromisoformat(LAST_RUN_FILE.read_text().strip())
        except Exception as e:
            logging.warning(f"Failed to read last run file: {e}")
    return None


def save_last_run(dt: datetime):
    try:
        LAST_RUN_FILE.write_text(dt.isoformat())
    except Exception as e:
        logging.error(f"Failed to save last run: {e}")


def get_next_scheduled_run(last_run: datetime, now: datetime) -> datetime | None:
    """Return the next scheduled datetime after last_run and now, skipping missed ones."""
    for day_offset in [0, 1]:  # today and tomorrow
        day = now + timedelta(days=day_offset)
        for t in SCHEDULE_TIMES:
            h, m = map(int, t.split(":"))
            scheduled = day.replace(hour=h, minute=m, second=0, microsecond=0)
            if scheduled > now:
                return scheduled
    return None


# --- MAIN ENTRY ---
if __name__ == "__main__":
    logging.info("Scheduler started.")
    now = datetime.now()
    last_run = load_last_run() or (now - timedelta(days=1))

    # Determine if we should run pipeline now
    next_run_time = None
    for t in SCHEDULE_TIMES:
        h, m = map(int, t.split(":"))
        scheduled = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if scheduled > last_run and scheduled <= now:
            next_run_time = scheduled
            break

    if next_run_time:
        logging.info(f"Running next scheduled post for {next_run_time.strftime('%H:%M')}.")
        try:
            run_pipeline()
            logging.info("Pipeline executed successfully.")
        except Exception as e:
            logging.exception(f"Pipeline execution failed: {e}")
        save_last_run(now)
    else:
        logging.info("No scheduled post to run at this time.")

    logging.info("Scheduler finished.")