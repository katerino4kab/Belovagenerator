from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'todo.db'


# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Инициализация базы данных
def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            text TEXT NOT NULL
                        )''')
        conn.commit()


def create_pic_pillow(pic, text):
    pass


# Маршрут для создания заметки
@app.route('/createPic', methods=['POST'])
def create_pic():
    text = request.json.get('text')
    
    create_pic_pillow()

    return jsonify({'id': todo_id, 'text': text}), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
