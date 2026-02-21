import socket
import json
import os
import re
import random
import sys
import threading
import time
from datetime import datetime

WORDS_FILE = "mad_lib_words.json"
GAMES_FILE = "mad_lib_games.json"
SENTENCES_FILE = "mad_lib_sentences.json"

DEFAULT_WORD_BANK = {
    "noun": [
        "apple", "astronaut", "avocado", "banana", "barrel", "beachball", "bicycle", "blender", "book", "boot",
        "boulder", "cactus", "camera", "candle", "canoe", "canyon", "carrot", "cat", "cave", "chef",
        "cloud", "coat", "computer", "cookie", "cow", "crayon", "crow", "cupcake", "cushion", "desert",
        "dog", "doll", "donut", "door", "dragon", "drum", "duck", "eagle", "egg", "elephant",
        "engine", "eyeball", "feather", "fence", "fish", "flag", "flamingo", "flashlight", "flower", "fork",
        "fridge", "frog", "galaxy", "game", "garden", "ghost", "giraffe", "glove", "goat", "guitar",
        "hamburger", "hammer", "hat", "helicopter", "hippo", "honey", "house", "iceberg", "igloo", "island",
        "jacket", "jellybean", "jungle", "kangaroo", "key", "kite", "kitchen", "ladder", "lamp", "leaf",
        "lemon", "lion", "lizard", "marble", "microwave", "mirror", "moon", "mouse", "muffin", "mushroom",
        "napkin", "ninja", "noodle", "notebook", "ocean", "octopus", "onion", "ostrich", "oven", "owl"
    ],
    "verb": [
        "admire", "argue", "assemble", "bake", "balance", "beam", "blink", "boil", "bounce", "break",
        "build", "burst", "cackle", "carry", "chase", "cheer", "clap", "climb", "collapse", "comb",
        "cook", "crawl", "cry", "dance", "dive", "doodle", "drag", "draw", "dream", "drink",
        "drive", "drop", "drum", "eat", "escape", "explore", "fall", "fight", "float", "fly",
        "fold", "gather", "giggle", "glide", "grab", "growl", "gulp", "hammer", "hide", "hike",
        "hop", "hug", "hunt", "hurry", "invent", "itch", "jog", "juggle", "jump", "kick",
        "kiss", "knock", "laugh", "launch", "lick", "lift", "listen", "march", "melt", "mimic",
        "mix", "mow", "nod", "open", "pack", "paint", "pat", "pet", "poke", "pop",
        "pour", "pull", "punch", "push", "quack", "race", "rest", "roar", "run", "sail",
        "scratch", "scream", "shake", "shiver", "shout", "sing", "skip", "slide", "smile", "spin"
    ],
    "adjective": [
        "adorable", "adventurous", "ancient", "angry", "anxious", "awkward", "bitter", "bizarre", "bouncy", "brave",
        "bright", "brilliant", "broken", "bumpy", "calm", "cheerful", "chilly", "chunky", "clever", "clumsy",
        "colorful", "confused", "cozy", "creepy", "crispy", "crunchy", "curly", "cute", "damp", "dangerous",
        "dark", "delightful", "dirty", "dusty", "eager", "elegant", "enormous", "excited", "faint", "fancy",
        "fast", "fat", "fierce", "filthy", "fluffy", "fragile", "frantic", "fuzzy", "gentle", "giggly",
        "glamorous", "gloomy", "goofy", "graceful", "greasy", "grumpy", "hairy", "handsome", "happy", "harsh",
        "heavy", "helpful", "hilarious", "hollow", "honest", "hot", "huge", "icy", "itchy", "jealous",
        "jolly", "juicy", "kind", "lame", "lazy", "light", "loud", "lovely", "lumpy", "magical",
        "messy", "mighty", "miniature", "moist", "muddy", "mysterious", "narrow", "nervous", "noisy", "odd",
        "old", "oily", "pleasant", "plump", "pointy", "prickly", "proud", "puffy", "quick", "quiet"
    ],
    "adverb": [
        "abruptly", "accidentally", "angrily", "anxiously", "awkwardly", "badly", "beautifully", "boldly", "bravely", "brightly",
        "briskly", "calmly", "carefully", "carelessly", "cautiously", "cheerfully", "clumsily", "confidently", "coolly", "crazily",
        "cruelly", "curiously", "daily", "daintily", "dangerously", "deliberately", "diligently", "dimly", "dizzily", "eagerly",
        "easily", "elegantly", "energetically", "enthusiastically", "evenly", "eventually", "exactly", "excitedly", "faintly", "faithfully",
        "fast", "ferociously", "fiercely", "fondly", "foolishly", "fortunately", "frantically", "freely", "frequently", "gently",
        "gladly", "gleefully", "gracefully", "greedily", "happily", "hastily", "honestly", "hopefully", "hungrily", "immediately",
        "innocently", "intensely", "interestingly", "jovially", "joyfully", "jubilantly", "kindly", "lazily", "lightly", "likely",
        "loudly", "loyally", "madly", "merrily", "mildly", "mysteriously", "nervously", "nicely", "noisily", "obediently",
        "oddly", "often", "openly", "painfully", "patiently", "playfully", "politely", "poorly", "powerfully", "promptly",
        "quickly", "quietly", "rapidly", "rarely", "really", "recklessly", "reluctantly", "repeatedly", "roughly", "rudely"
    ],
    "place": [
        "airport", "amusement park", "aquarium", "attic", "bakery", "balcony", "ball pit", "barn", "basement", "beach",
        "bedroom", "boat", "bookstore", "bouncy castle", "bridge", "cabin", "cafeteria", "campsite", "castle", "cave",
        "cemetery", "classroom", "closet", "cloud", "construction site", "cornfield", "cottage", "couch", "courthouse", "desert",
        "diner", "dungeon", "elevator", "factory", "farm", "fire station", "forest", "fountain", "garage", "garden",
        "gas station", "gym", "hallway", "hospital", "hotel", "houseboat", "igloo", "island", "jungle", "kitchen",
        "lake", "laundromat", "library", "lighthouse", "living room", "mall", "market", "meadow", "mine", "moon",
        "mountain", "museum", "ocean", "office", "outer space", "park", "parking lot", "pasture", "pet store", "pirate ship",
        "playground", "pond", "post office", "restaurant", "restroom", "river", "roof", "sandbox", "school", "sewer",
        "ship", "skate park", "skyscraper", "snowfield", "stadium", "stage", "station", "store", "submarine", "subway",
        "swamp", "swimming pool", "tent", "theater", "toilet", "tower", "train", "treehouse", "tunnel", "volcano"
    ]
}

