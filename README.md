# Reddit Persona Generator

This project scrapes a Reddit user's public posts and comments, analyzes their content, and generates a detailed psychological persona using **Google Gemini 1.5-flash**. The public user accounts gets the persona created for them but the ones that are banned, private or deleted from reddit could not be accessed and thus no personas could be created for them. The outputs for the user personas will get save in persona_output in the same folder.

> Example use cases:
 - Behavioral research
 - Social media analysis
 - UX design personas
 - User profiling in startups or academic studies

---

## Features

- Scrapes **latest submissions and comments** from any public Reddit user
- Sends data to **Google Gemini (1.5 Flash)** for persona generation
- Output includes:
  - Interests & hobbies  
  - Quotes
  - Motivations
  - Frustrations
  - Goals and needs
  - Personality traits  
  - Writing style  
  - Ideologies and values  
  - Emotional tone and behavioral insights  
  - Likely profession or background
- Automatically adds metadata: username, post/comment count

---

## Requirements

- Python 3.11.13
- Reddit Developer Account (to get client_id and client_secret)
- Google Generative AI API Key

---

## Installation
# Clone this repository 
git clone https://github.com/Ishan1819/BeyondChats-reddit.git

# Create a conda environment (optional but recommended)(Needs anaconda prompt downloaded)
- conda create -n reddit python=3.11
- conda activate reddit  

# Install dependencies
pip install -r requirements.txt

# Create .env file                                 (OPTIONAL: Only change the api key by creating one)
REDDIT_CLIENT_ID=your_reddit_client_id             (We get this by creating new user account and find there or keep it same)
REDDIT_CLIENT_SECRET=your_reddit_client_secret     (We get this by creating new user accound and find there or keep it same)
REDDIT_USER_AGENT=your_custom_user_agent           (We can put on your own or keep it same)
GEMINI_API_KEY=your_google_generativeai_key        (Generate new api key from https://aistudio.google.com/apikey)

# Run the code (in command prompt)
python main.py


