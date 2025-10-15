from __future__ import annotations
from typing import Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse
import logging
import requests
from bs4 import BeautifulSoup
import trafilatura
from readability import Document
import dateparser
import pytz
from django.utils.timezone import make_aware

log = logging.getLogger(__name__)

META_DATE_QUERIES = [
    ("meta", {"property": "article:published_time"}),
    ("meta", {"name": "article:published_time"}),
    ("meta", {"property": "og:article:published_time"}),
    ("meta", {"name": "pubdate"}),
    ("meta", {"name": "publish_date"}),
    ("meta", {"itemprop": "datePublished"}),
    ("meta", {"name": "date"}),
    ("time", {"itemprop": "datePublished"}),
    ("time", {}),
]

def fetch_html(url: str, timeout: int = 15) -> str:
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Safari/537.36"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.text

def extract_title(soup: BeautifulSoup) -> Optional[str]:
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    if soup.title and soup.title.text:
        return soup.title.text.strip()
    h1 = soup.find("h1")
    return h1.text.strip() if h1 else None

def extract_html_and_text(html: str) -> Tuple[str, str]:
    extracted = trafilatura.extract(
        html, include_comments=False, include_tables=False, include_images=False, favor_recall=True
    )
    if extracted:
        text_content = extracted.strip()
        html_content = html  # zachowujemy pełny HTML
    else:
        doc = Document(html)
        article_html = doc.summary(html_partial=True)
        text_content = BeautifulSoup(article_html, "lxml").get_text("\n").strip()
        html_content = article_html
    return html_content, text_content

def _dateparse(text: str, base_tz: str) -> Optional[datetime]:
    settings = {
        "PREFER_DATES_FROM": "past",
        "TIMEZONE": base_tz,
        "RETURN_AS_TIMEZONE_AWARE": True,
        "LANGUAGES": ["pl", "en"],
        "DATE_ORDER": "YMD",
    }
    dt = dateparser.parse(text, settings=settings)
    if not dt:
        return None
    if dt.tzinfo is None:
        tz = pytz.timezone(base_tz)
        dt = make_aware(dt, timezone=tz)
    # jeśli brak dokładnej godziny – ustaw 00:00:00
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt

def parse_any_date(soup: BeautifulSoup, base_tz: str = "Europe/Warsaw") -> datetime:
    for tag, attrs in META_DATE_QUERIES:
        el = soup.find(tag, attrs=attrs)
        if el:
            val = el.get("content") if el.has_attr("content") else el.get_text(strip=True)
            if val:
                dt = _dateparse(val, base_tz)
                if dt:
                    return dt
    # fallback: teraz (00:00)
    tz = pytz.timezone(base_tz)
    now = datetime.now(tz)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)

def scrape_one(url: str, base_tz: str = "Europe/Warsaw") -> dict:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    title = extract_title(soup) or "(brak tytułu)"
    pub_dt = parse_any_date(soup, base_tz=base_tz)
    html_content, text_content = extract_html_and_text(html)
    domain = urlparse(url).netloc
    return {
        "title": title,
        "html_content": html_content,
        "text_content": text_content,
        "source_url": url,
        "source_domain": domain,
        "published_at": pub_dt,
    }
