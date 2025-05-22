import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random
from datetime import datetime
import os
from PIL import Image, ImageTk

class VocabQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English → Japanese Vocabulary Quiz")
        self.root.geometry("600x600")

        # Background Image
        self.bg_image = Image.open("japan_background.jpg").resize((600, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas for background image
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Frame
        self.frame = tk.Frame(root, bg="#ffffff", bd=3, relief=tk.RIDGE)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=550, height=550)

        self.csv_files = {
            "Noun": "Noun.csv",
            "Adjective": "Adjective.csv",
            "Verbs": "Verbs.csv",
            "TimeDate": "TimeDate.csv",
            "Numbers & Counts": "NumbersCounts.csv"
        }

        self.data = None
        self.questions = []
        self.current_q = 0
        self.score = 0
        self.quiz_length = 5
        self.wrong_answers = []

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffffff")
        style.configure("TCombobox", font=("Segoe UI", 11))

        self.title_label = ttk.Label(self.frame, text="English → Japanese", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(pady=10)

        self.combo_label = ttk.Label(self.frame, text="Choose category:")
        self.combo_label.pack()
        self.csv_selector = ttk.Combobox(self.frame, values=list(self.csv_files.keys()), state="readonly")
        self.csv_selector.pack(pady=5)
        self.csv_selector.current(0)

        self.length_label = ttk.Label(self.frame, text="Number of questions:")
        self.length_label.pack()
        self.length_selector = ttk.Spinbox(self.frame, from_=5, to=20, width=5, font=("Segoe UI", 11))
        self.length_selector.pack(pady=5)
        self.length_selector.delete(0, tk.END)
        self.length_selector.insert(0, "5")

        self.word_label = ttk.Label(self.frame, text="Click Start to begin", font=("Segoe UI", 13))
        self.word_label.pack(pady=10)

        entry_frame = tk.Frame(self.frame, bg="#ffffff")
        entry_frame.pack(pady=5)

        self.entry = ttk.Entry(entry_frame, font=("Segoe UI", 12))
        self.entry.pack(side=tk.LEFT, padx=(0, 10))

        self.submit_btn = tk.Button(entry_frame, text="Submit", command=self.check_answer, state=tk.DISABLED,
                                     bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"))
        self.submit_btn.pack(side=tk.RIGHT)

        self.feedback_label = ttk.Label(self.frame, text="", font=("Segoe UI", 11))
        self.feedback_label.pack(pady=5)

        self.start_btn = tk.Button(self.frame, text="Start Quiz", command=self.start_quiz, 
                                   bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"))
        self.start_btn.pack(pady=10)

        button_row = tk.Frame(self.frame, bg="#ffffff")
        button_row.pack(side=tk.BOTTOM, pady=10)

        self.history_btn = tk.Button(button_row, text="Show Score History", command=self.show_history,
                                     bg="#f0f0f0", font=("Segoe UI", 10))
        self.history_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(button_row, text="Clear Score History", command=self.clear_history,
                                    bg="#f0f0f0", font=("Segoe UI", 10))
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.reset_mistakes_btn = tk.Button(button_row, text="Reset Mistakes", command=self.reset_mistake_history,
                                            bg="#f0f0f0", font=("Segoe UI", 10))
        self.reset_mistakes_btn.pack(side=tk.LEFT, padx=5)

    def load_csv(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File {filename} not found!")
            return None
        df = pd.read_csv(filename)
        if 'mistakes' not in df.columns:
            df['mistakes'] = 0
        return df

    def update_mistake_count(self, word):
        df = self.data
        df.loc[df['english'] == word['english'], 'mistakes'] += 1
        df.to_csv(self.csv_files[self.csv_selector.get()], index=False)

    def start_quiz(self):
        self.current_q = 0
        self.score = 0
        self.wrong_answers = []
        self.quiz_length = int(self.length_selector.get())

        category = self.csv_selector.get()
        filename = self.csv_files[category]
        self.data = self.load_csv(filename)

        if self.data is not None:
            self.questions = self.data.to_dict(orient='records')
            self.ask_question()

    def ask_question(self):
        if self.current_q < self.quiz_length:
            self.current_word = random.choice(self.questions)
            self.word_label.config(text=self.current_word['english'])
            self.submit_btn.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.feedback_label.config(text="")
        else:
            self.end_quiz()

    def check_answer(self):
        user_input = self.entry.get().strip()
        correct_answer = self.current_word['japanese'].strip()
        english_word = self.current_word['english'].strip()

        if user_input == correct_answer:
            self.feedback_label.config(text="✅ Correct!", foreground="green")
            self.score += 1
        else:
            self.feedback_label.config(text=f"❌ Wrong! Correct: {correct_answer}", foreground="red")
            self.wrong_answers.append(f"{english_word}: {correct_answer} ≠ {user_input or '[empty]'} (Mistakes: {self.current_word['mistakes'] + 1})")
            self.update_mistake_count(self.current_word)

        self.current_q += 1
        self.root.after(1500, self.ask_question)

    def end_quiz(self):
        self.save_quiz_result()
        messagebox.showinfo("Quiz Completed", f"Your score: {self.score}/{self.quiz_length}")

    def save_quiz_result(self):
        history_file = "score_history.csv"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        category = self.csv_selector.get()
        row = {"datetime": now, "category": category, "score": self.score, "total": self.quiz_length}
        df = pd.DataFrame([row])
        if os.path.exists(history_file):
            df.to_csv(history_file, mode='a', index=False, header=False)
        else:
            df.to_csv(history_file, index=False)

    def show_history(self):
        history_file = "score_history.csv"
        if not os.path.exists(history_file):
            messagebox.showinfo("History", "No history available.")
            return

        df = pd.read_csv(history_file)
        last_five = df.tail(5)

        popup = tk.Toplevel(self.root)
        popup.title("Quiz Score History")
        popup.geometry("400x200")

        title = ttk.Label(popup, text="Last 5 Quiz Sessions", font=("Segoe UI", 12, "bold"))
        title.pack(pady=5)

        tree = ttk.Treeview(popup, columns=("datetime", "category", "score", "total"), show="headings")
        tree.heading("datetime", text="Date & Time")
        tree.heading("category", text="Category")
        tree.heading("score", text="Score")
        tree.heading("total", text="Total")

        for index, row in last_five.iterrows():
            tree.insert("", tk.END, values=(row["datetime"], row["category"], row["score"], row["total"]))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def clear_history(self):
        history_file = "score_history.csv"
        if os.path.exists(history_file):
            os.remove(history_file)
        messagebox.showinfo("History Cleared", "Score history has been cleared.")

    def reset_mistake_history(self):
        category = self.csv_selector.get()
        filename = self.csv_files[category]
        df = self.load_csv(filename)
        if df is not None:
            df['mistakes'] = 0
            df.to_csv(filename, index=False)
            messagebox.showinfo("Mistakes Reset", "Mistakes history has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabQuizApp(root)
    root.mainloop()
