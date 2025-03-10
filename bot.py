from flask import Flask, send_from_directory, jsonify, request
import sqlite3
import os

app = Flask(__name__, static_folder='static')

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        task_type TEXT NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL
    )''')
    c.execute("SELECT COUNT(*) FROM tasks")
    if c.fetchone()[0] == 0:
        # Добавляем примеры заданий
        tasks = [
            ("Орфография", "Задание 1", "В каком слове допущена ошибка?", '["Подъезд", "Притензия", "Красивее", "Баловать"]', "2", "Правильно писать 'претензия'."),
            ("Орфография", "Задание 1", "Укажите слово с ударением на первом слоге:", '["Торты", "Звонит", "Средства", "Каталог"]', "1", "Правильное ударение в слове 'торты' на первом слоге."),
            ("Пунктуация", "Задание 2", "Где нужно поставить запятую?", '["Я хотел бы пойти в кино, но у меня нет времени.", "Я хотел бы пойти в кино но у меня нет времени."]', "1", "Запятая ставится перед союзом 'но'."),
            ("Лексика", "Задание 3", "Какое слово является синонимом слова 'красивый'?", '["Уродливый", "Прекрасный", "Страшный", "Нелепый"]', "2", "Синоним слова 'красивый' — 'прекрасный'."),
            # Добавьте больше заданий здесь
        ]
        c.executemany('''INSERT INTO tasks (category, task_type, question, options, correct_answer, explanation)
                          VALUES (?, ?, ?, ?, ?, ?)''', tasks)
    conn.commit()
    conn.close()

# Главная страница (Web App)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# API для получения задания
@app.route('/get_task')
def get_task():
    task_type = request.args.get('task_type', default=None, type=str)
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if task_type:
        c.execute("SELECT question, options, correct_answer, explanation FROM tasks WHERE task_type = ? ORDER BY RANDOM() LIMIT 1", (task_type,))
    else:
        c.execute("SELECT question, options, correct_answer, explanation FROM tasks ORDER BY RANDOM() LIMIT 1")
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
