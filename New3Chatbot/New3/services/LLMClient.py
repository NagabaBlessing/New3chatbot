import os
import requests


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.url = "https://api.groq.com/openai/v1/chat/completions"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_reply(self, user_message: str) -> str:
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.7,
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=30,
        )

        # 🔍 Helpful debugging
        if response.status_code != 200:
            raise Exception(
                f"Groq error {response.status_code}: {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
