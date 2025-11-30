from flask import Flask, render_template, request
from functions import english, russian

app = Flask(__name__)


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

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8001)