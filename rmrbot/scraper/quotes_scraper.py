from rmrbot.generator.quote_parser import parse_quote

from rmrbot.scraper.sources import RUNNING_SOURCES
from rmrbot.scraper.fetcher import fetch
from rmrbot.scraper.parser import (
    parse_keepinspiring,
    parse_goodreads,
    parse_runnersworld,
    parse_azquotes,
    parse_brainyquote,
)
from rmrbot.scraper.cleaner import clean


MIN_QUOTE_LENGTH = 40
MAX_QUOTE_LENGTH = 280

def build_paginated_url(base_url, page):

    if "azquotes.com" in base_url:
        if page == 1:
            return base_url
        return f"{base_url}?p={page}"

    if "brainyquote.com" in base_url:
        if page == 1:
            return base_url
        return f"{base_url}_{page}"

    if "goodreads.com" in base_url:
        return f"{base_url}?page={page}"

    # others single page
    return base_url

def scrape():
    quotes = []

    for base_url in RUNNING_SOURCES:

        for page in range(1, 27):  # up to 10 pages
            url = build_paginated_url(base_url, page)

            print(f"Scraping: {url}")

            html = fetch(url)
            if not html:
                break

            if "keepinspiring.me" in base_url:
                parsed = parse_keepinspiring(html)

            elif "goodreads.com" in base_url:
                parsed = parse_goodreads(html)

            elif "runnersworld.com" in base_url:
                parsed = parse_runnersworld(html)

            elif "azquotes.com" in base_url:
                parsed = parse_azquotes(html)

            elif "brainyquote.com" in base_url:
                parsed = parse_brainyquote(html)

            else:
                continue

            if not parsed:
                break  # stop pagination if empty

            for q in parsed:
                q = clean(q)

                if not (MIN_QUOTE_LENGTH <= len(q) <= MAX_QUOTE_LENGTH):
                    continue

                              
                quotes.append(q)

    return list(set(quotes))
