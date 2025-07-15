# utils.py
# code for saving the output files in txt file
import os

def extract_username(url):
    return url.rstrip('/').split('/')[-1]

def save_output(username, persona_text):
    os.makedirs("persona_output", exist_ok=True)
    path = f"persona_output/{username}_persona.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(persona_text)