DEFAULT_GAME_TEMPLATES = [
    {"template": "The {adjective} {noun} decided to {verb} {adverb} in the {place}.", "order": ["adjective", "noun", "verb", "adverb", "place"]},
    {"template": "Yesterday, a {adjective} {noun} tried to {verb} me at the {place}!", "order": ["adjective", "noun", "verb", "place"]},
    {"template": "If you {verb} too {adverb}, the {noun} might get {adjective}.", "order": ["verb", "adverb", "noun", "adjective"]},
    {"template": "The {noun} was so {adjective} it could barely {verb}.", "order": ["noun", "adjective", "verb"]},
    {"template": "I {verb}ed a {adjective} {noun} while walking through the {place}.", "order": ["verb", "adjective", "noun", "place"]},
    {"template": "The {place} was filled with {adjective} {noun}s that would {verb} {adverb}.", "order": ["place", "adjective", "noun", "verb", "adverb"]},
    {"template": "Nothing is more {adjective} than a {noun} trying to {verb}.", "order": ["adjective", "noun", "verb"]},
    {"template": "At the {place}, I met a {adjective} {noun} who could {verb} {adverb}.", "order": ["place", "adjective", "noun", "verb", "adverb"]},
    {"template": "Never {verb} a {adjective} {noun} inside the {place}.", "order": ["verb", "adjective", "noun", "place"]},
    {"template": "The {noun} {verb}ed into the {place} and vanished {adverb}.", "order": ["noun", "verb", "place", "adverb"]},

    {"template": "I {verb}ed so {adverb} that the {noun} became {adjective}.", "order": ["verb", "adverb", "noun", "adjective"]},
    {"template": "In the {place}, a {adjective} {noun} loves to {verb} {adverb}.", "order": ["place", "adjective", "noun", "verb", "adverb"]},
    {"template": "You should never {verb} a {noun} when it's {adjective}.", "order": ["verb", "noun", "adjective"]},
    {"template": "The {noun} {verb}ed {adverb} over the {adjective} {place}.", "order": ["noun", "verb", "adverb", "adjective", "place"]},
    {"template": "My best friend is a {adjective} {noun} who can {verb}.", "order": ["adjective", "noun", "verb"]},
    {"template": "We found a {noun} {verb}ing {adverb} behind the {place}.", "order": ["noun", "verb", "adverb", "place"]},
    {"template": "Can a {adjective} {noun} really {verb} {adverb}?", "order": ["adjective", "noun", "verb", "adverb"]},
    {"template": "The {place} was surprisingly full of {adjective} {noun}s.", "order": ["place", "adjective", "noun"]},
    {"template": "When I {verb}, the {noun} always gets {adjective}.", "order": ["verb", "noun", "adjective"]},
    {"template": "The {adjective} {noun} {verb}ed through the {place} {adverb}.", "order": ["adjective", "noun", "verb", "place", "adverb"]},

    {"template": "On the {place}, a {adjective} {noun} suddenly {verb}ed {adverb}.", "order": ["place", "adjective", "noun", "verb", "adverb"]},
    {"template": "My {noun} likes to {verb} {adverb} in the {place}.", "order": ["noun", "verb", "adverb", "place"]},
    {"template": "That {adjective} {noun} just can't stop {verb}ing.", "order": ["adjective", "noun", "verb"]},
    {"template": "After the {place} collapsed, the {noun} went completely {adjective}.", "order": ["place", "noun", "adjective"]},
    {"template": "I always {verb} when I see a {adjective} {noun}.", "order": ["verb", "adjective", "noun"]},
    {"template": "The {noun} slept {adverb} on top of the {adjective} {place}.", "order": ["noun", "adverb", "adjective", "place"]},
    {"template": "Some say a {adjective} {noun} can {verb} forever.", "order": ["adjective", "noun", "verb"]},
    {"template": "Why did the {noun} {verb} across the {place}?", "order": ["noun", "verb", "place"]},
    {"template": "I saw a {adjective} {noun} {verb}ing {adverb} today.", "order": ["adjective", "noun", "verb", "adverb"]},
    {"template": "The {noun} vanished into the {place} without a {adjective} sound.", "order": ["noun", "place", "adjective"]},
    {"template": "Even the {adjective} {noun} couldn't {verb} in the {place}.", "order": ["adjective", "noun", "verb", "place"]},

    {"template": "Once, I {verb}ed a {adjective} {noun} at the {place}.", "order": ["verb", "adjective", "noun", "place"]},
    {"template": "The {place} smelled like a {adjective} {noun}.", "order": ["place", "adjective", "noun"]},
    {"template": "Never trust a {adjective} {noun} to {verb} {adverb}.", "order": ["adjective", "noun", "verb", "adverb"]},
    {"template": "If it wasn't so {adjective}, I might {verb} the {noun}.", "order": ["adjective", "verb", "noun"]},
    {"template": "Every time I {verb}, the {place} explodes {adverb}.", "order": ["verb", "place", "adverb"]},
    {"template": "A {noun} once {verb}ed all over my {place}.", "order": ["noun", "verb", "place"]},
    {"template": "No one expected the {adjective} {noun} to {verb}.", "order": ["adjective", "noun", "verb"]},
    {"template": "The {noun} {verb}ed and {verb}ed again in the {place}.", "order": ["noun", "verb", "verb", "place"]},
    {"template": "At dawn, the {adjective} {noun} would always {verb} {adverb}.", "order": ["adjective", "noun", "verb", "adverb"]},
    {"template": "A {noun} in the {place} is worth two in the {place}.", "order": ["noun", "place", "place"]},

    {"template": "The {adjective} {noun} kept trying to {verb} even though it was {adverb}.", "order": ["adjective", "noun", "verb", "adverb"]},
    {"template": "Did you hear about the {noun} who {verb}ed through the {place}?", "order": ["noun", "verb", "place"]},
    {"template": "Why is that {noun} always {verb}ing {adverb} in my {place}?", "order": ["noun", "verb", "adverb", "place"]},
    {"template": "The {adjective} {place} made my {noun} {verb} uncontrollably.", "order": ["adjective", "place", "noun", "verb"]},
    {"template": "According to legend, a {adjective} {noun} lives in the {place}.", "order": ["adjective", "noun", "place"]},
    {"template": "Please {verb} the {adjective} {noun} by the {place}.", "order": ["verb", "adjective", "noun", "place"]},
    {"template": "Nothing beats a {noun} that knows how to {verb} {adverb}.", "order": ["noun", "verb", "adverb"]},
    {"template": "The {noun} came from the {place} and started {verb}ing {adverb}.", "order": ["noun", "place", "verb", "adverb"]},
    {"template": "Don't forget to {verb} your {adjective} {noun} before bed.", "order": ["verb", "adjective", "noun"]},
    {"template": "The {adjective} {noun} lives under the {place} and {verb}s nightly.", "order": ["adjective", "noun", "place", "verb"]},

    {"template": "My {place} was invaded by a {adjective} {noun} that {verb}ed {adverb}.", "order": ["place", "adjective", "noun", "verb", "adverb"]},
    {"template": "Every {noun} dreams of {verb}ing in the {adjective} {place}.", "order": ["noun", "verb", "adjective", "place"]},
    {"template": "Have you ever seen a {adjective} {noun} {verb} like that?", "order": ["adjective", "noun", "verb"]},
    {"template": "After the storm, we found a {noun} {verb}ing {adverb} in the {place}.", "order": ["noun", "verb", "adverb", "place"]},
    {"template": "The {noun} was too {adjective} to {verb} properly at the {place}.", "order": ["noun", "adjective", "verb", "place"]},
    {"template": "That {adjective} {noun} just {verb}ed my entire {place}!", "order": ["adjective", "noun", "verb", "place"]},
    {"template": "Please don’t {verb} the {noun} unless it’s {adjective}.", "order": ["verb", "noun", "adjective"]},
    {"template": "At the edge of the {place}, the {adjective} {noun} began to {verb}.", "order": ["place", "adjective", "noun", "verb"]},
    {"template": "A {noun} that {verb}s {adverb} is always {adjective}.", "order": ["noun", "verb", "adverb", "adjective"]},
    {"template": "No {noun} can {verb} {adverb} like a {adjective} one!", "order": ["noun", "verb", "adverb", "adjective"]}
]

