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
    "alex", "max", "ivan", "john", "jane", "lisa", "anna", "maria", "david",
    "sarah", "mike", "chris", "jessica", "daniel", "laura", "james", "emma",
    "robert", "olivia", "william", "sophia", "michael", "isabella", "thomas",
    "mia", "charles", "amelia", "henry", "elijah", "abigail", "joseph", "ella",
    "andrew", "hannah", "samuel", "alice", "joshua", "grace", "nathan", "victoria",
    "liam", "ava", "noah", "charlotte", "oliver", "amelie", "lucas", "lily",
    "mason", "zoe", "logan", "emily", "jack", "ella", "levi", "luna",
    "moscow", "london", "nyc", "tokyo", "berlin", "paris", "rome", "madrid",
    "amsterdam", "oslo", "stockholm", "copenhagen", "helsinki", "dublin",
    "lisbon", "athens", "warsaw", "prague", "budapest", "vienna", "zurich",
    "toronto", "vancouver", "chicago", "houston", "phoenix", "philadelphia",
    "sandiego", "dallas", "austin", "boston", "miami", "seattle", "denver",
    "sydney", "melbourne", "brisbane", "perth", "adelaide", "auckland",
    "singapore", "kualalumpur", "bangkok", "seoul", "beijing", "shanghai",
    "hongkong", "taipei", "manila", "jakarta", "mumbai", "delhi", "bangalore",
    "dubai", "riyadh", "telaviv", "cairo", "capetown", "nairobi", "lagos",
    "happiness", "sadness", "anger", "fear", "surprise", "disgust", "love",
    "hate", "joy", "pain", "calm", "peace", "chaos", "silence", "sound",
    "light", "dark", "warm", "cold", "sweet", "bitter", "sour", "salty",
    "hope", "despair", "courage", "cowardice", "pride", "shame", "guilt",
    "jealousy", "envy", "gratitude", "compassion", "empathy", "sympathy",
    "loneliness", "bliss", "ecstasy", "rage", "terror", "astonishment",
])
COMMON_WORDS.update([
    " python", "javascript", "rust", "golang", "swift", "kotlin", "java", "cplusplus",
    "sql", "nosql", "mongodb", "postgres", "mysql", "redis", "elastic", "docker",
    "kubernetes", "linux", "unix", "windows", "macos", "android", "ios", "kernel",
    "exploit", "vulnerability", "payload", "shellcode", "reverse", "engineering",
    "malware", "ransomware", "trojan", "virus", "worm", "backdoor", "rootkit",
    "ddos", "botnet", "phishing", "spoofing", "sniffing", "spyware", "adware",
    "firewall", "encryption", "decrypt", "hash", "salt", "bcrypt", "aes", "rsa",
    "ssl", "tls", "tor", "i2p", "proxy", "vpn", "anonymity", "privacy",
    "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind", "storm",
    "thunder", "lightning", "fire", "water", "earth", "stone", "mountain",
    "river", "lake", "ocean", "sea", "wave", "sand", "desert", "forest",
    "jungle", "flower", "tree", "bird", "eagle", "tiger", "lion", "wolf",
    "bear", "fox", "deer", "rabbit", "snake", "shark", "whale", "dolphin",
    "seagull", "sparrow", "hawk", "falcon", "panther", "leopard", "cheetah",
    "hyena", "crocodile", "alligator", "turtle", "frog", "salmon", "trout",
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
    "science", "space", "planet", "galaxy", "nebulae", "cosmos", "asteroid",
    "comet", "meteor", "gravity", "quantum", "particle", "atom", "molecule",
    "logic", "reason", "truth", "false", "infinite", "finite", "void", "abyss",
    "miracle", "dream", "magic", "power", "faith", "destiny", "shadow",
    "flame", "frost", "bloom", "crystal", "honey", "nectar", "bliss",
    "echo", "rebel", "queen", "king", "crown", "throne", "sword", "shield",
    "wand", "spell", "curse", "blessing", "potion", "dragon", "unicorn",
    "meme", "dank", "sigma", "alpha", "beta", "chad", "virgin", "giga",
    "pog", "based", "cringe", "sus", "bruh", "lol", "rofl", "lmao",
    "yeet", "bet", "cap", "no", "fam", "lit", "fire", "goat", "muda",
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
    "ocean", "breeze", "sunset", "sunrise", "twilight", "dawn", "dusk",
    "garden", "orchid", "lavender", "jasmine", "rose", "lily", "tulip",
    "sunflower", "daisy", "poppy", "iris", "pearl", "diamond", "ruby",
    "emerald", "sapphire", "opal", "jade", "amber", "coral", "crimson",
    "scarlet", "velvet", "satin", "silver", "golden", "bronze", "onyx",
    "jasper", "flint", "ember", "spark", "blaze", "inferno", "wildfire",
])
COMMON_WORDS.update([
    "moonlight", "starlight", "aurora", "nebula", "comet", "meteorite",
    "gravity", "orbit", "cosmic", "celestial", "astral", "stellar",
    "bloom", "garden", "orchard", "meadow", "valley", "canyon", "cliff",
    "peak", "summit", "glacier", "tundra", "taiga", "savanna", "prairie",
    "reef", "lagoon", "atoll", "fjord", "strait", "delta", "oasis",
    "eagle", "falcon", "raven", "crow", "parrot", "peacock", "swan",
    "goose", "duck", "chicken", "turkey", "pigeon", "sparrow", "finch",
    "hawk", "owl", "bat", "fox", "coyote", "jackal", "dhole", "dingo",
    "leopard", "jaguar", "puma", "lynx", "bobcat", "serval", "caracal",
    "tiger", "lion", "panther", "cheetah", "snow", "clouded", "sunda",
    "gorilla", "chimpanzee", "orangutan", "gibbon", "mandrill", "baboon",
    "monkey", "lemur", "loris", "tarsier", "marmoset", "tamarin",
    "koala", "kangaroo", "wombat", "tasmanian", "platypus", "echidna",
    "sloth", "anteater", "armadillo", "pangolin", "aardvark", "hyrax",
    "elephant", "mammoth", "mastodon", "rhinoceros", "hippopotamus",
    "giraffe", "zebra", "okapi", "moose", "elk", "reindeer", "caribou",
    "bison", "buffalo", "yak", "muskox", "goat", "sheep", "ram", "ewe",
    "camel", "llama", "alpaca", "guanaco", "vicuna", "horse", "pony",
    "donkey", "mule", "zebroid", "quagga", "wild", "mustang", "brumby",
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

def generate_usernames(length, count=30, mode="any"):
    if mode == "no_digits":
        chars = string.ascii_lowercase
        middle_chars = string.ascii_lowercase + "_"
    elif mode == "only_digits":
        chars = string.ascii_lowercase + string.digits
        middle_chars = chars + "_"
    else:
        chars = string.ascii_lowercase + string.digits
        middle_chars = chars + "_"

    results = []
    attempts = 0
    while len(results) < count and attempts < count * 10:
        attempts += 1
        middle = ''.join(random.choices(middle_chars, k=length - 1))
        last = random.choice(chars)
        candidate = middle + last
        if validate_username(candidate)[0] and candidate not in results:
            results.append(candidate)
    return results
def generate_words(length, count=30):
    words = [w for w in COMMON_WORDS if len(w) == length and re.match(r'^[a-z]+$', w)]
    if len(words) < count:
        chars = string.ascii_lowercase
        for _ in range(count * 10):
            if len(words) >= count:
                break
            w = ''.join(random.choices(chars, k=length))
            if w not in words and validate_username(w)[0]:
                words.append(w)
    return random.sample(words, min(count, len(words)))

def check_generator(username):
    tg = check_telegram(username)
    frag = check_fragment(username)
    available = (tg is True or tg is None) and (frag is True or frag is None)
    wordlike = is_word_like(username)
    return {"username": username, "available": available, "wordlike": wordlike}
@bot.message_handler(commands=['command'])
def show_commands(message):
    bot.reply_to(message,
        "📋 Доступные команды:\n\n"
        "/command — показать это сообщение\n"
        "/start — старый бот (проверка юзернейма)\n"
        "/generate — справка по генерации\n\n"
        "🎲 Генерация случайных букв:\n"
        "/gen <длина> <режим>\n"
        "  режимы: any (без разницы), nodigits (без цифр), digits (только с цифрами)\n"
        "  Пример: /gen 7 nodigits\n\n"
        "📖 Генерация только слов из словаря:\n"
        "/genw <длина>\n"
        "  Пример: /genw 7\n\n"
        "🔍 Проверка юзернейма:\n"
        "  Просто отправьте любой текст — бот проверит его как юзернейм")

@bot.message_handler(commands=['start'])
def old_bot(message):
    bot.reply_to(message, "Пришлите юзернейм для проверки (без @).\nПример: myusername")

@bot.message_handler(commands=['generate'])
def new_bot_help(message):
    bot.reply_to(message,
        "Команды генерации:\n"
        "/gen <длина> <режим> — случайные буквы\n"
        "  режимы: any, nodigits, digits\n"
        "/genw <длина> — только слова из словаря")

@bot.message_handler(commands=['gen'])
def handle_generate(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Укажите длину. Пример: /gen 7 nodigits")
            return
        length = int(parts[1])
        if length < 3 or length > 20:
            bot.reply_to(message, "Длина от 3 до 20.")
            return
        mode = "any"
        if len(parts) >= 3:
            m = parts[2].lower()
            if m in ["nodigits", "no_digits", "безцифр"]:
                mode = "no_digits"
            elif m in ["digits", "only_digits", "сцифрами"]:
                mode = "only_digits"
        candidates = generate_usernames(length, 30, mode)
        results = [check_generator(u) for u in candidates]
        sorted_results = sorted(results, key=lambda x: (not x['wordlike'], not x['available']))
        mode_names = {"any": "без разницы", "no_digits": "без цифр", "only_digits": "только с цифрами"}
        answer = f"🎲 Случайные буквы, длина {length} (режим: {mode_names[mode]}):\n\n"
        for idx, r in enumerate(sorted_results[:30], 1):
            status = "✅" if r['available'] else "❌"
            word_tag = " [СЛОВО]" if r['wordlike'] else ""
            answer += f"{idx}. @{r['username']} {status}{word_tag}\n"
        free = [r['username'] for r in results if r['available']]
        if free:
            answer += f"\n💡 Свободные: {', '.join('@'+u for u in free[:5])}"
        bot.reply_to(message, answer)
    except ValueError:
        bot.reply_to(message, "Ошибка. Пример: /gen 7 nodigits")

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
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)
