from flask import Flask, send_from_directory, jsonify
import sqlite3
import os

app = Flask(__name__, static_folder='static')

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL
    )''')
    c.execute("SELECT COUNT(*) FROM tasks")
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO tasks (question, options, correct_answer, explanation)
                     VALUES (?, ?, ?, ?)''',
                  ("В каком слове допущена ошибка?",
                   '["Подъезд", "Притензия", "Красивее", "Баловать"]',
                   "2",
                   "Правильно писать 'претензия'."))
    conn.commit()
    conn.close()

# Главная страница (Web App)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# API для получения задания
@app.route('/get_task')
def get_task():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT question, options, correct_answer, explanation FROM tasks LIMIT 1")
    task = c.fetchone()
    conn.close()
    return jsonify({
        "question": task[0],
        "options": eval(task[1]),  # Преобразуем строку в список
        "correct_answer": task[2],
        "explanation": task[3]
    })

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Render использует переменную PORT
    app.run(host="0.0.0.0", port=port)