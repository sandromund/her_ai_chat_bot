import pygame as pg
import torch
from TTS.api import TTS


class Talker:

    def __init__(self, model):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.file_path = "output.wav"
        self.tts = TTS(model_name=model, progress_bar=False).to(self.device)

    def __play_audio(self):
        pg.mixer.init()
        pg.mixer.music.load(self.file_path)
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            pass
        pg.mixer.music.stop()
        pg.mixer.quit()

    def run(self, text):
        self.tts.tts_to_file(text=text, file_path=self.file_path)
        self.__play_audio()
