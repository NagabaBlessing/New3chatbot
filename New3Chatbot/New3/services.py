import requests
from typing import Optional, Dict, Any


class WitClient:
    """
    Minimal Wit.ai connection wrapper.

    - Uses requests.Session for connection reuse
    - Adds Authorization header (Bearer token) and Accept
    - Handles API versioning via 'v' query parameter
    - Exposes send_text() for GET /message?q=... and send_speech() for POST /speech
    """

    def __init__(
        self,
        token: str,
        api_version: str = "20240101",
        base_url: str = "https://api.wit.ai",
        timeout: float = 10.0,
    ) -> None:
        if not token:
            raise ValueError("Wit.ai token is required")
        self.token = token
        self.api_version = api_version
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            }
        )

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def send_text(self, message: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call GET /message?q=...
        Returns parsed JSON response.
        """
        if not isinstance(message, str):
            raise ValueError("message must be a string")

        url = self._build_url("message")
        query = {"v": self.api_version, "q": message}
        if params:
            query.update(params)

        resp = self.session.get(url, params=query, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def send_speech(
        self,
        audio_bytes: bytes,
        content_type: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Call POST /speech with raw audio bytes.

        content_type examples:
          - "audio/wav"
          - "audio/mpeg"
          - or more specific low-level descriptors required by some Wit setups

        Returns parsed JSON response.
        """
        if not content_type:
            raise ValueError("content_type is required")

        url = self._build_url("speech")
        query = {"v": self.api_version}
        if params:
            query.update(params)

        headers = {"Content-Type": content_type}
        resp = self.session.post(
            url, params=query, data=audio_bytes, headers=headers, timeout=self.timeout
        )
        resp.raise_for_status()
        # The speech endpoint returns JSON with intent/entities
        return resp.json()

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()

    def __enter__(self) -> "WitClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


# Example usage (for local testing; remove or adapt in production code):
# if __name__ == "__main__":
#     import os
#     client = WitClient(token=os.getenv("WIT_TOKEN"))
#     print(client.send_text("hello"))
#     # with open("speech.wav", "rb") as f:
#     #     print(client.send_speech(f.read(), "audio/wav"))
import os

def ask_wit_ai(message: str):
    """
    Simple helper used by Django views.
    """
    token = os.getenv("WIT_TOKEN")
    if not token:
        raise RuntimeError("WIT_TOKEN environment variable not set")

    client = WitClient(token=token)
    try:
        return client.send_text(message)
    finally:
        client.close()
