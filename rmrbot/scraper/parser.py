from bs4 import BeautifulSoup


def parse(html, url):

    if "keepinspiring.me" in url:
        return parse_keepinspiring(html)

    if "goodreads.com" in url:
        return parse_goodreads(html)

    if "runnersworld.com" in url:
        return parse_runnersworld(html)

    if "azquotes.com" in url:
        return parse_azquotes(html)

    if "brainyquote.com" in url:
        return parse_brainyquote(html)

    return []

def parse_keepinspiring(html):
    soup = BeautifulSoup(html, "html.parser")
    return [b.get_text(strip=True) for b in soup.find_all("blockquote")]

def parse_goodreads(html):
    soup = BeautifulSoup(html, "html.parser")
    return [
        div.get_text(strip=True)
        for div in soup.find_all("div", class_="quoteText")
    ]

def parse_runnersworld(html):
    # Often empty due to bot protection
    return []

def parse_azquotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    blocks = soup.select("div.wrap-block")

    for block in blocks:
        text_el = block.select_one("a.title")
        if not text_el:
            continue

        quote = text_el.get_text(strip=True)

        if quote:
            quotes.append(quote)

    return quotes

def parse_brainyquote(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    blocks = soup.select("div.grid-item")

    for block in blocks:
        text_el = block.select_one("a.b-qt")
        if not text_el:
            continue

        quote = text_el.get_text(strip=True)

        if quote:
            quotes.append(quote)

    return quotes