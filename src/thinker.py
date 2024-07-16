import requests
from openai import OpenAI


class ThinkerOllama:

    def __init__(self, config):
        self.url = config["Thinker"]["Ollama"]["url"]
        self.model = config["Thinker"]["Ollama"]["model"]

    def run(self, prompt: str) -> str:
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url, json=data).json()
        return response.get("response")


class ThinkerLMStudio:

    def __init__(self, config):
        self.base_url = config["Thinker"]["LMStudio"]["base_url"]
        self.api_key = config["Thinker"]["LMStudio"]["api_key"]
        self.model = config["Thinker"]["LMStudio"]["model"]
        self.system_role = config["Thinker"]["LMStudio"]["system_role"]
        self.temperature = config["Thinker"]["LMStudio"]["temperature"]
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def run(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_role},
                {"role": "user", "content": prompt}],
            temperature=self.temperature)
        return completion.choices[0].message.content
