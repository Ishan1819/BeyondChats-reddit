# reddit_scraper.py
# code to scrape a Reddit user's posts and comments

import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_instance():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    reddit.read_only = True
    return reddit


import prawcore

def scrape_user_data(username, post_limit=30, comment_limit=50):
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
