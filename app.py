from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Путь к файлу с данными
DATA_FILE = 'entries.json'

def load_entries():
    """Загружает записи из JSON-файла. Если файл не существует, возвращает пустой список."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_entries(entries):
    """Сохраняет список записей в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

# Загружаем записи при старте
entries = load_entries()

# ---------- Маршруты ----------

@app.route('/')
def index():
    """Главная страница со списком всех записей."""
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    """Страница просмотра одной записи."""
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry is None:
        return 'Запись не найдена', 404
    return render_template('detail.html', entry=entry)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Добавление новой записи."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            return 'Заголовок и текст не могут быть пустыми', 400

        # Генерация нового ID
        new_id = max([e['id'] for e in entries], default=0) + 1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {
            'id': new_id,
            'title': title,
            'content': content,
            'date': now
        }
        entries.append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    """Редактирование существующей записи."""
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry is None:
        return 'Запись не найдена', 404

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            return 'Заголовок и текст не могут быть пустыми', 400
        entry['title'] = title
        entry['content'] = content
        # Дату не меняем (оставляем исходную)
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    """Удаление записи (POST-запрос)."""
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Поиск записей по заголовку (без учёта регистра)."""
    query = request.args.get('q', '').strip().lower()
    if not query:
        return redirect(url_for('index'))
    filtered = [e for e in entries if query in e['title'].lower()]
    return render_template('index.html', entries=filtered)

@app.route('/filter/week')
def filter_week():
    """Фильтр записей за последние 7 дней."""
    week_ago = datetime.now() - timedelta(days=7)
    filtered = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d %H:%M:%S')
            if entry_date >= week_ago:
                filtered.append(e)
        except (ValueError, KeyError):
            # Если дата в неправильном формате, пропускаем запись
            continue
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)