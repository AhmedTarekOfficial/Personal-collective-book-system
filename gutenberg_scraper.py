"""
Project Gutenberg Book Scraper
==============================
Scrapes book metadata (title, author, language, ISBN, release date, subjects)
from https://www.gutenberg.org and saves results to books_data.json

Usage:
    python gutenberg_scraper.py

Dependencies:
    pip install requests beautifulsoup4
"""

import json
import time
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# -- Configuration -------------------------------------------------------------
TARGET_BOOK_COUNT = 50
OUTPUT_FILE       = "books_data.json"
REQUEST_DELAY     = 1.2          # seconds between requests (be a polite scraper)
REQUEST_TIMEOUT   = 15           # seconds
MAX_RETRIES       = 3

BASE_URL          = "https://www.gutenberg.org"
SEARCH_URL        = "https://www.gutenberg.org/ebooks/search/?sort_order=release_date&start_index={start}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# -- Logging setup -------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# -- HTTP helper ---------------------------------------------------------------
def fetch(url: str) -> BeautifulSoup | None:
    """Fetch a URL and return a BeautifulSoup object, or None on failure."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as exc:
            log.warning("Attempt %d/%d failed for %s -- %s", attempt, MAX_RETRIES, url, exc)
            if attempt < MAX_RETRIES:
                time.sleep(REQUEST_DELAY * attempt)
    log.error("All retries exhausted for %s", url)
    return None


# -- Listing page parser -------------------------------------------------------
def parse_listing_page(soup: BeautifulSoup) -> list:
    """
    Extract individual book page URLs from a search-results listing page.
    Returns a list of absolute URLs like 'https://www.gutenberg.org/ebooks/12345'.
    """
    book_urls = []

    for anchor in soup.select("li.booklink a.link"):
        href = anchor.get("href", "")
        if href.startswith("/ebooks/") and href[8:].isdigit():
            book_urls.append(BASE_URL + href)

    return book_urls


# -- Individual book page parser -----------------------------------------------
def parse_book_page(url: str, soup: BeautifulSoup) -> dict:
    """
    Extract metadata from a single book page.
    Fields: title, author, language, isbn, release_date, subjects, book_url
    """

    def get_bibrec_value(label: str) -> str:
        """Pull a value from the bibrec table by its label text."""
        row = soup.find("th", string=re.compile(label, re.I))
        if row:
            td = row.find_next_sibling("td")
            if td:
                return td.get_text(separator=" ", strip=True)
        return ""

    def get_all_bibrec_values(label: str) -> list:
        """Pull ALL values for a repeating label (e.g. multiple subjects)."""
        values = []
        for row in soup.find_all("th", string=re.compile(label, re.I)):
            td = row.find_next_sibling("td")
            if td:
                values.append(td.get_text(separator=" ", strip=True))
        return values

    # Title
    title_tag = soup.select_one("h1[itemprop='name']") or soup.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else get_bibrec_value("Title")

    # Author
    author_tag = soup.select_one("a[itemprop='creator']")
    author = author_tag.get_text(strip=True) if author_tag else get_bibrec_value("Author")

    # Language
    lang_tag = soup.select_one("tr[itemprop='inLanguage'] td")
    language = lang_tag.get_text(strip=True) if lang_tag else get_bibrec_value("Language")

    # Release Date
    date_tag = soup.select_one("td[itemprop='datePublished']")
    release_date = date_tag.get_text(strip=True) if date_tag else get_bibrec_value("Release date")

    # ISBN  -- Gutenberg books rarely have one; try multiple fallbacks
    isbn = get_bibrec_value("ISBN")
    if not isbn:
        m = re.search(r"\bISBN[:\s]*([\d\-X]{10,17})", soup.get_text())
        isbn = m.group(1).strip() if m else "N/A"

    # Subjects
    subject_tags = soup.select("td[itemprop='about'] a")
    if subject_tags:
        subjects = [t.get_text(strip=True) for t in subject_tags]
    else:
        subjects = get_all_bibrec_values("Subject")

    return {
        "title":        title or "Unknown",
        "author":       author or "Unknown",
        "language":     language or "Unknown",
        "isbn":         isbn,
        "release_date": release_date or "Unknown",
        "subjects":     subjects,
    }


# -- Main scraping loop --------------------------------------------------------
def scrape_gutenberg(target: int = TARGET_BOOK_COUNT) -> list:
    books = []
    seen_urls = set()
    page_start = 0      # Gutenberg paginates with ?start_index=N (25 per page)

    log.info("Starting Project Gutenberg scrape -- target: %d books", target)

    while len(books) < target:
        list_url = SEARCH_URL.format(start=page_start)
        log.info("Fetching listing page (start=%d) ...", page_start)

        list_soup = fetch(list_url)
        if list_soup is None:
            log.error("Failed to fetch listing page, stopping.")
            break

        book_urls = parse_listing_page(list_soup)
        if not book_urls:
            log.info("No more book links found on listing page, stopping.")
            break

        log.info("Found %d books on this page", len(book_urls))

        for book_url in book_urls:
            if len(books) >= target:
                break
            if book_url in seen_urls:
                continue
            seen_urls.add(book_url)

            log.info("[%02d/%d] Scraping: %s", len(books) + 1, target, book_url)
            time.sleep(REQUEST_DELAY)

            book_soup = fetch(book_url)
            if book_soup is None:
                log.warning("Skipping %s -- fetch failed", book_url)
                continue

            try:
                book_data = parse_book_page(book_url, book_soup)
                books.append(book_data)
                log.info(
                    "  + %-60s | Author: %s | Lang: %s | Date: %s",
                    book_data["title"][:60],
                    book_data["author"][:30],
                    book_data["language"],
                    book_data["release_date"],
                )
            except Exception as exc:
                log.exception("Error parsing %s: %s", book_url, exc)

        page_start += 25   # advance to next listing page

    return books


# -- Entry point ---------------------------------------------------------------
def main():
    books = scrape_gutenberg()

    if not books:
        log.error("No books collected -- aborting file write.")
        return

    output = {
        "metadata": {
            "source":      "https://www.gutenberg.org",
            "total_books": len(books),
            "description": "Book metadata scraped from Project Gutenberg",
        },
        "books": books,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log.info("Done! %d books saved to '%s'", len(books), OUTPUT_FILE)


if __name__ == "__main__":
    main()