# ========== JSON Utilities ==========
def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# ========== Learning ==========
def learn_template(template_str, word_order, games_db):
    for game in games_db:
        if game["template"] == template_str and game["order"] == word_order:
            return
    games_db.append({"template": template_str, "order": word_order})

def learn_from_story(template_str, word_order, filled_story, word_bank, games_db, sentence_log, source_ip):
    learn_template(template_str, word_order, games_db)
    template_id = games_db.index({"template": template_str, "order": word_order})
    regex_template = re.escape(template_str)
    for pos in word_order:
        regex_template = regex_template.replace(r'\{' + pos + r'\}', r'(.+?)')

    match = re.match(regex_template, filled_story)
    if not match:
        print("⚠️ Could not parse story:", filled_story)
        return

    words = match.groups()
    for pos, word in zip(word_order, words):
        if word not in word_bank.get(pos, []):
            print(f"📚 Learned new '{pos}': {word}")
            word_bank[pos].append(word)

    sentence_log.append({
        "story": filled_story,
        "from_ip": source_ip,
        "timestamp": datetime.now().isoformat(),
        "source_template": template_str,
        "template_id": template_id
    })

# ========== Story ==========
def fill_template(template_str, word_order, word_bank):
    story = template_str
    for pos in word_order:
        word = random.choice(word_bank.get(pos, ["???"]))
        story = story.replace(f"{{{pos}}}", word, 1)
    return story

