import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from PIL import Image, ImageTk
import createDB


# Создание подключения к БД и создание БД
db = createDB.Database()
db.create_table_user_and_results()


class PersonalityTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тест на определение типа личности")
        self.geometry("1108x404")
        self.resizable(False, False)

        self.pages = []
        self.current_page = 0
        self.results = []
        self.selected_answer = tk.IntVar()  # Переменная для выбранного ответа
        self.load_questions()  # Загрузка вопросов из файла
        self.create_name_page()  # Создание страницы с вводом имени и фамилии
        self.name = ""  # Добавляем переменную для хранения имени пользователя

    def set_background_image(self, image_path):
        # Установка фонового изображения
        image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(image)

        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        background_label.lower()

    def load_questions(self):
        # Загрузка вопросов из файла testQuestionsAndAnswers.json
        with open("testQuestionsAndAnswers.json", "r", encoding="utf-8") as file:
            self.questions = json.load(file)

    def create_name_page(self):
        # Создание страницы с вводом имени и фамилии
        self.background_frame = tk.Frame(self)
        self.background_frame.pack(pady=20)

        self.set_background_image("./back.jpg")  # Установка фонового изображения

        background_label = tk.Label(self.background_frame, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        content_frame = tk.Frame(self.background_frame, bg='#FF1493')
        content_frame.pack(pady=20)

        self.name_label = tk.Label(content_frame, text="Введите имя и фамилию:", background='#FF1493')
        self.name_label.pack()

        self.name_entry = tk.Entry(content_frame)
        self.name_entry.pack(pady=10)

        self.start_button = tk.Button(content_frame, text="Начать тест", command=self.start_test,  bg="#B698B8")
        self.start_button.pack()

    def create_question_page(self):
        # Создание страницы с вопросом и вариантами ответов
        self.question_frame = tk.Frame(self, bg='#E0FFFF')
        self.question_frame.pack(pady=20)

        self.question_number_label = tk.Label(self.question_frame, text="Вопрос {}/{}".format(self.current_page + 1, len(self.questions)), bg='#E0FFFF')
        self.question_number_label.pack()

        self.question_label = tk.Label(self.question_frame, text=self.questions[self.current_page]["question"], bg='#E0FFFF')
        self.question_label.pack()

        self.answers_frame = tk.Frame(self.question_frame, bg='#E0FFFF')
        self.answers_frame.pack(pady=10)

        for answer in self.questions[self.current_page]["answer"]:
            # Создание радиокнопок для вариантов ответов
            answer_radio = tk.Radiobutton(self.answers_frame, text=answer, value=len(self.answers_frame.winfo_children()), variable=self.selected_answer, bg='#E0FFFF')
            answer_radio.pack(anchor="w")

        self.next_button = tk.Button(self.question_frame, text="Далее", command=self.validate_answer, bg='#E0FFFF')  
        self.next_button.pack(pady=10)
        
    def create_result_page(self):
    # Создание страницы с результатами
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=20)
        personality_type, result_values = self.who_are_you(self.results)
        result_label_text = "Результаты: {}".format(personality_type[0])
        self.result_label = tk.Label(self.result_frame, text=result_label_text)
        self.result_label.pack()

        self.result_text = tk.Text(self.result_frame, width=70, height=20)
        self.result_text.pack(pady=10)

        # Вставка имени пользователя и результата в БД
        name = self.name  # Получаем имя пользователя из сохраненной переменной
        db.insert_info(name, personality_type[0], personality_type[1], result_values[0], result_values[1], result_values[2], result_values[3])
        

    def start_test(self):
        # Начало теста
        name = self.name_entry.get()
        if name.strip() == "":
            # Проверка на заполнение имени и фамилии
            messagebox.showwarning("Ошибка", "Введите имя и фамилию")
            return
        
        self.name = name  # Сохраняем имя пользователя

        self.background_frame.destroy()
        self.create_question_page()
        self.selected_answer.set(-1)  # Сброс выбранного ответа

    def validate_answer(self):
        # Проверка выбранного ответа
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Предупреждение", "Выберите один из ответов.")
        else:
            self.next_question()

    def next_question(self):
        # Переход к следующему вопросу или отображение результатов
        self.results.append(int(bool(self.selected_answer.get())))
        self.selected_answer.set(-1)  # Сброс выбранного ответа
        if self.current_page < len(self.questions) - 1:
            self.current_page += 1
            self.question_frame.destroy()
            self.create_question_page()
        else:
            self.question_frame.destroy()
            self.create_result_page()
            self.show_results()

    def show_results(self):
        # Отображение результатов
        personality_type, _ = self.who_are_you(self.results)
        result_text = self.load_result_text(personality_type[0])

        self.result_text.insert(tk.END, result_text)

        self.result_text.configure(state="disabled")  # Блокировка редактирования текста

        self.result_text.pack(pady=10)  

        self.quit_button = tk.Button(self.result_frame, text="Закрыть", command=self.quit)
        self.quit_button.pack(pady=10)

    def who_are_you(self, results):
        # Определение типа личности на основе результатов
        personality_type = ""

        if results[::7].count(1) > results[::7].count(0):
            e_i_max = results[::7].count(1)
            personality_type += "I"
        else:
            e_i_max = results[::7].count(0)
            personality_type += "E"

        ei = e_i_max

        if (results[1::7].count(1) + results[2::7].count(1)) > (results[1::7].count(0) + results[2::7].count(0)):
            s_n_max = results[1::7].count(1) + results[2::7].count(1)
            personality_type += "N"
        else:
            s_n_max = results[1::7].count(0) + results[2::7].count(0)
            personality_type += "S"

        sn = s_n_max

        if (results[3::7].count(1) + results[4::7].count(1)) > (results[3::7].count(0) + results[4::7].count(0)):
            t_f_max = results[3::7].count(1) + results[4::7].count(1)
            personality_type += "F"
        else:
            t_f_max =  results[3::7].count(0) + results[4::7].count(0)
            personality_type += "T"

        tf = t_f_max

        if (results[5::7].count(1) + results[6::7].count(1)) > (results[5::7].count(0) + results[6::7].count(0)):
            j_p_max = results[5::7].count(1) + results[6::7].count(1)
            personality_type += "P"
        else:
            j_p_max = results[5::7].count(0) + results[6::7].count(0)
            personality_type += "J"

        jp = j_p_max
        return [[personality_type, ei + sn + tf + jp], [ei, sn, tf, jp]]

    def load_result_text(self, personality_type):
        # Загрузка текста результата из файла
        with open('result_text/' + personality_type + ".md", "r", encoding="utf-8") as file:
            result_text = file.read()
        return result_text

app = PersonalityTestApp()
app.mainloop()