from flask import Flask, render_template, request
from functions import english, russian
from flask import Flask, render_template, request, session, redirect, url_for
from data import db_session
from data.users import User
from data.texts import Text
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'Jigjdfhdjsfjnseufnsnfsufsuikf'


def get_readability_level(score):
    if score >= 90: return "Очень легко (5 класс)"
    if score >= 80: return "Легко (6 класс)"
    if score >= 70: return "Достаточно легко (7 класс)"
    if score >= 60: return "Стандартно (8-9 класс)"
    if score >= 50: return "Сложно (10-11 класс)"
    if score >= 30: return "Очень сложно (студенты)"
    if score >= 0: return "Профессиональный уровень"
    return "Академический уровень"


def analyze_text_stats(text, score):
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?') or 1
    reading_time = round(max(1, words // 3) * max((3 - score * 3 / 100), 0.9), 2)
    words_per_sentence = words / sentences

    return {
        'words': words,
        'sentences': sentences,
        'reading_time': reading_time,
        'words_per_sentence': round(words_per_sentence, 1)
    }


def get_recommendations(score, stats):
    recommendations = []

    if score < 60:
        recommendations.append("Упростите предложения - разбейте длинные на несколько")
        recommendations.append("Используйте более простые и понятные слова")

    if score > 80:
        recommendations.append("Текст отлично сбалансирован!")
        recommendations.append("Подходит для широкой аудитории")

    if stats['words_per_sentence'] > 20:
        recommendations.append("Слишком длинные предложения - упростите структуру")

    if stats['words_per_sentence'] < 5:
        recommendations.append("Предложения слишком короткие - можно объединить")

    if not recommendations:
        recommendations.append("Текст хорошо сбалансирован")

    return recommendations


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        language = request.form.get('language', 'russian')

        if not text:
            return render_template('index.html', error="Введите текст для анализа")

        if len(text) < 10:
            return render_template('index.html', error="Текст должен содержать минимум 10 символов")

        if language == 'english':
            score = english(text)
        else:
            score = russian(text)

        if score is None:
            return render_template('index.html', error="Не удалось проанализировать текст")

        stats = analyze_text_stats(text, score)
        level = get_readability_level(score)
        recommendations = get_recommendations(score, stats)

        return render_template('index.html',
                               score=round(score, 1),
                               level=level,
                               stats=stats,
                               recommendations=recommendations,
                               text=text,
                               language=language)

    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    users = [user.username for user in db_sess.query(User).all()]
    if session.get("user", "") not in users:
        return redirect(url_for("register"))

    texts = [text for text in db_sess.query(Text).filter(Text.user == session.get("user", ""))]

    return render_template('index.html', tests=texts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password or not username.strip() or not password.strip():
            return render_template('register.html', error="Необходимо ввести пароль и имя пользователя.")
        if len(password) <= 3:
            return render_template('register.html', error="Короткий пароль.")

        try:
            db_session.global_init("db/db.db")
            db_sess = db_session.create_session()
            users = [user.username for user in db_sess.query(User).all()]
            if username not in users:
                return render_template('login.html', error="Такого пользователя не существует")
            user_password = db_sess.query(User).filter(User.username == username).first().password
            if password != user_password:
                return render_template('login.html', error="Неправильный пароль")
        except Exception as e:
            return render_template('login.html', error=e)

        session['user'] = username
        return redirect(url_for('index'))

    session.clear()

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password or not username.strip() or not password.strip():
            return render_template('register.html', error="Необходимо ввести пароль и имя пользователя.")
        if len(password) <= 3:
            return render_template('register.html', error="Короткий пароль.")

        try:
            db_session.global_init("db/db.db")
            db_sess = db_session.create_session()
            users = [user.username for user in db_sess.query(User).all()]
            if username in users:
                return render_template('register.html', error="Такой пользователь уже существует.")
            new_user = User()
            new_user.username = username
            new_user.password = password
            db_sess.add(new_user)
            db_sess.commit()
            db_sess.close()
        except Exception as e:
            return render_template('login.html', error=e)

        session['user'] = username
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/save_test', methods=['POST'])
def save_test():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()

        new_text = Text()

        text = request.form.get('text')
        score = float(request.form.get('score'))

        stats = analyze_text_stats(text, score)
        level = get_readability_level(score)
        recommendations = get_recommendations(score, stats)

        new_text.name = f"Анализ от {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        new_text.user = session['user']
        new_text.text = text
        new_text.score = str(score)
        new_text.level = str(level)
        new_text.sentences = str(stats.get("sentences"))
        new_text.words = str(stats.get("words"))
        new_text.words_per_sentence = str(stats.get("words_per_sentence"))
        new_text.reading_time = str(stats.get("reading_time"))
        new_text.recommendations = recommendations

        db_sess.add(new_text)
        db_sess.commit()
        db_sess.close()

    except Exception as e:
        print(f"Error saving test: {e}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8001)
