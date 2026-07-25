import re
import requests
import telebot
import time
import random
import string

BOT_TOKEN = "8940503804:AAHQWBBipgYujzllOs3USpWbDJCap-WPFv0"
bot = telebot.TeleBot(BOT_TOKEN)

COMMON_WORDS = set([
    "bitcoin", "ethereum", "solana", "cardano", "polkadot", "ripple", "litecoin",
    "monero", "zcash", "tether", "usdt", "usdc", "binance", "coinbase", "kraken",
    "bybit", "okx", "blockchain", "mining", "wallet", "private", "public", "seed",
    "phrase", "mnemonic", "ledger", "trezor", "metamask", "pancake", "uniswap",
    "liquidity", "staking", "yield", "apr", "apy", "gas", "fee", "commission",
    "investor", "investment", "profit", "loss", "capital", "asset", "liability",
    "equity", "cash", "credit", "debit", "mortgage", "loan", "bond", "stock",
    "share", "dividend", "arbitrage", "hedge", "swap", "option", "future",
    "forex", "trader", "broker", "exchange", "market", "bull", "bear", "greed",
    "fear", "fomo", "jeet", "whale", "shark", "pump", "dump", "rug", "pull",
    "salary", "tax", "audit", "accountant", "bookkeeper", "cfo", "ceo", "startup",
    "venture", "angel", "seed", "series", "revenue", "ebitda", "valuation",
    "love", "lust", "desire", "kiss", "touch", "pleasure", "passion", "romance",
    "sexy", "hot", "beautiful", "handsome", "cute", "adorable", "charming",
    "seductive", "intimate", "sensual", "orgasm", "erotic", "fetish", "kinky",
    "bdsm", "dom", "sub", "switch", "bondage", "latex", "leather", "spank",
    "whip", "collar", "cage", "rope", "blindfold", "vibrator", "dildo", "strap",
    "penis", "vagina", "breast", "nipple", "clitoris", "erection", "cum", "sperm",
    "porn", "nude", "strip", "lapdance", "pole", "burlesque", "cam", "onlyfans",
    "sugar", "daddy", "mommy", "mistress", "master", "slave", "pet", "puppy",
    "cuckold", "femdom", "maledom", "impact", "breathplay", "knifeplay",
    "edgeplay", "consent", "primal", "tantra", "lingam", "yoni", "sacred",
    "python", "javascript", "rust", "golang", "swift", "kotlin", "java", "cplusplus",
    "sql", "nosql", "mongodb", "postgres", "mysql", "redis", "elastic", "docker",
    "kubernetes", "linux", "unix", "windows", "macos", "android", "ios", "kernel",
    "exploit", "vulnerability", "payload", "shellcode", "reverse", "engineering",
    "malware", "ransomware", "trojan", "virus", "worm", "backdoor", "rootkit",
    "ddos", "botnet", "phishing", "spoofing", "sniffing", "spyware", "adware",
    "firewall", "encryption", "decrypt", "hash", "salt", "bcrypt", "aes", "rsa",
    "ssl", "tls", "tor", "i2p", "proxy", "vpn", "anonymity", "privacy",
    "zero", "day", "buffer", "overflow", "xss", "csrf", "injection", "sqli",
    "osint", "social", "engineering", "password", "bruteforce", "hashcat",
])
COMMON_WORDS.update([
    "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind", "storm",
    "thunder", "lightning", "fire", "water", "earth", "stone", "mountain",
    "river", "lake", "ocean", "sea", "wave", "sand", "desert", "forest",
    "jungle", "flower", "tree", "bird", "eagle", "tiger", "lion", "wolf",
    "bear", "fox", "deer", "rabbit", "snake", "shark", "whale", "dolphin",
    "seagull", "sparrow", "hawk", "falcon", "panther", "leopard", "cheetah",
    "hyena", "crocodile", "alligator", "turtle", "frog", "salmon", "trout",
    "happiness", "sadness", "anger", "fear", "surprise", "disgust", "love",
    "hate", "joy", "pain", "calm", "peace", "chaos", "silence", "sound",
    "light", "dark", "warm", "cold", "sweet", "bitter", "sour", "salty",
    "hope", "despair", "courage", "cowardice", "pride", "shame", "guilt",
    "jealousy", "envy", "gratitude", "compassion", "empathy", "sympathy",
    "heart", "brain", "lungs", "liver", "kidney", "stomach", "intestine",
    "muscle", "bone", "skin", "blood", "vein", "artery", "nerve", "cell",
    "oxygen", "carbon", "dioxide", "hormone", "enzyme", "protein", "fat",
    "doctor", "nurse", "surgeon", "therapy", "psychology", "psychiatry",
    "trauma", "stress", "anxiety", "depression", "bipolar", "psychosis",
    "sport", "run", "jump", "swim", "gym", "fit", "yoga", "pilates", "boxing",
    "football", "soccer", "tennis", "golf", "basketball", "volleyball",
    "baseball", "hockey", "skiing", "snowboard", "surfing", "skateboarding",
    "chess", "poker", "blackjack", "roulette", "slot", "gamble", "bet",
    "pizza", "burger", "sushi", "ramen", "taco", "burrito", "steak", "wine",
    "beer", "vodka", "whiskey", "rum", "gin", "juice", "coffee", "tea",
    "chocolate", "vanilla", "strawberry", "mango", "pineapple", "coconut",
    "garlic", "onion", "pepper", "salt", "spice", "herb", "rosemary", "thyme",
])
COMMON_WORDS.update([
    "moscow", "london", "nyc", "tokyo", "berlin", "paris", "rome", "madrid",
    "usa", "uk", "eu", "china", "india", "japan", "brazil", "canada",
    "english", "spanish", "french", "german", "chinese", "arabic", "russian",
    "alex", "max", "ivan", "john", "jane", "lisa", "anna", "maria", "david",
    "zeus", "athena", "apollo", "hercules", "odin", "thor", "loki", "freya",
    "anubis", "osiris", "horus", "isis", "ra", "shiva", "vishnu", "brahma",
    "meme", "dank", "sigma", "alpha", "beta", "chad", "virgin", "giga",
    "pog", "based", "cringe", "sus", "bruh", "lol", "rofl", "lmao",
    "yeet", "bet", "cap", "no", "fam", "lit", "fire", "goat", "muda",
    "science", "space", "planet", "galaxy", "nebulae", "cosmos", "asteroid",
    "comet", "meteor", "gravity", "quantum", "particle", "atom", "molecule",
    "logic", "reason", "truth", "false", "infinite", "finite", "void", "abyss",
    "miracle", "dream", "magic", "power", "faith", "destiny", "shadow",
    "flame", "frost", "bloom", "crystal", "honey", "nectar", "bliss",
    "echo", "rebel", "queen", "king", "crown", "throne", "sword", "shield",
    "wand", "spell", "curse", "blessing", "potion", "dragon", "unicorn"
])
def check_telegram(username):
    try:
        r = requests.get(f"https://t.me/{username}", timeout=5)
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
def is_word_like(text):
    text = text.lower()
    if len(text) < 3:
        return False
    if text in COMMON_WORDS:
        return True
    for word in COMMON_WORDS:
        if len(word) < 3:
            continue
        if word in text:
            return True
        common = sum(1 for a, b in zip(text, word) if a == b)
        if len(word) >= 3 and common / len(word) > 0.6:
            return True
    return False

