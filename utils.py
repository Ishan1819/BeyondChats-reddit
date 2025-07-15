"""utils.py

Utility functions for extracting usernames and saving persona output to files.
"""

import os


def extract_username(url: str) -> str:
    """
    Extract the Reddit username from a full Reddit profile URL.

    Parameters
    ----------
    url : str
        Reddit profile URL (e.g., https://www.reddit.com/user/username/)

    Returns
    -------
    str
        Extracted Reddit username.
    """
    return url.rstrip("/").split("/")[-1]


def save_output(username: str, persona_text: str) -> None:
    """
    Save the generated persona text to a file inside 'persona_output/'.

    Parameters
    ----------
    username : str
        Reddit username used to name the output file.

    persona_text : str
        The persona content to be written to file.
    """
    os.makedirs("persona_output", exist_ok=True)
    path = f"persona_output/{username}_persona.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(persona_text)
