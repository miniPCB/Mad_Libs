# 🧠 Mad Libs Duel - Self-Learning LAN Game

**Mad Libs Duel** is a Python-based game where two computers (e.g., desktop & Raspberry Pi) automatically discover each other on a local network and play Mad Libs back and forth — forever.

It features auto-discovery, role-swapping, vocabulary learning, and logging of every sentence ever created.

---

## 🚀 Features

- 🔄 **Automatic role swapping** (Story Teller & Word Generator)
- 🌐 **LAN auto-discovery** using UDP broadcasts (no IP config needed)
- 🧠 **Self-learning**:
  - Builds a word bank from gameplay
  - Learns new sentence templates
  - Stores every completed sentence with metadata
- 📄 Fully JSON-driven:
  - `mad_lib_words.json`: all known words by category
  - `mad_lib_games.json`: reusable sentence structures
  - `mad_lib_sentences.json`: every generated sentence
- 🧹 Modular and easy to extend
- 🢨 Cancel partner discovery with `q`

---

## 🗂 File Structure

```
.
├── mad_libs.py                 # The main game script
├── mad_lib_words.json          # Word bank (learned)
├── mad_lib_games.json          # Sentence templates (learned)
├── mad_lib_sentences.json      # Completed sentences log
```

---

## 🧪 How to Run

> ✅ Python 3.8+

### On both machines:
```bash
python3 mad_libs.py
```

That’s it! No IPs or ports required — just be on the same network.

---

## 🧠 How It Works

- Each device broadcasts `HELLO:<ip>` over the LAN
- If it receives a `HELLO` from another device, it responds with `CONFIRM:<ip>`
- The device that sent `HELLO` becomes the **Generator**, and the responder becomes the **Teller**
- After every round, roles swap

---

## 🧾 Data Files

- **`mad_lib_words.json`**
  - Categories: `noun`, `verb`, `adjective`, `adverb`, `place`
  - Grows as new words are extracted from stories

- **`mad_lib_games.json`**
  - Templates with `{placeholders}` and `order` arrays
  - Allows reuse and learning of structures

- **`mad_lib_sentences.json`**
  - Log of all generated sentences with:
    - `story`, `from_ip`, `timestamp`, `source_template`, `template_id`

---

## ❓ Example Sentence Template

```json
{
  "template": "The {adjective} {noun} decided to {verb} {adverb} in the {place}.",
  "order": ["adjective", "noun", "verb", "adverb", "place"]
}
```

---

## ✨ Example Sentence

> "The fuzzy toaster decided to explode awkwardly in the kitchen."

---

## 🔧 Customize

- Add more templates to `mad_lib_games.json`
- Expand your word bank with new categories
- Add a GUI or TTS for Raspberry Pi
- Build an HTML log viewer for completed stories

---

## 📦 TODO / Ideas

- Multiplayer support (more than 2 devices)
- Word frequency stats
- Sentence quality scoring
- Story narration mode (TTS)
- Game mode: battle of the adjectives 😄

---

## 🦮 Credits

Built with Python. Inspired by Mad Libs. Supercharged with self-learning.

Enjoy your LAN-powered comedy machine 🤖✍️

