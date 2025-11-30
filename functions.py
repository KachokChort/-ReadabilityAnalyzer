import re

MAX_RES_EN = 221.22
MAX_RES_RU = 225.22


def count_syllables_en(word):
    word = word.lower()
    if len(word) <= 3:
        return 1

    count = 0
    vowels = "aeiouy"

    if word.endswith(('e', 'es', 'ed')) and not word.endswith(('le', 'les')):
        word = word[:-1]

    for i in range(len(word)):
        if word[i] in vowels:
            if i == 0 or word[i - 1] not in vowels:
                count += 1

    return max(1, count)


def count_syllables_ru(word):
    vowels = "аеёиоуыэюя"
    word = word.lower()
    count = 0

    for char in word:
        if char in vowels:
            count += 1

    return max(1, count)


def english(text):
    if not text.strip():
        return None

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r'\b[a-z]+\b', text, re.IGNORECASE)

    if not sentences or not words:
        return None

    total_syllables = sum(count_syllables_en(word) for word in words)

    avg_words_per_sentence = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    result = 306.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    result = max(result, 0)
    k = result / MAX_RES_EN
    result = 100 * k

    return round(result, 2)


def russian(text):
    if not text.strip():
        return None

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r'\b[а-я]+\b', text, re.IGNORECASE)

    if not sentences or not words:
        return None

    total_syllables = sum(count_syllables_ru(word) for word in words)

    avg_words_per_sentence = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    result = 266.835 - (1.52 * avg_words_per_sentence) - (40.1 * avg_syllables_per_word)
    result = max(result, 0)
    k = result / MAX_RES_RU
    result = 100 * k
    return round(result, 2)
