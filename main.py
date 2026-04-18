symbols = ["~", "*", ":", ".", "•", "/", ";"]
caps_mix = ["A", "B", "C", "E", "K", "O", "T", "X", "P", "H"]

words_base = [
    "мамки", "спящие", "жесткие", "сочные",
    "жанры", "категории", "все возраста",
    "подборки", "видео"
]

def random_symbols(text):
    result = ""
    for ch in text:
        result += ch
        if random.random() < 0.25:
            result += random.choice(symbols)
    return result


def chaos_word(word):
    # иногда делаем латиницу
    if random.random() < 0.3:
        word = "".join(random.choice(caps_mix) for _ in range(random.randint(4,8)))
    
    word = random_symbols(word)

    # иногда перенос
    if random.random() < 0.5:
        split = random.randint(2, len(word)-1)
        word = word[:split] + "\n" + word[split:]

    return word


def ladder_block():
    base = ["D", "E", "C", "T", "K", "O", "E"]
    line = ""

    result = ""
    spaces = 0

    for ch in base:
        line += ch
        styled = random_symbols(line)

        result += " " * spaces + styled + "\n"
        spaces += random.randint(3,6)

    return "🔥" + result.strip() + "🔥"


def spaced_line(words):
    line = ""
    for w in words:
        line += chaos_word(w) + " " * random.randint(3,10)
    return line.strip()


def generate_text():
    blocks = []

    # 1. обычный хаос блок
    w = random.sample(words_base, 3)
    blocks.append(spaced_line(w))

    # 2. второй блок (иногда норм текст)
    if random.random() < 0.5:
        blocks.append("И   " + spaced_line(random.sample(words_base, 2)))

    # 3. инфо строка
    blocks.append(random_symbols("все возраста 💯"))

    # 4. иногда лесенка
    if random.random() < 0.7:
        blocks.append("\n" + ladder_block())

    # 5. финал
    endings = [
        "ПИШИ В ЛС 🔞",
        "пиши в личку",
        "пиши 🔥",
        "в лс 👀"
    ]

    blocks.append("\n" + random.choice(endings))

    return "\n\n".join(blocks)