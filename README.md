<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-Telegram%20Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

</div>


# 🗑️ Save-Send-TG Bot

**Your personal "black box" for Telegram**  
Instantly forwards deleted messages, media, and voice notes directly to your private chat.

</div>

---

## ⚡ About

**Save-Send-TG** is a powerful bot utilizing the **Telegram Business API** to monitor your personal chats.  
It acts as a logger: saving all incoming messages to a local database and instantly forwarding them to you if the sender deletes them.

> ⚠️ **Note:** A Telegram Premium subscription is required to use Telegram Business features.

---

## 🚀 Features

- 🕵️‍♂️ **Captures everything** — text, photos, videos, GIFs, stickers, audio  
- 🗣️ **Voice & video notes protection** — bypasses forwarding restrictions  
- 💾 **Full archive** — incoming + outgoing messages  
- 🌍 **Multi-language** — English, Russian, Ukrainian  
- ⚙️ **Flexible settings** — `/start` interactive menu  
- 📤 **Data export** — deleted or full history to `.txt`  
- 🚨 **Emergency wipe** — instant database cleanup  
- 🔒 **Privacy-focused** — local SQLite database only  

---

## 🛠️ Installation & Setup

### 1. Prerequisites

- Python **3.10+**

### 2. Clone repository

```bash
git clone https://github.com/apvcode/Save-Send-TG.git
cd Save-Send-TG
```

### 3. Create virtual environment (recommended)

```bash
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configuration

Open `conf.py` and insert your bot token:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
```

*(Optional)* Set your numeric Telegram ID in `ADMIN_ID`.

---

### 6. Run the bot

```bash
python main.py
```

---

## 📲 How to connect Telegram Business

1. Start the bot:
```bash
python main.py
```

2. Open Telegram → **Settings → Telegram Business**
3. Go to **Chat Bots**
4. Add your bot and grant permissions
5. Done 🎉

---

## 📸 Screenshots

- Settings Menu  
- Deleted Message Notification  

---

## ⚠️ Disclaimer

This tool is intended **for personal archiving only**.  
Please respect others' privacy.  
The developer is **not responsible** for misuse.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/apvcode">ApvCode</a>
</div>
