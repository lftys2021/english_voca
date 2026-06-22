import json
import os

# 1. 현재 실행 중인 main.py 파일의 절대 경로를 구합니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. 그 폴더 경로 뒤에 "words.json"을 안전하게 결합합니다.
FILE_NAME = os.path.join(BASE_DIR, "words.json")

# 1. 파일에서 단어 데이터 불러오기
def load_data():
    # 파일이 존재하면 열어서 가져오고, 없으면 빈 딕셔너리 반환
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 2. 파일에 단어 데이터 저장하기
def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        # ensure_ascii=False를 해야 한글이 깨지지 않고 잘 저장됩니다.
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    # 단어를 저장할 빈 딕셔너리 생성
    voca_dict = {}

    while True:
        print("\n--- 나만의 영어 단어장 ---")
        print("1. 단어 등록")
        print("2. 전체 단어 보기")
        print("3. 단어 수정 🛠️")
        print("4. 단어 삭제 🛠️")
        print("5. 미니 퀴즈 🛠️")
        print("6. 종료")
        
        menu = input("원하는 메뉴 번호를 입력하세요: ")
        
        if menu == "1":
            eng = input("영어 단어를 입력하세요: ").strip()
            kor = input("한국어 뜻을 입력하세요: ").strip()

            # 딕셔너리에 추가 후 파일에 바로 저장
            voca_dict[eng] = kor
            save_data(voca_dict)
            print(f"🎉 '{eng}' 단어가 저장되었습니다.")

        elif menu == "2":
            print("\n=== 등록된 단어 목록 ===")
            if not voca_dict:
                print("등록된 단어가 없습니다.")
            else:
                for eng, kor in voca_dict.items():
                    print(f"📖 {eng} : {kor}")
        elif menu == "3":
            print("\n=== 단어 수정 ===")
            if not voca_dict:
                print("수정할 단어가 없습니다.")
                continue

            target = input("수정할 영어 단어를 입력하세요: ").strip()

            # 입력한 단어가 단어장에 존재하는지 확인
            if target in voca_dict:
                print(f"선택된 단어: {target} (현재 뜻: {voca_dict[target]})")
                sub_menu = input("[1] 단어 수정 [2] 취소: ")

                if sub_menu == "1":
                    new_kor = input("새로운 한국어 뜻을 입력하세요: ").strip()
                    voca_dict[target] = new_kor  # 덮어쓰기로 수정
                    save_data(voca_dict)
                    print(f"✏️ '{target}'의 뜻이 '{new_kor}'로 수정되었습니다.")

                else:
                    print("작업이 취소되었습니다.")

            else:
                print("❌ 단어장에 존재하지 않는 단어입니다.")

        elif menu == "4":
            print("\n=== 단어 삭제 ===")
            if not voca_dict:
                print("삭제할 단어가 없습니다.")
                continue
            
            target = input("삭제할 영어 단어를 입력하세요: ").strip()

            # 입력한 단어가 단어장에 존재하는지 확인
            if target in voca_dict:
                print(f"선택된 단어: {target} (현재 뜻: {voca_dict[target]})")
                sub_menu = input("[1] 단어 삭제 [2] 취소: ")

                if sub_menu == "1":
                    del voca_dict[target]  # 딕셔너리에서 삭제
                    save_data(voca_dict)
                    print(f"🗑️ '{target}' 단어가 삭제되었습니다.")

                else:
                    print("작업이 취소되었습니다.")

            else:
                print("❌ 단어장에 존재하지 않는 단어입니다.")

        elif menu == "5":
            print("프로그램을 종료합니다.")
            break
        elif menu == "4":
            print("\n=== 🎯 미니 퀴즈 시작 ===")
            # 단어장에 단어가 없으면 퀴즈를 진행할 수 없음
            if not voca_dict:
                print("퀴즈를 낼 단어가 없습니다. 먼저 단어를 등록해 주세요.")
                continue
            
            # 딕셔너리의 키(영어 단어)들만 모아서 리스트로 변환
            word_list = list(voca_dict.keys())
            # 리스트에서 무작위로 하나의 단어 선택
            quiz_word = random.choice(word_list)
            
            print(f"문제: '{quiz_word}'의 뜻은 무엇일까요?")
            user_answer = input("정답 입력: ").strip()
            
            # 사용자가 입력한 정답과 실제 뜻 비교
            if user_answer == voca_dict[quiz_word]:
                print("⭕ 정답입니다! 참 잘하셨어요! 🎉")
            else:
                print(f"❌ 틀렸습니다. 정답은 '{voca_dict[quiz_word]}'입니다. 🥲")
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()