def generate_usernames(length, count=30):
    chars = string.ascii_lowercase + string.digits
    results = []
    attempts = 0
    while len(results) < count and attempts < count * 10:
        attempts += 1
        middle = ''.join(random.choices(string.ascii_lowercase + string.digits + "_", k=length - 1))
        last = random.choice(string.ascii_lowercase + string.digits)
        candidate = middle + last
        if validate_username(candidate)[0] and candidate not in results:
            results.append(candidate)
    return results

def check_generator(username):
    tg = check_telegram(username)
    frag = check_fragment(username)
    available = (tg is True or tg is None) and (frag is True or frag is None)
    wordlike = is_word_like(username)
    return {"username": username, "available": available, "wordlike": wordlike}
@bot.message_handler(commands=['start'])
def old_bot(message):
    bot.reply_to(message, "Пришлите юзернейм для проверки (без @).\nПример: myusername")

@bot.message_handler(commands=['generate'])
def new_bot(message):
    bot.reply_to(message, "Отправьте число от 3 до 20 — сгенерирую юзернеймы.")

@bot.message_handler(func=lambda m: m.text.isdigit() and m.text not in ["/start", "/generate"])
def handle_generate(message):
    length = int(message.text.strip())
    if length < 3 or length > 20:
        bot.reply_to(message, "Длина от 3 до 20.")
        return
    candidates = generate_usernames(length, 30)
    results = [check_generator(u) for u in candidates]
    sorted_results = sorted(results, key=lambda x: (not x['wordlike'], not x['available']))
    answer = f"🎲 Юзернеймы длиной {length}:\n\n"
    for idx, r in enumerate(sorted_results[:30], 1):
        status = "✅" if r['available'] else "❌"
        word_tag = " [СЛОВО]" if r['wordlike'] else ""
        answer += f"{idx}. @{r['username']} {status}{word_tag}\n"
    free = [r['username'] for r in results if r['available']]
    if free:
        answer += f"\n💡 Свободные: {', '.join('@'+u for u in free[:5])}"
    bot.reply_to(message, answer)

@bot.message_handler(func=lambda m: True)
def old_bot_check(message):
    username = message.text.strip().lower()
    if not username or username.startswith("/"):
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
        answer += "🔍 Все заняты. Ищу свободный...\n"
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
            answer += f"✅ Рекомендую: @{found} — свободен."
        else:
            answer += "❌ Свободный не найден."
    bot.reply_to(message, answer)

if __name__ == "__main__":
    print("Оба бота запущены...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)
