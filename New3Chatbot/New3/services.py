
from typing import Optional, Dict, Any


# services.py
import requests
import os
from typing import Optional, Dict, Any

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_reply(self, message: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": message},
            ],
        }

        r = requests.post(self.url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
