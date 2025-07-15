# main.py

from reddit_scrapper import scrape_user_data
from persona_generator import generate_persona
from utils import save_output, extract_username

def main():
    url = input("Enter Reddit user profile URL: ").strip()
    username = extract_username(url)

    print(f"[+] Scraping data for user: {username}")
    posts, comments = scrape_user_data(username)

    print(f"[+] Generating persona...")
    persona = generate_persona(posts, comments, username)

    print(f"[+] Saving persona to file...")
    save_output(username, persona)

    print(f"[✓] Done! Persona saved as 'persona_output/{username}_persona.txt'.")

if __name__ == "__main__":
    main()
