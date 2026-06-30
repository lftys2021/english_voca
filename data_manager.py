import os
import json
import csv
from gtts import gTTS
import pygame
import requests

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
    
    def crawl_naver_dict(self, word):
        """네이버 사전 API를 통해 단어의 뜻과 예문을 보다 안정적으로 크롤링합니다."""
        if not word:
            return None
            
        try:
            # range=word 조건을 빼고 검색 범위를 넓혀 안정성을 확보합니다.
            search_url = f"https://en.dict.naver.com/api3/enko/search?query={word}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(search_url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                return None
                
            res_data = response.json()
            
            # 1. 단어 정보 구역(searchResultMap -> searchResultListMap -> WORD) 접근
            search_list_map = res_data.get("searchResultMap", {}).get("searchResultListMap", {})
            if not search_list_map or "WORD" not in search_list_map:
                return None
                
            word_items = search_list_map["WORD"].get("items", [])
            if not word_items:
                return None
                
            # 가장 매칭 확률이 높은 첫 번째 아이템 선택
            target_item = word_items[0]
            
            # 2. 뜻(Meaning) 추출 가공
            means_collector = target_item.get("meansCollector", [])
            means_list = []
            for m in means_collector:
                if m.get("name"):
                    # html 태그 혹시 모를 제거
                    clean_mean = m["name"].replace("<b>", "").replace("</b>", "").strip()
                    means_list.append(clean_mean)
            
            if not means_list:
                return None
                
            meaning = ", ".join(means_list)
            
            # 3. 예문(Example) 추출 가공
            example_eng = "등록된 예문이 없습니다."
            example_kor = ""
            
            example_group = target_item.get("exampleGroup", [])
            if example_group and len(example_group) > 0:
                example_list = example_group[0].get("exampleList", [])
                if example_list:
                    first_ex = example_list[0]
                    # 태그 및 불필요한 공백 제거 가공
                    example_eng = first_ex.get("exampleSentence", "").replace("<b>", "").replace("</b>", "").strip()
                    example_kor = first_ex.get("exampleTranslate", "").strip()
            
            # 💡 만약 예문 그룹이 비어있다면, JSON 내 다른 예문 구조(meansCollector 안쪽 등)를 재탐색
            if example_eng == "등록된 예문이 없습니다." and len(means_collector) > 0:
                for m in means_collector:
                    if m.get("exampleGroup"):
                        ex_list = m["exampleGroup"][0].get("exampleList", [])
                        if ex_list:
                            example_eng = ex_list[0].get("exampleSentence", "").replace("<b>", "").replace("</b>", "").strip()
                            example_kor = ex_list[0].get("exampleTranslate", "").strip()
                            break

            return {
                "meaning": meaning,
                "example_eng": example_eng,
                "example_kor": example_kor
            }
            
        except Exception as e:
            print(f"네이버 사전 API 연동 실패 원인: {e}")
            return None