import requests

class WitClient:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.wit.ai/message"

    def message(self, text):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "q": text
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()
