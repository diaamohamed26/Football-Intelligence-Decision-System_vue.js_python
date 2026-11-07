
import calendar
import re
import urllib.request

import feedparser

from datetime import datetime, timezone as dt_timezone
from html import unescape

from django.utils import timezone

from .models import NewsArticle


NEWS_FEEDS = [
    {
        "name": "BBC Sport",
        "url": "https://feeds.bbci.co.uk/sport/football/rss.xml",
        "website": "https://www.bbc.com/sport/football",
    },
    {
        "name": "The Guardian",
        "url": "https://www.theguardian.com/football/rss",
        "website": "https://www.theguardian.com/football",
    },
    {
        "name": "Sky Sports",
        "url": "https://www.skysports.com/rss/11095",
        "website": "https://www.skysports.com/football",
    },
    {
        "name": "The Athletic",
        "url": "https://www.nytimes.com/athletic/rss/football/",
        "website": "https://www.nytimes.com/athletic/football/",
    },
]

CATEGORY_KEYWORDS = {
    "transfers": [
        "transfer", "signing", "signed", "signs",
        "loan deal", "transfer window", "linked with",
        "transfer target", "rumour", "rumor"
    ],
    "injuries": [
        "injury", "injured", "hamstring", "knee injury",
        "fitness", "surgery", "suspended", "suspension"
    ],
    "managers": [
        "manager", "coach", "sacked", "appointed",
        "head coach", "resigns"
    ],
    "international": [
        "world cup", "national team", "international",
        "afcon", "africa cup of nations", "qualifier",
        "uefa nations league"
    ],
    "matches": [
        "match report", "full-time", "kick-off",
        "premier league", "champions league",
        "la liga", "serie a", "bundesliga",
        "ligue 1", "matchday", "fixture"
    ],
    "breaking": [
        "breaking", "just in", "official announcement",
        "confirmed", "officially"
    ],
}

RUMOUR_KEYWORDS = [
    "rumour", "rumor", "reportedly", "linked with",
    "interested in", "could sign", "eyeing",
    "transfer target", "considering a move"
]


def clean_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def detect_category(title, summary):
    text = f"{title} {summary}".lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "general"


def is_transfer_rumour(title, summary):
    text = f"{title} {summary}".lower()

    return any(
        keyword in text for keyword in RUMOUR_KEYWORDS
    )


def extract_image(entry):
    thumbnails = entry.get("media_thumbnail", [])

    if thumbnails:
        return thumbnails[0].get("url", "")

    media = entry.get("media_content", [])

    if media:
        return media[0].get("url", "")

    enclosures = entry.get("enclosures", [])

    for enclosure in enclosures:
        if enclosure.get("type", "").startswith("image/"):
            return enclosure.get("href", "")

    return ""


def parse_published_date(entry):
    parsed = (
        entry.get("published_parsed")
        or entry.get("updated_parsed")
    )

    if not parsed:
        return None

    timestamp = calendar.timegm(parsed)

    return datetime.fromtimestamp(
        timestamp,
        tz=dt_timezone.utc
    )


def fetch_feed(feed):
    request = urllib.request.Request(
        feed["url"],
        headers={
            "User-Agent": "FIDS-Football-News/1.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=15
    ) as response:
        content = response.read()

    return feedparser.parse(content)


def sync_football_news():
    stats = {
        "sources": 0,
        "created": 0,
        "updated": 0,
        "errors": []
    }

    for feed in NEWS_FEEDS:
        try:
            parsed_feed = fetch_feed(feed)
            stats["sources"] += 1

            for entry in parsed_feed.entries:
                title = clean_text(entry.get("title"))

                article_url = entry.get("link", "").strip()

                if not title or not article_url:
                    continue

                summary = clean_text(
                    entry.get("summary", "")
                )[:2000]

                category = detect_category(
                    title, summary
                )

                published_at = parse_published_date(entry)

                article, created = NewsArticle.objects.update_or_create(
                    article_url=article_url,
                    defaults={
                        "title": title[:500],
                        "summary": summary,
                        "source_name": feed["name"],
                        "source_url": feed["website"],
                        "image_url": extract_image(entry),
                        "category": category,
                        "is_rumour": is_transfer_rumour(
                            title, summary
                        ),
                        "published_at": published_at,
                    }
                )

                if created:
                    stats["created"] += 1
                else:
                    stats["updated"] += 1

        except Exception as error:
            stats["errors"].append({
                "source": feed["name"],
                "error": str(error)
            })

    return stats
