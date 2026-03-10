# scraper/sources.py

import time

RUNNING_SOURCES = [
    "https://www.runnersworld.com/quotes/",
    "https://www.goodreads.com/quotes/tag/running",
    "https://www.keepinspiring.me/running-quotes/",
    "https://www.azquotes.com/quotes/topics/running.html"
]


def scrape():
    quotes = []

    for base_url in RUNNING_SOURCES:

        # ---- PAGINATION LOOP ----
        for page in range(1, 11):  # scrape up to 10 pages
            url = build_paginated_url(base_url, page)

            print(f"Scraping: {url}")
            html = fetch(url)

            if not html:
                break

            parsed = parse(html, url)

            if not parsed:
                break  # stop pagination when no results

            for q in parsed:
                q = clean(q)
                if len(q) > 20:
                    quotes.append(q)

            time.sleep(2)  # polite delay

    return list(set(quotes))


def build_paginated_url(base_url, page):

    # AZQuotes pagination: ?p=2
    if "azquotes.com" in base_url:
        if page == 1:
            return base_url
        return f"{base_url}?p={page}"

    # BrainyQuote pagination: _2
    if "brainyquote.com" in base_url:
        if page == 1:
            return base_url
        return f"{base_url}_{page}"

    # Goodreads pagination: ?page=2
    if "goodreads.com" in base_url:
        return f"{base_url}?page={page}"

    # Others: single page
    return base_url