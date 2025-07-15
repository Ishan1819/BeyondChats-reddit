"""reddit_scraper.py

Module to scrape a Reddit user's posts and comments using PRAW.
"""

import os
import praw
import prawcore
from dotenv import load_dotenv

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()


def get_reddit_instance() -> praw.Reddit:
    """Initialize and return a read-only Reddit instance."""
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    reddit.read_only = True
    return reddit


def scrape_user_data(
    username: str, post_limit: int = 30, comment_limit: int = 50
) -> tuple[list[dict], list[dict]]:
    """
    Scrape posts and comments for a given Reddit username.

    Parameters
    ----------
    username : str
        The Reddit username to scrape.
    post_limit : int
        Number of posts to fetch (default is 30).
    comment_limit : int
        Number of comments to fetch (default is 50).

    Returns
    -------
    tuple
        A tuple containing two lists: posts and comments.
    """
    reddit = get_reddit_instance()
    redditor = reddit.redditor(username)

    posts = []
    comments = []

    try:
        for submission in redditor.submissions.new(limit=post_limit):
            posts.append({
                "title": submission.title,
                "body": submission.selftext,
                "link": f"https://reddit.com{submission.permalink}"
            })
    except prawcore.exceptions.NotFound:
        print(f"[!] User '{username}' not found or has no public submissions.")
        return [], []

    try:
        for comment in redditor.comments.new(limit=comment_limit):
            comments.append({
                "body": comment.body,
                "link": f"https://reddit.com{comment.permalink}"
            })
    except prawcore.exceptions.NotFound:
        print(f"[!] User '{username}' not found or has no public comments.")
        return posts, []

    return posts, comments
