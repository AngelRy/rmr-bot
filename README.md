



# RMR Bot

Automated motivational running quote poster.  
Generates quote images, captions, and posts them to a Facebook Page automatically.  
Includes web scraping and embedding-based relevance filtering to focus on **distance running quotes**.



## Features

- Selects quotes from SQLite database with 4-week cooldown logic  
- Scrapes motivational quotes from websites  
- **Relevance filter using embeddings** ensures quotes are related to distance running  
  - Centroid built from curated anchor quotes (`data/distance_running_anchor_quotes.csv`)  
  - Uses `sentence-transformers` (`all-MiniLM-L6-v2`) and cosine similarity  
- Generates professional-looking images with optional author  
- Generates captions using OpenAI GPT-4o-mini or deterministic fallback  
- Posts to Facebook using Page Access Token  
- Scheduler supports offline resilience (skips missed posts)  
- Logs and outputs stored in `logs/` and `output/`



## Tech Stack

- Python 3.12  
- Libraries:
  - `requests`, `beautifulsoup4` for scraping
  - `sentence-transformers`, `numpy`, `pandas`, `joblib` for embedding-based relevance filtering
  - `Pillow`, `python-dotenv`, `openai` (optional)
  - `facebook-sdk` for posting
  - `APScheduler` or `schedule` for scheduling

---

## Folder Structure

```

rmr-bot/
├── assets/                  # fonts, images, logos
├── archive/                 # experimental or development scripts
│   ├── build_centroid.py
│   ├── generate_image.py
│   └── inspect_similarity.py
├── data/                    # small CSVs, e.g., anchor quotes
├── logs/                    # generated logs (ignored by Git)
├── main.py                  # optional entry point
├── models/                  # precomputed centroid & embedding model
│   ├── running_centroid.joblib
│   └── embedding_model.joblib
├── output/                  # generated images (ignored by Git)
├── rmrbot/                  # main Python package
│   ├── config/              # settings.py, environment configs
│   ├── database/            # SQLite DB models
│   ├── generator/           # image generation, caption logic
│   ├── ml/                  # optional ML-related scripts
│   ├── publisher/           # Facebook posting logic
│   ├── scraper/             # scraping + embedding relevance
│   │   ├── build_centroid.py
│   │   ├── embedding_filter.py
│   │   ├── scraper.py
│   │   └── utils.py
│   ├── scheduler/           # scheduler.py
│   ├── pipeline.py          # main orchestration script
│   └── logging_config.py
├── scripts/                 # helper scripts (init_db, scrape_and_save, etc.)
├── tests/                   # unit tests
├── README.md
├── requirements.txt
└── rmvnv/                   # virtual environment (ignored by Git)

````

> **Ignored in GitHub:** `logs/`, `output/`, `rmvnv/`, `.env`  

---

## Setup Instructions

### 1. Clone repository

```bash
git clone <repo_url>
cd rmr-bot
````

### 2. Create Python virtual environment

```bash
python3 -m venv rmvnv
source rmvnv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Fill in your own tokens and keys:

```text
FB_PAGE_ID=your_real_page_id
FB_PAGE_TOKEN=your_real_page_access_token
FB_APP_TOKEN=your_real_app_token
OPENAI_API_KEY=your_real_openai_api_key (optional)
```

> **Important:** `.env` is ignored by Git.
> `.env.example` contains placeholders and is safe to commit.

---

### 5. Rebuild Distance Running Centroid (optional)

```bash
python3 -m rmrbot.scraper.build_centroid
```

* Generates `models/running_centroid.joblib` and `models/embedding_model.joblib`
* Used by `scraper/embedding_filter.py` to filter quotes relevant to distance running

---

### 6. Test the pipeline manually

```bash
python3 -m rmrbot.pipeline
```

* Runs the end-to-end pipeline: selects a quote, generates caption, generates image, posts to Facebook, and marks the quote as posted

---

### 7. Test the scheduler manually

```bash
python3 -m rmrbot.scheduler.scheduler
```

* Scheduler handles posting the next quote at scheduled times
* Skips missed posts if the machine was offline

---

## Scheduler / Automation

* Example cron job (runs hourly):

```bash
0 * * * * PYTHONPATH=/home/angels/rmr-bot /home/angels/rmr-bot/rmvnv/bin/python3 /home/angels/rmr-bot/rmrbot/scheduler/scheduler.py >> /home/angels/rmr-bot/logs/cron.log 2>&1
```

* Scheduler posts **only the next scheduled quote**, skipping missed ones
* Logs are saved automatically in `logs/cron.log`

---

## License

MIT License

