# persona_generator.py
# Code to generate a persona from Reddit posts and comments

import os
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# ── Main function ─────────────────────────────────────────────────────────────
def generate_persona(posts: list[dict], comments: list[dict], username: str) -> str:
    """
    Build a detailed persona for `username` and return it as plain text.
    Each insight must cite the source (post/comment URL).
    """

    # ── 1. Concatenate Reddit data ─────────────────────────────────────────────
    combined_data = ["### Reddit Posts ###"]
    for p in posts:
        combined_data.append(
            f"- Title: {p['title']}\n  Body: {p['body']}\n  Source: {p['link']}\n"
        )

    combined_data.append("### Reddit Comments ###")
    for c in comments:
        combined_data.append(
            f"- Comment: {c['body']}\n  Source: {c['link']}\n"
        )

    data_block = "\n".join(combined_data)

    # ── 2. Prompt Gemini with structured UX persona format ─────────────────────
    prompt = f"""
You are an expert in psychological profiling and UX persona creation.
Below are some of the parameters you should use to generate a detailed user persona based on Reddit posts and comments. Add more parameters if relevant. If there is not enough information or the user is inactive or banned, return: "Not enough information to generate a persona for this user."

Using the Reddit posts and comments below, generate a structured user persona for **u/{username}** in the format below.

---

### Basic Profile
- Name: (If not available, use 'u/{username}')
- Age: (Estimate if possible or leave blank)
- Occupation: (Guess from context or say 'Unknown')
- Status: (Single, Married, Unknown)
- Location: (If guessable)
- Tier: (e.g., Early Adopter, Mainstream — optional)
- Archetype: (e.g., The Creator, The Analyst, The Helper)

---

### Trait Tags
List 3–6 traits like: Practical, Adaptive, Curious, Analytical, etc.

---

### Quote
A one-line quote that reflects their mindset or frustration  
(e.g., "I want to spend less time ordering food and more time enjoying it.")

---

### Motivations (Rate from 1 to 5)
- Convenience  
- Wellness  
- Speed  
- Preferences  
- Comfort  
- Dietary Needs

---

### Personality (Scale 0–5)
- Openness (4) - (1) Closed
- Introvert (2) - (3) Extrovert  
- Intuition (3) - (2) Sensing  
- Feeling (1) - (4) Thinking  
- Perceiving (5) - (0) Judging

---

### Behaviour & Habits
List 4–6 behavioral patterns observed from their posts/comments. Cite Reddit URLs.

---

### Frustrations
List 3–5 common pain points or complaints.

---

### Goals & Needs
List 3–5 key desires or priorities.

---

Use only insights from the user’s Reddit content below. **Cite Reddit URLs wherever possible**.

---

{data_block}
"""

    # ── 3. Send to Gemini-Pro ─────────────────────────────────────────────────
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # ── 4. Attach metadata ─────────────────────────────────────────────────────
    metadata = (
        f"---\n"
        f"Username: u/{username}\n"
        f"Profile URL: https://www.reddit.com/user/{username}/\n"
        f"Posts Scraped: {len(posts)}\n"
        f"Comments Scraped: {len(comments)}\n"
        f"---\n\n"
    )

    # ── 5. Return structured result ────────────────────────────────────────────
    return metadata + response.text
