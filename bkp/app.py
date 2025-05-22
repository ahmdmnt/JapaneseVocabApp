import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import os
from datetime import datetime

# Constants
APP_WIDTH = 600
APP_HEIGHT = 800
CATEGORIES = ["Noun", "Adjectives", "Verbs", "Time&Date", "Number&Count", "AddOn"]
CATEGORY_FILES = {
    "Noun": "noun.csv",
    "Adjectives": "adjectives.csv",
    "Verbs": "verbs.csv",
    "Time&Date": "timedate.csv",
    "Number&Count": "numbercount.csv",
    "AddOn": "addon.csv"
}
HISTORY_FILE = "history.csv"

# GUI Setup
root = tk.Tk()
root.title("English → Japanese Vocabulary Quiz")
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.resizable(False, False)  # Prevent resizing

# Title and Subtitle
title = tk.Label(root, text="English → Japanese Vocabulary Quiz", font=("Helvetica", 20, "bold"))
title.pack(pady=10)
subtitle = tk.Label(root, text="日本語　練習", font=("Helvetica", 16))
subtitle.pack(pady=5)

# Category Selection
category_var = tk.StringVar()
category_label = tk.Label(root, text="Choose Category", font=("Helvetica", 14))
category_label.pack()
category_menu = ttk.Combobox(root, textvariable=category_var, values=CATEGORIES, state="readonly")
category_menu.pack(pady=5)

# Question Count Selection
question_count_var = tk.IntVar(value=5)
question_count_label = tk.Label(root, text="Number of Questions", font=("Helvetica", 14))
question_count_label.pack()
question_count_spinbox = tk.Spinbox(root, from_=5, to=30, textvariable=question_count_var)
question_count_spinbox.pack(pady=5)

# Question Display
question_text = tk.StringVar()
question_label = tk.Label(root, textvariable=question_text, font=("Helvetica", 16), wraplength=500)
question_label.pack(pady=20)

# Answer Entry and Submit
answer_frame = tk.Frame(root)
answer_frame.pack(pady=10)
answer_entry = tk.Entry(answer_frame, font=("Helvetica", 14))
answer_entry.pack(side=tk.LEFT, padx=5)
submit_button = tk.Button(answer_frame, text="Submit", bg="green", fg="white")
submit_button.pack(side=tk.LEFT)

# Start Quiz Button
start_button = tk.Button(root, text="Start Quiz", bg="blue", fg="white", font=("Helvetica", 12))
start_button.pack(pady=10)

# Extra Feature Buttons
extra_frame = tk.Frame(root)
extra_frame.pack(side=tk.BOTTOM, pady=10)
history_button = tk.Button(extra_frame, text="Show History")
clear_history_button = tk.Button(extra_frame, text="Clear History")
reset_mistakes_button = tk.Button(extra_frame, text="Reset Mistakes")
history_button.pack(side=tk.LEFT, padx=5)
clear_history_button.pack(side=tk.LEFT, padx=5)
reset_mistakes_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
