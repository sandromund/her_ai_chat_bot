import requests


class Thinker:

    def __init__(self, url, model):
        self.url = url
        self.model = model

    def run(self, prompt: str) -> str:
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url, json=data).json()
        return response.get("response")
