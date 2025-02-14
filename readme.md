# 📥 Telegram File Downloader Bot

A **Python-based Telegram bot** that allows users to **send media files (videos, documents, etc.)** via Telegram and automatically downloads them with real-time progress updates. This bot uses **Telethon (Telegram App API)** for **fast and secure downloads up to 2GB**.

---

## ✨ Features
✅ Supports **files up to 2GB**  
✅ **Extracts the correct filename** from Telegram messages  
✅ **Shows download progress** (in MB and percentage)  
✅ **Sends a startup message** to the bot owner  
✅ **Logs success and errors** for debugging  
✅ **Runs in Docker (optional)**  

---

## 📌 Requirements
- **Python 3.8+**
- **Telegram App API Credentials**
- **A Telegram Bot Token (from BotFather)**

---

## 🔧 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/YOUR_USERNAME/telegram-file-downloader.git
cd telegram-file-downloader
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Get Telegram API Credentials**
- Go to [my.telegram.org](https://my.telegram.org/)
- Sign in and **create a new application**
- Copy your **API ID** and **API HASH**

### **4️⃣ Get a Telegram Bot Token**
- Open [BotFather](https://t.me/BotFather) on Telegram  
- Create a new bot and copy the **bot token**

### **5️⃣ Get Your Telegram User ID**
- Open [`@userinfobot`](https://t.me/userinfobot) on Telegram  
- Start the bot and copy your **User ID**

---

## 📁 Configuration (Setting up `.env`)
Create a `.env` file in the same directory and add:
```ini
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_ID
DOWNLOAD_FOLDER=downloads
SESSION_NAME=bot_session
```

Replace values with your **API credentials and Telegram ID**.

---

## 🚀 Running the Bot
```sh
python telegram_file_downloader.py
```

### **🎯 What Happens?**
1. The bot **sends a startup message** to the OWNER_ID:
   ```
   ✅ Bot is running and ready to receive files!
   ```
2. Users can **send media files (videos, documents, etc.)**.
3. The bot **downloads files with progress updates**:
   ```
   ⬇️ Downloading: 12.34/100.00 MB (12.34%)
   ✅ Download complete: video.mp4
   ```
4. All files are **saved in the `downloads/` folder**.

---

