import customtkinter as ctk
import random

# ==========================================
# [화면 1] 단어 및 예문 관리 UI
# ==========================================
class ListPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_panel = ctk.CTkFrame(self, fg_color="transparent")
        top_panel.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        self.input_frame = ctk.CTkFrame(top_panel, corner_radius=10)
        self.input_frame.pack(fill="x", pady=5)
        
        row1 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        self.entry_eng = ctk.CTkEntry(row1, placeholder_text="영어 단어 입력", width=200)
        self.entry_eng.pack(side="left", padx=5, pady=5)
        
        self.entry_kor = ctk.CTkEntry(row1, placeholder_text="한국어 뜻 입력", width=200)
        self.entry_kor.pack(side="left", padx=5, pady=5)
        
        self.btn_submit = ctk.CTkButton(row1, text="추가하기", command=self.handle_submit, width=90)
        self.btn_submit.pack(side="left", padx=5, pady=5)

        self.btn_cancel = ctk.CTkButton(row1, text="취소", fg_color="#64748b", hover_color="#475569", command=self.cancel_edit, width=50)
        
        self.status_label = ctk.CTkLabel(row1, text="", text_color="#38bdf8")
        self.status_label.pack(side="left", padx=15)

        row2 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        self.entry_ex_eng = ctk.CTkEntry(row2, placeholder_text="영어 예문 입력", width=410)
        self.entry_ex_eng.pack(side="left", padx=5, pady=5)
        
        self.entry_ex_kor = ctk.CTkEntry(row2, placeholder_text="예문 해석 입력", width=410)
        self.entry_ex_kor.pack(side="left", padx=5, pady=5)

        search_frame = ctk.CTkFrame(top_panel, corner_radius=10)
        search_frame.pack(fill="x", pady=5)
        
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="🔍 검색할 단어, 뜻, 또는 예문을 입력하세요...", width=500)
        self.entry_search.pack(fill="x", padx=15, pady=10)
        self.entry_search.bind("<KeyRelease>", self.filter_words)

        self.list_frame = ctk.CTkScrollableFrame(self, label_text="나의 풍성한 단어장 목록")
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.update_word_list()

    def handle_submit(self):
        eng, kor = self.entry_eng.get().strip(), self.entry_kor.get().strip()
        ex_eng, ex_kor = self.entry_ex_eng.get().strip(), self.entry_ex_kor.get().strip()
        if eng == "" or kor == "":
            self.status_label.configure(text="⚠️ 단어와 뜻은 필수 입력입니다.", text_color="#f87171")
            return
        word_data = {"meaning": kor, "example_eng": ex_eng if ex_eng else "등록된 예문이 없습니다.", "example_kor": ex_kor if ex_kor else ""}
        if self.app.editing_target:
            if self.app.editing_target != eng: del self.db.voca_dict[self.app.editing_target]
            self.db.voca_dict[eng] = word_data
            self.status_label.configure(text=f"✏️ '{eng}' 수정 완료!", text_color="#38bdf8")
            self.cancel_edit()
        else:
            self.db.voca_dict[eng] = word_data
            self.status_label.configure(text=f"🎉 '{eng}' 저장 완료!", text_color="#34d399")
            self.entry_eng.delete(0, 'end'); self.entry_kor.delete(0, 'end')
            self.entry_ex_eng.delete(0, 'end'); self.entry_ex_kor.delete(0, 'end')
        self.db.save_data(); self.entry_search.delete(0, 'end'); self.update_word_list()

    def start_edit(self, eng, data):
        self.app.editing_target = eng
        self.entry_eng.delete(0, 'end'); self.entry_eng.insert(0, eng)
        self.entry_kor.delete(0, 'end'); self.entry_kor.insert(0, data["meaning"])
        self.entry_ex_eng.delete(0, 'end'); self.entry_ex_eng.insert(0, data["example_eng"])
        self.entry_ex_kor.delete(0, 'end'); self.entry_ex_kor.insert(0, data["example_kor"])
        self.btn_submit.configure(text="수정완료", fg_color="#eab308", hover_color="#ca8a04")
        self.btn_cancel.pack(side="left", padx=5, pady=5)

    def cancel_edit(self):
        self.app.editing_target = None
        self.entry_eng.delete(0, 'end'); self.entry_kor.delete(0, 'end')
        self.entry_ex_eng.delete(0, 'end'); self.entry_ex_kor.delete(0, 'end')
        self.btn_submit.configure(text="추가하기", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.btn_cancel.pack_forget(); self.status_label.configure(text="")

    def delete_word(self, eng):
        if eng in self.db.voca_dict:
            del self.db.voca_dict[eng]
            self.db.save_data()
            if self.app.editing_target == eng: self.cancel_edit()
            self.update_word_list()

    def filter_words(self, event):
        search_keyword = self.entry_search.get().strip().lower()
        for widget in self.list_frame.winfo_children(): widget.destroy()
        for eng, data in self.db.voca_dict.items():
            if (search_keyword in eng.lower() or search_keyword in data["meaning"].lower() or 
                search_keyword in data["example_eng"].lower() or search_keyword in data["example_kor"]):
                self.create_word_row(eng, data)

    def create_word_row(self, eng, data):
        item_card = ctk.CTkFrame(self.list_frame, corner_radius=8)
        item_card.pack(fill="x", padx=10, pady=6)
        text_subframe = ctk.CTkFrame(item_card, fg_color="transparent")
        text_subframe.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        lbl_word = ctk.CTkLabel(text_subframe, text=f"📖  {eng}  :  {data['meaning']}", font=ctk.CTkFont(size=17, weight="bold"), anchor="w")
        lbl_word.pack(fill="x")
        ex_text = f"💡 Ex: {data['example_eng']} ({data['example_kor']})" if data['example_kor'] else f"💡 Ex: {data['example_eng']}"
        lbl_ex = ctk.CTkLabel(text_subframe, text=ex_text, font=ctk.CTkFont(size=13), text_color="#94a3b8", anchor="w")
        lbl_ex.pack(fill="x", pady=(3, 0))
        btn_subframe = ctk.CTkFrame(item_card, fg_color="transparent")
        btn_subframe.pack(side="right", padx=10)
        
        btn_speak_w = ctk.CTkButton(btn_subframe, text="🔊 단어", width=60, height=26, fg_color="#10b981", hover_color="#059669", command=lambda e=eng: self.db.speak_text(e))
        btn_speak_w.pack(side="left", padx=3)
        btn_speak_e = ctk.CTkButton(btn_subframe, text="🗣️ 예문", width=60, height=26, fg_color="#8b5cf6", hover_color="#6d28d9", command=lambda ex=data['example_eng']: self.db.speak_text(ex))
        btn_speak_e.pack(side="left", padx=3)
        btn_edit = ctk.CTkButton(btn_subframe, text="수정", width=45, height=26, fg_color="#3b82f6", hover_color="#2563eb", command=lambda e=eng, d=data: self.start_edit(e, d))
        btn_edit.pack(side="left", padx=3)
        btn_del = ctk.CTkButton(btn_subframe, text="삭제", width=45, height=26, fg_color="#ef4444", hover_color="#dc2626", command=lambda e=eng: self.delete_word(e))
        btn_del.pack(side="left", padx=3)

    def update_word_list(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        for eng, data in self.db.voca_dict.items(): self.create_word_row(eng, data)


# ==========================================
# [화면 2] 미니 연습 퀴즈 UI
# ==========================================
class QuizPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.quiz_correct_answer = ""

        self.grid_columnconfigure(0, weight=1)
        quiz_title = ctk.CTkLabel(self, text="🧠 미니 단어 퀴즈 (무한 연습)", font=ctk.CTkFont(size=26, weight="bold"))
        quiz_title.pack(pady=20)

        self.quiz_card = ctk.CTkFrame(self, width=600, height=400, corner_radius=15)
        self.quiz_card.pack(pady=10, padx=50, fill="both", expand=True)

        self.lbl_question = ctk.CTkLabel(self.quiz_card, text="문제를 불러오는 중입니다...", font=ctk.CTkFont(size=22, weight="bold"), text_color="#38bdf8")
        self.lbl_question.pack(pady=30)

        self.lbl_quiz_hint = ctk.CTkLabel(self.quiz_card, text="", font=ctk.CTkFont(size=16, slant="italic"), text_color="#94a3b8")
        self.lbl_quiz_hint.pack(pady=5)

        self.entry_quiz_ans = ctk.CTkEntry(self.quiz_card, placeholder_text="한국어 뜻을 입력하고 엔터를 누르세요", width=350, font=ctk.CTkFont(size=16))
        self.entry_quiz_ans.pack(pady=15)
        self.entry_quiz_ans.bind("<Return>", lambda e: self.check_quiz_answer())

        btn_frame = ctk.CTkFrame(self.quiz_card, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="정답 확인", width=120, command=self.check_quiz_answer).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="다음 문제 ➡️", width=120, fg_color="#10b981", hover_color="#059669", command=self.next_quiz).pack(side="left", padx=10)

        self.lbl_quiz_feedback = ctk.CTkLabel(self.quiz_card, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_quiz_feedback.pack(pady=15)

    def next_quiz(self):
        self.entry_quiz_ans.delete(0, 'end')
        self.lbl_quiz_feedback.configure(text="")
        if not self.db.voca_dict:
            self.lbl_question.configure(text="⚠️ 등록된 단어가 없습니다!")
            self.entry_quiz_ans.configure(state="disabled")
            return
        self.entry_quiz_ans.configure(state="normal")
        random_eng = random.choice(list(self.db.voca_dict.keys()))
        target_data = self.db.voca_dict[random_eng]
        self.quiz_correct_answer = target_data["meaning"]
        self.lbl_question.configure(text=f"Q. 다음 단어의 뜻은 무엇일까요?\n\n[  {random_eng}  ]")
        blank_sentence = target_data["example_eng"].replace(random_eng, " ______ ")
        self.lbl_quiz_hint.configure(text=f"Hint (Sentence): {blank_sentence}")
        self.db.speak_text(random_eng)

    def check_quiz_answer(self):
        user_ans = self.entry_quiz_ans.get().strip()
        if user_ans == "": return
        if user_ans in self.quiz_correct_answer or self.quiz_correct_answer in user_ans:
            self.lbl_quiz_feedback.configure(text=f"⭕ 정답입니다!\n(저장된 뜻: {self.quiz_correct_answer})", text_color="#34d399")
        else:
            self.lbl_quiz_feedback.configure(text=f"❌ 틀렸습니다! 다시 맞혀보세요.", text_color="#f87171")


# ==========================================
# [화면 3] 100문제 테스트 모드 UI
# ==========================================
class TestPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        
        self.test_queue = []
        self.test_total_count = 0
        self.test_current_idx = 0
        self.test_score = 0

        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="💯 실전! 100문제 테스트 모드", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=20)

        self.test_card = ctk.CTkFrame(self, width=650, height=450, corner_radius=15)
        self.test_card.pack(pady=10, padx=50, fill="both", expand=True)

        self.lbl_test_progress = ctk.CTkLabel(self.test_card, text="준비 완료", font=ctk.CTkFont(size=16, weight="bold"), text_color="#a8a29e")
        self.lbl_test_progress.pack(pady=15)

        self.lbl_test_question = ctk.CTkLabel(self.test_card, text="시작 버튼을 누르면 시험이 시작됩니다.", font=ctk.CTkFont(size=24, weight="bold"), text_color="#38bdf8")
        self.lbl_test_question.pack(pady=30)

        self.lbl_test_hint = ctk.CTkLabel(self.test_card, text="", font=ctk.CTkFont(size=15, slant="italic"), text_color="#94a3b8")
        self.lbl_test_hint.pack(pady=5)

        self.entry_test_ans = ctk.CTkEntry(self.test_card, placeholder_text="뜻을 입력하고 엔터를 누르세요", width=350, font=ctk.CTkFont(size=16), state="disabled")
        self.entry_test_ans.pack(pady=20)
        self.entry_test_ans.bind("<Return>", lambda e: self.submit_test_answer())

        self.btn_test_action = ctk.CTkButton(self.test_card, text="🚀 시험 시작하기", width=180, height=40, font=ctk.CTkFont(size=16, weight="bold"),
                                             fg_color="#10b981", hover_color="#059669", command=self.start_test_session)
        self.btn_test_action.pack(pady=20)

    def reset_test_ui(self):
        self.lbl_test_progress.configure(text="준비 완료")
        self.lbl_test_question.configure(text="시작 버튼을 누르면 시험이 시작됩니다.\n(최대 100문제가 무작위 셔플링되어 출제됩니다.)", text_color="#38bdf8")
        self.lbl_test_hint.configure(text="")
        self.entry_test_ans.delete(0, 'end')
        self.entry_test_ans.configure(state="disabled")
        self.btn_test_action.configure(text="🚀 시험 시작하기", fg_color="#10b981", hover_color="#059669", state="normal", command=self.start_test_session)

    def start_test_session(self):
        if not self.db.voca_dict:
            self.lbl_test_question.configure(text="⚠️ 등록된 단어가 없습니다!", text_color="#f87171")
            return
        all_words = list(self.db.voca_dict.keys())
        sample_size = min(100, len(all_words))
        self.test_queue = random.sample(all_words, sample_size)
        self.test_total_count = sample_size
        self.test_current_idx = 0
        self.test_score = 0

        self.entry_test_ans.configure(state="normal")
        self.btn_test_action.configure(text="➡️ 정답 제출 후 다음", fg_color="#3b82f6", hover_color="#2563eb", command=self.submit_test_answer)
        self.load_next_test_question()

    def load_next_test_question(self):
        self.entry_test_ans.delete(0, 'end')
        self.entry_test_ans.focus()
        if self.test_current_idx < self.test_total_count:
            self.lbl_test_progress.configure(text=f"📝 문제 {self.test_current_idx + 1} / {self.test_total_count}")
            current_word = self.test_queue[self.test_current_idx]
            self.lbl_test_question.configure(text=f"Q. 다음 단어의 뜻은?\n\n[  {current_word}  ]")
            blank_sentence = self.db.voca_dict[current_word]["example_eng"].replace(current_word, " ______ ")
            self.lbl_test_hint.configure(text=f"Hint: {blank_sentence}")
            self.db.speak_text(current_word)
        else:
            self.show_test_result()

    def submit_test_answer(self):
        if self.test_current_idx >= self.test_total_count: return
        user_ans = self.entry_test_ans.get().strip()
        if user_ans == "": return
        
        current_word = self.test_queue[self.test_current_idx]
        correct_meaning = self.db.voca_dict[current_word]["meaning"]
        if user_ans in correct_meaning or correct_meaning in user_ans:
            self.test_score += 1
            
        self.test_current_idx += 1
        self.load_next_test_question()

    def show_test_result(self):
        self.entry_test_ans.configure(state="disabled")
        self.lbl_test_progress.configure(text="🏁 TEST FINISHED")
        final_percentage = int((self.test_score / self.test_total_count) * 100)
        
        if final_percentage >= 90: grade_msg = "👑 완벽합니다! 원어민이시군요!"; color = "#34d399"
        elif final_percentage >= 70: grade_msg = "👍 훌륭한 실력입니다."; color = "#60a5fa"
        else: grade_msg = "📚 복습이 조금 더 필요해요!"; color = "#f87171"

        self.lbl_test_question.configure(text=f"✨ 시험 결과 리포트 ✨\n\n맞힌 개수: {self.test_score} / {self.test_total_count}\n최종 점수: {final_percentage}점\n\n{grade_msg}", text_color=color)
        self.lbl_test_hint.configure(text="")
        self.btn_test_action.configure(text="🔄 다시 도전하기", fg_color="#8b5cf6", hover_color="#6d28d9", command=self.reset_test_ui)