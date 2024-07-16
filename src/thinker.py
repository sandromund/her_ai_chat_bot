import json
import os
import time

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
        think = config["Thinker"]["LMStudio"]
        self.base_url = think["base_url"]
        self.api_key = think["api_key"]
        self.model = think["model"]
        self.system_role = think["system_role"]
        self.temperature = think["temperature"]
        self.history_dir = think["history_dir"]
        self.personality_file = think["personality_file"]

        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.history = [{"role": "system", "content": self.system_role}]

    def run(self, prompt: str) -> str:
        self.history.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=self.temperature)
        message = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": message})
        return message

    def __get_most_recent_file(self):
        most_recent_file = None
        most_recent_time = 0
        for entry in os.scandir(self.history_dir):
            if entry.is_file():
                mod_time = entry.stat().st_mtime_ns
                if mod_time > most_recent_time:
                    most_recent_file = entry.name
                    most_recent_time = mod_time
        return os.path.join(self.history_dir, most_recent_file)

    def load_history(self):
        if len(os.listdir(self.history_dir)) < 1:
            return
        with open(self.__get_most_recent_file(), 'r') as file:
            self.history += json.load(file)

    def save_history(self):
        new_file_name = str(int(time.time())) + ".txt"
        with open(os.path.join(self.history_dir, new_file_name), 'w') as file:
            file.write(json.dumps(self.history))

    def load_personality(self):
        with open(self.personality_file, 'r') as file:
            personality_data = file.read()
        self.history += [{"role": "system", "content": personality_data}]
