# persona_generator.py
# code to get the information about how to generate a persona from reddit posts and comments

from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # <-- Make sure this is set

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
Below are some of the paramters you should use to generate a detailed user persona based on Reddit posts and comments. Add some more parameters other than included below that could be useful for a UX persona. If didn't get enough information or the user is not active or banned, return a message saying "Not enough information to generate a persona for this user."
Using the Reddit posts and comments below, generate a detailed structured user persona for **u/{username}** in the format below.

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

Interests & hobbies   
  - Writing style  
  - Ideologies and values  
  - Emotional tone and behavioral insights  
  - Likely profession or background

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

### Personality (on scale of number out of 5)
- Openness (4) - (1) Closed
- Introvert (2) - (3) Extrovert  
- Intuition (3) - (2) Sensing  
- Feeling (1) - (4) Thinking  
- Perceiving (5) - (0) Judging

---

### Behaviour & Habits
List 4–6 habits or observed behavioral patterns from their posts/comments. Each bullet should ideally link to a Reddit post.

---

### Frustrations
List 3–5 common pain points or issues they mention.

---

### Goals & Needs
List 3–5 things they seem to want or care about.

---

Use insights only from the user’s Reddit content below. **Cite Reddit URLs to justify your claims wherever possible**.

---

{data_block}
"""

    # ── 3. Send to Gemini-Pro ─────────────────────────────────────────────────
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # ── 4. Attach metadata ─────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata = f"""---
Username: u/{username}
Profile URL: https://www.reddit.com/user/{username}/
Posts Scraped: {len(posts)}
Comments Scraped: {len(comments)}
---

"""

    # ── 5. Return structured result ────────────────────────────────────────────
    return metadata + response.text