# ========== Networking ==========
def send_message(sock, message, target_ip, port):
    sock.sendto(message.encode(), (target_ip, port))

def receive_message(sock):
    data, addr = sock.recvfrom(4096)
    return data.decode().strip(), addr

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

# ========== Cancel Listener ==========
stop_waiting = False
def keyboard_listener():
    global stop_waiting
    while not stop_waiting:
        key = sys.stdin.read(1)
        if key.lower() == "q":
            stop_waiting = True
            print("\n🛑 Quit requested. Exiting...")
            os._exit(0)

# ========== Forever Discovery ==========
def discover_partner(my_ip, port):
    print("🔍 Discovering partner (press 'q' to cancel)...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((my_ip, port))
    sock.settimeout(1)

    threading.Thread(target=keyboard_listener, daemon=True).start()

    start_time = time.time()

    while not stop_waiting:
        seconds = int(time.time() - start_time)
        print(f"\r⏳ Searching for partner... {seconds}s", end="", flush=True)

        try:
            # Broadcast HELLO
            message = f"HELLO:{my_ip}"
            sock.sendto(message.encode(), ("255.255.255.255", port))

            # Check if anyone replies
            data, addr = sock.recvfrom(1024)
            msg = data.decode()
            if msg.startswith("HELLO:"):
                partner_ip = msg.split(":")[1]
                if partner_ip != my_ip:
                    print(f"\n👋 Partner detected: {partner_ip}")
                    sock.sendto(f"CONFIRM:{my_ip}".encode(), (partner_ip, port))
                    return partner_ip, "generator"
            elif msg.startswith("CONFIRM:"):
                partner_ip = msg.split(":")[1]
                print(f"\n✅ Partner confirmed: {partner_ip}")
                return partner_ip, "teller"

        except socket.timeout:
            continue

    sock.close()
    sys.exit(1)

# ========== Game Loop ==========
def mad_libs_duel(my_ip, partner_ip, port, initial_role):
    role = initial_role
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_ip, port))
    print(f"\n🎮 Starting game as {role.upper()} on {my_ip}:{port} ↔ {partner_ip}:{port}")

    word_bank = load_json(WORDS_FILE, DEFAULT_WORD_BANK.copy())
    games_db = load_json(GAMES_FILE, DEFAULT_GAME_TEMPLATES.copy())
    sentence_log = load_json(SENTENCES_FILE, [])

    while True:
        if role == "teller":
            template_obj = random.choice(games_db)
            template_str = template_obj["template"]
            word_order = template_obj["order"]

            msg = f"TEMPLATE:{template_str}|ORDER:{','.join(word_order)}"
            send_message(sock, msg, partner_ip, port)
            print(f"\n🗣 Sent template:\n{template_str}")

            story, addr = receive_message(sock)
            if story.startswith("STORY:"):
                story_text = story[len("STORY:"):].strip()
                print(f"📖 Received filled story:\n{story_text}")
                learn_from_story(template_str, word_order, story_text, word_bank, games_db, sentence_log, addr[0])

        else:
            msg, addr = receive_message(sock)
            if msg.startswith("TEMPLATE:"):
                try:
                    template_str, order_str = msg[len("TEMPLATE:"):].split("|ORDER:")
                    word_order = order_str.split(",")
                    print(f"\n📜 Received template:\n{template_str}")
                except Exception as e:
                    print("Error parsing template:", e)
                    continue

                story_text = fill_template(template_str, word_order, word_bank)
                response = f"STORY:{story_text}"
                send_message(sock, response, partner_ip, port)
                print(f"📝 Sent filled story:\n{story_text}")
                learn_from_story(template_str, word_order, story_text, word_bank, games_db, sentence_log, my_ip)

        save_json(WORDS_FILE, word_bank)
        save_json(GAMES_FILE, games_db)
        save_json(SENTENCES_FILE, sentence_log)

        print("🔄 Swapping roles...\n")
        role = "generator" if role == "teller" else "teller"
        time.sleep(2)

# ========== Main ==========
def main():
    port = 12345
    print("🌐 Detecting local IP address...")
    my_ip = get_own_ip()
    print(f"📡 Your IP address: {my_ip}")

    partner_ip, initial_role = discover_partner(my_ip, port)
    mad_libs_duel(my_ip, partner_ip, port, initial_role)

if __name__ == "__main__":
    main()
