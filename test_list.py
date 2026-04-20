import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

with open("models.txt", "w") as f:
    for m in client.models.list():
        if 'embed' in m.name.lower() or 'embedContent' in getattr(m, 'supported_actions', []):
            f.write(f"{m.name}\n")
