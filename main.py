import customtkinter as ctk
from data_manager import VocaDataManager
from screens import ListPage, QuizPage, TestPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VocaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 백엔드 데이터 엔진 초기화
        self.db = VocaDataManager()
        self.editing_target = None 

        # 윈도우 창 설정
        self.title("My English Vocabulary App - Modular Edition")
        self.geometry("1150x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # 사이드바 레이아웃 구역
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar_frame, text="VOCA APP v3.5", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30, padx=20)

        self.btn_menu_list = ctk.CTkButton(self.sidebar_frame, text="📖 단어 및 예문 관리", font=ctk.CTkFont(size=15), fg_color="transparent", text_color="#f8fafc", hover_color="#1e293b", command=self.show_list_page, anchor="w", height=40)
        self.btn_menu_list.pack(fill="x", padx=10, pady=3)

        self.btn_menu_quiz = ctk.CTkButton(self.sidebar_frame, text="🧩 미니 연습 퀴즈", font=ctk.CTkFont(size=15), fg_color="transparent", text_color="#f8fafc", hover_color="#1e293b", command=self.show_quiz_page, anchor="w", height=40)
        self.btn_menu_quiz.pack(fill="x", padx=10, pady=3)

        self.btn_menu_test = ctk.CTkButton(self.sidebar_frame, text="💯 100문제 테스트", font=ctk.CTkFont(size=15), fg_color="transparent", text_color="#f8fafc", hover_color="#1e293b", command=self.show_test_page, anchor="w", height=40)
        self.btn_menu_test.pack(fill="x", padx=10, pady=3)

        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="#334155").pack(fill="x", padx=15, pady=20)
        ctk.CTkButton(self.sidebar_frame, text="📁 CSV 단어 가져오기", font=ctk.CTkFont(size=14), fg_color="#0284c7", hover_color="#0369a1", command=self.trigger_csv_import).pack(fill="x", padx=15, pady=10)

        # ==========================================
        # 메인 콘텐츠 컨테이너 구역
        # ==========================================
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 자식 화면 객체들을 컴포넌트 단위로 생성
        self.list_page = ListPage(self.container, self)
        self.quiz_page = QuizPage(self.container, self)
        self.test_page = TestPage(self.container, self)

        # 기본 페이지 활성화
        self.show_list_page()

    def show_list_page(self):
        self.quiz_page.grid_forget()
        self.test_page.grid_forget()
        self.list_page.grid(row=0, column=0, sticky="nsew")
        self.list_page.update_word_list()
        self._update_menu_styles(self.btn_menu_list)

    def show_quiz_page(self):
        self.list_page.grid_forget()
        self.test_page.grid_forget()
        self.quiz_page.grid(row=0, column=0, sticky="nsew")
        self.quiz_page.next_quiz()
        self._update_menu_styles(self.btn_menu_quiz)

    def show_test_page(self):
        self.list_page.grid_forget()
        self.quiz_page.grid_forget()
        self.test_page.grid(row=0, column=0, sticky="nsew")
        self.test_page.reset_test_ui()
        self._update_menu_styles(self.btn_menu_test)

    def _update_menu_styles(self, active_btn):
        for btn in [self.btn_menu_list, self.btn_menu_quiz, self.btn_menu_test]:
            if btn == active_btn:
                btn.configure(fg_color="#1e293b", text_color="#38bdf8")
            else:
                btn.configure(fg_color="transparent", text_color="#f8fafc")

    def trigger_csv_import(self):
        file_path = ctk.filedialog.askopenfilename(title="불러올 단어장 CSV 파일을 선택하세요", filetypes=[("CSV 파일", "*.csv")])
        if file_path:
            count = self.db.import_csv(file_path)
            self.list_page.update_word_list()
            self.list_page.status_label.configure(text=f"📊 CSV에서 {count}개 단어 동기화 완료!", text_color="#34d399")

if __name__ == "__main__":
    app = VocaApp()
    app.mainloop()