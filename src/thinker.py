import json
import logging
import os
import time

import requests
from openai import OpenAI


class Thinker:

    def run(self, prompt: str) -> str:
        pass

    def load(self):
        pass

    def save(self):
        pass

    def memorize(self):
        pass


class ThinkerOllama(Thinker):

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


class ThinkerLMStudio(Thinker):

    def __init__(self, config):
        think = config["Thinker"]["LMStudio"]
        self.base_url = think["base_url"]
        self.api_key = think["api_key"]
        self.model = think["model"]
        self.temperature: float = think["temperature"]
        self.history_dir = think["history_dir"]
        self.personality_file = think["personality_file"]
        self.do_load_history: bool = think["load_history"]
        self.do_load_memory: bool = think["load_memory"]
        self.history_buffer_size: int = think["history_buffer_size"]
        self.memory_dir = think["memory_dir"]
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.personality_data = []
        self.history = []
        self.memory = ""
        self.summarize_prompt = ""
        self.summarize_prompt_file = think["summarize_prompt"]
        self.memory_buffer = []

    def run(self, prompt: str) -> str:
        self.history.append({"role": "user", "content": prompt})
        history_buffer = self.history[-self.history_buffer_size:]
        history_buffer = self.personality_data + history_buffer
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=history_buffer,
            temperature=self.temperature)
        message = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": message})
        self.memory_buffer.append({"role": "user", "content": prompt})
        self.memory_buffer.append({"role": "assistant", "content": message})
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

    def load_memory(self):
        if not self.do_load_memory:
            return
        if len(os.listdir(self.memory_dir)) < 1:
            return
        file = self.__get_most_recent_file()
        logging.info("Loading memories in %s", file)
        with open(file, 'r') as file:
            self.memory += file.read()

    def load_summarize_prompt(self):
        if not os.path.isfile(self.summarize_prompt_file):
            self.summarize_prompt = \
                "Summarize the following chat history capturing the key points and important details:"
        logging.info("Loading summarize prompt from %s", self.summarize_prompt_file)
        with open(self.summarize_prompt_file, 'r') as file:
            self.summarize_prompt = file.read()

    def load(self):
        self.load_history()
        self.load_personality()
        self.load_memory()
        self.load_summarize_prompt()

    def save_history(self, new_file_name=None):
        if new_file_name is None:
            new_file_name = str(int(time.time())) + ".txt"
        with open(os.path.join(self.history_dir, new_file_name), 'w') as file:
            file.write(json.dumps(self.history))

    def save_memory(self, new_file_name=None):
        if new_file_name is None:
            new_file_name = str(int(time.time())) + ".txt"
        with open(os.path.join(self.memory_dir, new_file_name), 'w') as file:
            file.write(self.memory)
        self.memory_buffer = []

    def save(self):
        new_file_name = str(int(time.time())) + ".txt"
        self.save_history(new_file_name=new_file_name)
        self.memorize(exit_mode=True)

    def load_personality(self):
        if not os.path.isfile(self.personality_file):
            return
        with open(self.personality_file, 'r') as file:
            personality_data = file.read()
        self.personality_data = [{"role": "system", "content": personality_data}]

    def summarize_chat(self):
        sys = [{"role": "system", "content": self.summarize_prompt}]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=sys + self.memory_buffer,
            temperature=self.temperature)
        self.memory = completion.choices[0].message.content
        print(self.summarize_prompt)
        print(self.memory)

    def memorize(self, exit_mode: bool = False):
        if not exit_mode or len(self.memory_buffer) >= self.history_buffer_size:
            return
        self.summarize_chat()
        self.save_memory()
