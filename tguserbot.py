import re
import requests
import telebot
import time

# ===== КОНФИГУРАЦИЯ =====
BOT_TOKEN = "8940503804:AAHQWBBipgYujzllOs3USpWbDJCap-WPFv0"  # замени на реальный токен
bot = telebot.TeleBot(BOT_TOKEN)

# ===== ПРОВЕРКА В TELEGRAM =====
def check_telegram(username):
    url = f"https://t.me/{username}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            if "If you have Telegram" in r.text or "You can contact" in r.text:
                return False
            return True
        return None
    except:
        return None

# ===== ПРОВЕРКА В FRAGMENT =====
def check_fragment(username):
    try:
        r = requests.get(f"https://fragment.com/api/auction/username/{username}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("auction") or data.get("price"):
                return False
            return True
        return None
    except:
        return None

# ===== ПРОВЕРКА ДЛИНЫ И СИМВОЛОВ =====
def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{5,32}$', username):
        return False, "Недопустимая длина или символы (только латиница, цифры, _, 5-32)"
    reserved = ["admin", "support", "telegram", "bot", "fragment", "root", "system"]
    if username.lower() in reserved:
        return False, "Зарезервированное слово"
    return True, "ОК"

# ===== ПРОВЕРКА В INSTAGRAM И TWITTER =====
def check_social(username):
    results = {}
    try:
        r = requests.get(f"https://www.instagram.com/{username}/", timeout=3)
        results['instagram'] = r.status_code == 404
    except:
        results['instagram'] = None
    try:
        r = requests.get(f"https://twitter.com/{username}", timeout=3)
        results['twitter'] = r.status_code == 404
    except:
        results['twitter'] = None
    return results

# ===== ОСНОВНАЯ ПРОВЕРКА =====
def full_check(username):
    report = {}
    report['input'] = username
    valid, msg = validate_username(username)
    report['valid'] = valid
    report['validation_msg'] = msg
    if not valid:
        report['available'] = False
        report['details'] = "Не прошёл валидацию"
        return report

    tg = check_telegram(username)
    frag = check_fragment(username)
    social = check_social(username)

    report['telegram'] = tg
    report['fragment'] = frag
    report['social'] = social

    available = (
        (tg is True or tg is None) and
        (frag is True or frag is None) and
        valid
    )
    report['available'] = available
    report['details'] = f"TG: {tg}, Fragment: {frag}, Соцсети: {social}"
    return report

# ===== ОБРАБОТЧИК КОМАНДЫ /start =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Пришлите юзернейм для проверки (без @).\nПример: myusername")

# ===== ОБРАБОТЧИК ЛЮБОГО СООБЩЕНИЯ =====
@bot.message_handler(func=lambda m: True)
def handle_username(message):
    username = message.text.strip().lower()
    if not username:
        bot.reply_to(message, "Введите хотя бы один символ.")
        return

    # Убираем @, если пользователь его ввёл
    if username.startswith("@"):
        username = username[1:]

    base = username
    variants = []

    # Генерируем варианты, если длина не подходит
    if len(base) < 5:
        variants.append(base + "1" * (5 - len(base)))
    elif len(base) > 32:
        base = base[:32]
        variants.append(base)
    else:
        variants.append(base)

    # Добавляем суффиксы
    for suffix in ["_", "1", "2026", "bot"]:
        if len(base + suffix) <= 32 and len(base + suffix) >= 5:
            variants.append(base + suffix)

    variants = list(set(variants))

    results = []
    for v in variants:
        res = full_check(v)
        results.append(res)

    answer = "📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:\n\n"
    for r in results:
        status = "✅ СВОБОДЕН" if r.get('available') else "❌ ЗАНЯТ"
        answer += f"@{r['input']} → {status}\n"
        answer += f"   Валидация: {r['validation_msg']}\n"
        answer += f"   Telegram: {'свободен' if r['telegram'] is True else 'занят' if r[


egram'] is False else 'ошибка'}\n"
        answer += f"   Fragment: {'свободен' if r['fragment'] is True else 'занят' if r['fragment'] is False else 'ошибка'}\n"
        if r.get('social'):
            soc = r['social']
            answer += f"   Instagram: {'свободен' if soc.get('instagram') is True else 'занят' if soc.get('instagram') is False else 'ошибка'}\n"
            answer += f"   Twitter: {'свободен' if soc.get('twitter') is True else 'занят' if soc.get('twitter') is False else 'ошибка'}\n"
        answer += "\n"

    # Если все заняты — ищем свободный
    if not any(r.get('available') for r in results):
        answer += "🔍 Все варианты заняты. Ищу свободный близкий вариант...\n"
        found = None
        test_base = base
        for i in range(1, 100):
            candidate = test_base + str(i)
            if len(candidate) > 32:
                break
            valid, _ = validate_username(candidate)
            if not valid:
                continue
            tg_free = check_telegram(candidate) is True
            frag_free = check_fragment(candidate) is True
            if tg_free and frag_free:
                found = candidate
                break
        if found:
            answer += f"✅ Рекомендую: @{found} — свободен во всех проверках."
        else:
            answer += "❌ Свободный вариант не найден в пределах 100 переборов."

    bot.reply_to(message, answer)

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 секунд...")
            time.sleep(5)'tel
   
