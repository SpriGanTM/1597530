import tkinter as tk
from tkinter import messagebox
import random
import json
import os

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_quote():
    filtered = []
    for q in quotes:
        if (author_filter.get() == "" or q["author"] == author_filter.get()) and \
           (topic_filter.get() == "" or q["topic"] == topic_filter.get()):
            filtered.append(q)

    if not filtered:
        messagebox.showwarning("Ошибка", "Нет подходящих цитат")
        return

    q = random.choice(filtered)
    text_var.set(q["text"] + "\n— " + q["author"] + " (" + q["topic"] + ")")

    history.append(q)
    update_history()
    save_history()

def update_history():
    history_list.delete(0, tk.END)
    for q in history:
        history_list.insert(tk.END, q["text"] + " — " + q["author"])

def add_quote():
    text = entry_text.get()
    author = entry_author.get()
    topic = entry_topic.get()

    if text == "" or author == "" or topic == "":
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    q = {"text": text, "author": author, "topic": topic}
    quotes.append(q)

    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_topic.delete(0, tk.END)

root = tk.Tk()
root.title("Random Quote Generator")

quotes = load_quotes()
history = load_history()

text_var = tk.StringVar()

label = tk.Label(root, textvariable=text_var, wraplength=400)
label.pack()

tk.Button(root, text="Сгенерировать цитату", command=generate_quote).pack()

author_filter = tk.Entry(root)
author_filter.pack()

topic_filter = tk.Entry(root)
topic_filter.pack()

history_list = tk.Listbox(root, width=60)
history_list.pack()

entry_text = tk.Entry(root)
entry_text.pack()

entry_author = tk.Entry(root)
entry_author.pack()

entry_topic = tk.Entry(root)
entry_topic.pack()

tk.Button(root, text="Добавить цитату", command=add_quote).pack()

update_history()

root.mainloop()
