import re
import requests
import telebot
import time

BOT_TOKEN = "8940503804:AAHQWBBipgYujzllOs3USpWbDJCap-WPFv0"
bot = telebot.TeleBot(BOT_TOKEN)

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

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{5,32}$', username):
        return False, "Недопустимая длина или символы"
    reserved = ["admin", "support", "telegram", "bot", "fragment", "root", "system"]
    if username.lower() in reserved:
        return False, "Зарезервированное слово"
    return True, "ОК"
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
    available = (tg is True or tg is None) and (frag is True or frag is None) and valid
    report['available'] = available
    report['details'] = f"TG: {tg}, Fragment: {frag}, Соцсети: {social}"
    return report
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Пришлите юзернейм для проверки (без @).\nПример: myusername")

@bot.message_handler(func=lambda m: True)
def handle_username(message):
    username = message.text.strip().lower()
    if not username:
        bot.reply_to(message, "Введите хотя бы один символ.")
        return
    if username.startswith("@"):
        username = username[1:]

    base = username
    variants = []
    if len(base) < 5:
        variants.append(base + "1" * (5 - len(base)))
    elif len(base) > 32:
        base = base[:32]
        variants.append(base)
    else:
        variants.append(base)

    for suffix in ["_", "1", "2026", "bot"]:
        if len(base + suffix) <= 32 and len(base + suffix) >= 5:
            variants.append(base + suffix)

    variants = list(set(variants))
    results = []
    for v in variants:
        results.append(full_check(v))
        answer = "📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:\n\n"
    for r in results:
        status = "✅ СВОБОДЕН" if r.get('available') else "❌ ЗАНЯТ"
        answer += f"@{r['input']} → {status}\n"
        answer += f"   Валидация: {r['validation_msg']}\n"
        answer += f"   Telegram: {'свободен' if r['telegram'] is True else 'занят' if r['telegram'] is False else 'ошибка'}\n"
        answer += f"   Fragment: {'свободен' if r['fragment'] is True else 'занят' if r['fragment'] is False else 'ошибка'}\n"
        if r.get('social'):
            soc = r['social']
            answer += f"   Instagram: {'свободен' if soc.get('instagram') is True else 'занят' if soc.get('instagram') is False else 'ошибка'}\n"
            answer += f"   Twitter: {'свободен' if soc.get('twitter') is True else 'занят' if soc.get('twitter') is False else 'ошибка'}\n"
        answer += "\n"

    if not any(r.get('available') for r in results):
        answer += "🔍 Все варианты заняты. Ищу свободный близкий вариант...\n"
        found = None
        for i in range(1, 100):
            candidate = base + str(i)
            if len(candidate) > 32:
                break
            valid, _ = validate_username(candidate)
            if not valid:
                continue
            if check_telegram(candidate) is True and check_fragment(candidate) is True:
                found = candidate
                break
        if found:
            answer += f"✅ Рекомендую: @{found} — свободен во всех проверках."
        else:
            answer += "❌ Свободный вариант не найден в пределах 100 переборов."

    bot.reply_to(message, answer)

if __name__ == "__main__":
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)
