from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError
import speech_recognition as sr

from src.talker import Talker
from src.thinker import ThinkerLMStudio as Thinker


class AI:

    def __init__(self, config):
        self.talk = Talker(config)
        self.listen = Recognizer()
        self.think = Thinker(config)
        self.device_index = config["Recognizer"]["microphone_device_index"]

    def run(self):
        mics = {}
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            mics[index] = name
            print(index, "->", name)
        self.think.load()
        while True:
            try:
                with Microphone(device_index=self.device_index) as mic:
                    print(f"listening ... ({mics.get(mic.device_index)})")
                    self.listen.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.listen.listen(mic)
                    user_text = self.listen.recognize_google(audio)
                    print(user_text)
                    if user_text in ["quit", "exit", "close"]:
                        self.think.save()
                        break
                    ai_answer = self.think.run(prompt=user_text)
                    print(ai_answer)
                    self.talk.run(ai_answer)
            except RequestError as e:
                print("Could not request results; {0}".format(e))
            except UnknownValueError:
                continue
