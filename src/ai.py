from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError

from src.talker import Talker
from src.thinker import ThinkerLMStudio as Thinker


class AI:

    def __init__(self, config):
        self.talk = Talker(config)
        self.listen = Recognizer()
        self.think = Thinker(config)

    def run(self):
        self.think.load_history()
        self.think.load_personality()
        while True:
            print("listening ... ")
            try:
                with Microphone() as mic:
                    self.listen.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.listen.listen(mic)
                    text = self.listen.recognize_google(audio)
                    print(text)
                    if text in ["quit", "exit", "close"]:
                        self.think.save_history()
                        break
                    ai_answer = self.think.run(prompt=text)
                    print(ai_answer)
                    ai_answer_filtered = ai_answer.split("###")[0]
                    self.talk.run(ai_answer_filtered)
            except RequestError as e:
                print("Could not request results; {0}".format(e))
            except UnknownValueError:
                continue
