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


# Маршрут для создания заметки
@app.route('/todo', methods=['POST'])
def create_todo():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todo (text) VALUES (?)', (text,))
        conn.commit()
        todo_id = cursor.lastrowid

    return jsonify({'id': todo_id, 'text': text}), 201


# Маршрут для редактирования текста заметки по id
@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE todo SET text = ? WHERE id = ?', (text, id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Todo not found'}), 404

    return jsonify({'id': id, 'text': text})


# Маршрут для удаления заметки по id
@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todo WHERE id = ?', (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Todo not found'}), 404

    return jsonify({'message': 'Todo deleted'})


# Маршрут для получения всех заметок
@app.route('/todo', methods=['GET'])
def get_all_todos():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todo')
        todos = cursor.fetchall()
        todos_list = [{'id': row['id'], 'text': row['text']} for row in todos]

    return jsonify(todos_list)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
