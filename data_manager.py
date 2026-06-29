import os
import json
import csv
import random
from gtts import gTTS
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "words.json")

class VocaDataManager:
    def __init__(self):
        pygame.mixer.init()
        self.voca_dict = self.load_data()

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if data and isinstance(list(data.values())[0], str): return {}
                    return data
                except: return {}
        return {}

    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.voca_dict, f, ensure_ascii=False, indent=4)

    def speak_text(self, text):
        if not text or text.startswith("등록된 예문"): return
        try:
            tts = gTTS(text=text, lang='en')
            temp_file = os.path.join(BASE_DIR, "temp_voca.mp3")
            tts.save(temp_file)
            pygame.mixer.music.unload()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
        except: pass

    def import_csv(self, file_path):
        if not file_path: return 0
        count = 0
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if len(row) < 2: continue
                eng, kor = row[0].strip(), row[1].strip()
                ex_eng = row[2].strip() if len(row) > 2 else ""
                ex_kor = row[3].strip() if len(row) > 3 else ""
                if eng == "" or kor == "": continue
                self.voca_dict[eng] = {
                    "meaning": kor,
                    "example_eng": ex_eng if ex_eng else "등록된 예문이 없습니다.",
                    "example_kor": ex_kor if ex_kor else ""
                }
                count += 1
        self.save_data()
        return count