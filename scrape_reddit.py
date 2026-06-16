#!/usr/bin/env python3
"""Scrape post titles from r/unpopularopinion into a CSV for labeling."""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_SUBREDDIT = "unpopularopinion"
DEFAULT_OUTPUT = Path("data/unpopularopinion_posts.csv")
USER_AGENT = "takemeter/1.0 (educational labeling project)"
PULLPUSH_BASE = "https://api.pullpush.io/reddit/search/submission"


def fetch_json(url: str) -> dict | list:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def scrape_reddit_api(subreddit: str, limit: int) -> list[dict]:
    posts: list[dict] = []
    after: str | None = None

    while len(posts) < limit:
        page_size = min(100, limit - len(posts))
        params = {
            "limit": page_size,
            "raw_json": "1",
        }
        if after:
            params["after"] = after

        url = (
            f"https://www.reddit.com/r/{subreddit}/new.json?"
            f"{urllib.parse.urlencode(params)}"
        )
        payload = fetch_json(url)
        children = payload["data"]["children"]
        if not children:
            break

        for child in children:
            post = child["data"]
            posts.append(
                {
                    "id": post["id"],
                    "title": post["title"].strip(),
                }
            )

        after = payload["data"].get("after")
        if not after:
            break
        time.sleep(1)

    return posts[:limit]


def scrape_pullpush(subreddit: str, limit: int) -> list[dict]:
    posts: list[dict] = []
    seen_ids: set[str] = set()
    before: int | None = None

    while len(posts) < limit:
        page_size = min(100, limit - len(posts))
        params = {
            "subreddit": subreddit,
            "size": page_size,
            "sort": "desc",
            "sort_type": "created_utc",
        }
        if before is not None:
            params["before"] = before

        url = f"{PULLPUSH_BASE}?{urllib.parse.urlencode(params)}"
        batch = fetch_json(url)["data"]
        if not batch:
            break

        added = 0
        for post in batch:
            post_id = post["id"]
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            posts.append(
                {
                    "id": post_id,
                    "title": post["title"].strip(),
                }
            )
            added += 1
            if len(posts) >= limit:
                break

        if added == 0:
            break

        before = batch[-1]["created_utc"]
        time.sleep(0.5)

    return posts[:limit]


def scrape_posts(subreddit: str, limit: int) -> tuple[list[dict], str]:
    try:
        posts = scrape_reddit_api(subreddit, limit)
        if posts:
            return posts, "reddit_api"
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        print(f"Reddit API unavailable ({exc}); falling back to Pullpush archive.")

    posts = scrape_pullpush(subreddit, limit)
    return posts, "pullpush"


def write_csv(posts: list[dict], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seen_titles: set[str] = set()
    rows: list[dict[str, str]] = []

    for post in posts:
        title = post["title"].strip()
        normalized = title.casefold()
        if not title or normalized in seen_titles:
            continue
        seen_titles.add(normalized)
        rows.append({"text": title, "label": "", "difficulty": ""})

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["text", "label", "difficulty"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape r/unpopularopinion post titles into a labeling CSV."
    )
    parser.add_argument(
        "--subreddit",
        default=DEFAULT_SUBREDDIT,
        help="Subreddit name without r/ prefix.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Maximum number of unique posts to collect.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path.",
    )
    args = parser.parse_args()

    posts, source = scrape_posts(args.subreddit, args.limit)
    if not posts:
        raise SystemExit("No posts were collected.")

    row_count = write_csv(posts, args.output)
    print(f"Saved {row_count} unique posts from {source} to {args.output}")


if __name__ == "__main__":
    main()
