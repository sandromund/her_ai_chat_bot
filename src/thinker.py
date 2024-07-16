import json
import logging
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

        self.temperature: float = think["temperature"]
        self.history_dir = think["history_dir"]
        self.personality_file = think["personality_file"]
        self.do_load_history: bool = think["load_history"]
        self.history_buffer_size: int = think["history_buffer_size"]
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.system_role = [{"role": "system", "content": think["system_role"]}]
        self.personality_data = []
        self.history = []

    def run(self, prompt: str) -> str:
        self.history.append({"role": "user", "content": prompt})
        history_buffer = self.history[-self.history_buffer_size:]
        history_buffer = self.system_role + self.personality_data + history_buffer
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=history_buffer,
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
        if not self.do_load_history:
            return
        if len(os.listdir(self.history_dir)) < 1:
            return
        file = self.__get_most_recent_file()
        logging.info("Loading history in %s", file)
        with open(file, 'r') as file:
            self.history += json.load(file)

    def save_history(self):
        new_file_name = str(int(time.time())) + ".txt"
        with open(os.path.join(self.history_dir, new_file_name), 'w') as file:
            file.write(json.dumps(self.history))

    def load_personality(self):
        if not os.path.isfile(self.personality_file):
            return
        with open(self.personality_file, 'r') as file:
            personality_data = file.read()
        self.personality_data = [{"role": "system", "content": personality_data}]
