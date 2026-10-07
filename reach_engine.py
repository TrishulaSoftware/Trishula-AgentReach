"""
reach_engine.py — Sovereign Multi-Platform Stealth Radar
Extracts intelligence from Twitter/X, Reddit, YouTube, and GitHub without paid API keys.
Part of Trishula Sovereign Fleet (Trishula Software)
"""

import re
import json
import urllib.request
from typing import Dict, Any, Optional

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class SovereignAgentReach:
    """
    Stealth multi-platform reconnaissance sensor.
    Handles unauthenticated intelligence gathering across major platforms.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/json,application/xhtml+xml,*/*",
            "Accept-Language": "en-US,en;q=0.9"
        }

    def inspect_x_post(self, tweet_url: str) -> Dict[str, Any]:
        """Scrapes Twitter/X post via syndication and OpenGraph fallback."""
        # Convert twitter.com/x.com to fxtwitter / fixupx API for instant unauthenticated JSON
        match = re.search(r"(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+)/status/([0-9]+)", tweet_url)
        if not match:
            return {"success": False, "error": "Invalid X / Twitter post URL"}

        author, tweet_id = match.group(1), match.group(2)
        api_url = f"https://api.fxtwitter.com/{author}/status/{tweet_id}"

        try:
            req = urllib.request.Request(api_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                tweet = data.get("tweet", {})
                return {
                    "success": True,
                    "platform": "X (Twitter)",
                    "author": tweet.get("author", {}).get("screen_name", author),
                    "author_name": tweet.get("author", {}).get("name", ""),
                    "text": tweet.get("text", ""),
                    "created_at": tweet.get("created_at", ""),
                    "likes": tweet.get("likes", 0),
                    "retweets": tweet.get("retweets", 0),
                    "media_urls": [m.get("url") for m in tweet.get("media", {}).get("all", []) if m.get("url")]
                }
        except Exception as e:
            return {"success": False, "error": f"FXTwitter extraction fallback failed: {str(e)}"}

    def inspect_reddit_post(self, reddit_url: str) -> Dict[str, Any]:
        """Extracts complete Reddit post and top comments via native .json endpoint."""
        clean_url = reddit_url.split("?")[0].rstrip("/") + ".json"
        try:
            req = urllib.request.Request(clean_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                post_data = data[0]["data"]["children"][0]["data"]
                return {
                    "success": True,
                    "platform": "Reddit",
                    "subreddit": post_data.get("subreddit"),
                    "title": post_data.get("title"),
                    "selftext": post_data.get("selftext"),
                    "author": post_data.get("author"),
                    "score": post_data.get("score"),
                    "num_comments": post_data.get("num_comments"),
                    "url": post_data.get("url")
                }
        except Exception as e:
            return {"success": False, "error": f"Reddit JSON extraction failed: {str(e)}"}
