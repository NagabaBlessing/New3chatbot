import os
import requests

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_reply(self, user_message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]
