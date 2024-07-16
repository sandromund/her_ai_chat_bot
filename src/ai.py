from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError

from src.talker import Talker
from src.thinker import Thinker


class AI:

    def __init__(self, config):
        self.talk = Talker(model=config.get("talk_model"))
        self.listen = Recognizer()
        self.think = Thinker(
            model=config.get("think_model"),
            url=config.get("url"))

    def run(self):
        while True:
            print("listening ... ")
            try:
                with Microphone() as mic:
                    self.listen.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.listen.listen(mic)
                    text = self.listen.recognize_google(audio)
                    print(text)
                    if text in ["quite", "exit", "close"]:
                        break
                    ai_answer = self.think.run(prompt=text)
                    self.talk.run(ai_answer)
            except RequestError as e:
                print("Could not request results; {0}".format(e))
            except UnknownValueError:
                print("unknown error occurred")
