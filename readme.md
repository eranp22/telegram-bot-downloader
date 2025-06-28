# 📥 Telegram File Downloader Bot

A **Python-based Telegram bot** that allows users to **send media files (videos, documents, etc.)** via Telegram and automatically downloads them with real-time progress updates. This bot uses **Telegram Bot API** for **secure and efficient downloads**.

---

## ✨ Features
✅ Supports **files up to 2GB**  
✅ **Extracts the correct filename** from Telegram messages  
✅ **Sends a startup message** to the bot owner  
✅ **Logs success and errors** for debugging  
✅ **Runs in Docker** for easy deployment  

---

## 📌 Requirements
- **Python 3.8+**
- **Docker (optional)**
- **A Telegram Bot Token (from BotFather)**

---

## 🔧 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/eranp22/telegram-bot-downloader.git
cd telegram-bot-downloader
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Get a Telegram Bot Token**
- Open [BotFather](https://t.me/BotFather) on Telegram  
- Create a new bot and copy the **bot token**

### **4️⃣ Get Your Telegram User ID**
- Open [`@userinfobot`](https://t.me/userinfobot) on Telegram  
- Start the bot and copy your **User ID**

---

## 📁 Configuration (Setting up `.env`)
Create a `.env` file in the same directory and add:
```ini
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_ID
TELEGRAM_API_ID=YOUR_API_ID  # Added API ID
TELEGRAM_API_HASH=YOUR_API_HASH  # Added API Hash
DOWNLOAD_FOLDER=/videos
VOLUME_SOURCE=/absolute/path/to/volume
```

Replace values with your **bot token**, Telegram ID, API ID, API Hash, and desired download folder path.

---

## 🚀 Running the Bot

### **Option 1: Run Locally**
```sh
python telegram-file-downloader.py
```

### **Option 2: Run with Docker**
1. Build and start the Docker container:
   ```sh
   docker-compose up --build
   ```
2. The bot will start and listen for incoming files.

---

## 🎯 What Happens?
1. The bot **sends a startup message** to the OWNER_ID:
   ```
   🤖 Bot is starting up...
   ```
2. Users can **send media files (videos, documents, etc.)**.
3. The bot **downloads files** and sends feedback:
   ```
   ✅ File downloaded: video.mp4
   ```
4. All files are **saved in the specified folder**.

---

## 🐳 Docker Configuration
The bot can run inside a Docker container for easier deployment. The `compose.yml` file binds the download folder to a Docker volume.

### Example `.env` for Docker:
```ini
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_ID
TELEGRAM_API_ID=YOUR_API_ID  # Added API ID
TELEGRAM_API_HASH=YOUR_API_HASH  # Added API Hash
VOLUME_SOURCE=/absolute/path/to/volume
DOWNLOAD_FOLDER=/videos
```

Ensure the `VOLUME_SOURCE` points to a valid directory on your host machine.

---

