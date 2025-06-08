import os
import logging
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/videos")  # Path inside Docker volume
OWNER_ID = os.getenv("OWNER_ID")  # Optional
BASE_URL = f"http://localhost:8081/bot{BOT_TOKEN}/"
FILE_BASE_URL = f"http://localhost:8081/file/bot{BOT_TOKEN}/"

# Ensure download folder exists
#os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def get_updates(session, offset=None):
    """
    Fetch updates from the Telegram Bot API using long polling.
    This function retrieves new messages or events sent to the bot.
    """
    url = BASE_URL + "getUpdates"
    params = {"timeout": 10}
    if offset is not None:
        params["offset"] = offset
    try:
        async with session.get(url, params=params) as resp:
            return await resp.json()
    except Exception as e:
        logging.error(f"Failed to get updates: {e}")
        return {}

async def get_file_info(session, file_id):
    """
    Retrieve file information (e.g., file path) from the Telegram Bot API.
    This function is used to get metadata about a file, such as its location on the server.
    """
    # Use GET with query parameters instead of POST
    url = BASE_URL + "getFile"
    params = {"file_id": file_id}
    try:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            if data.get("ok"):
                return data["result"]
            else:
                logging.error(f"getFile failed: {data}")
                return None
    except Exception as e:
        logging.error(f"Error calling getFile: {e}")
        return None

async def download_file(session, file_id):
    """
    Download a file from the Telegram Bot API using the file path.
    This function fetches the file from the server and saves it locally.
    """
    file_info = await get_file_info(session, file_id)
    if not file_info:
        logging.error("❌ No file info received.")
        return None

    file_path_api = file_info.get("file_path")
    if not file_path_api:
        logging.error("❌ Missing file_path.")
        return None
    logging.info(f"📥 File path: {file_path_api}")  

    # Build full download URL using /file API
    file_url = f"{FILE_BASE_URL}{file_path_api.lstrip('/')}"
    logging.info(f"🌐 Constructed file URL: {file_url}")  # Log the constructed URL
    
    # Ensure BOT_TOKEN is sanitized and resolved correctly
    resolved_bot_token = BOT_TOKEN.replace("$", "").strip()
    if not resolved_bot_token:
        logging.error("❌ BOT_TOKEN is invalid or missing.")
        return None

    # Update local filename to use VOLUME_SOURCE\\resolved_bot_token\\videos
    sanitized_token = "".join(c if c.isalnum() else "_" for c in BOT_TOKEN)
    sanitized_filename = os.path.basename(file_path_api).replace(":", "_").replace("\\", "_").replace("/", "_")
    volume_source = os.getenv("VOLUME_SOURCE").replace("/", "\\")

    local_filename = os.path.join(volume_source, sanitized_token, "videos", sanitized_filename)
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    
    try:
        async with session.get(file_url) as resp:
            # Log the HTTP status code for debugging
            logging.info(f"HTTP status code: {resp.status}")
            
            # Check if the response is valid
            if resp.status != 200:
                # raise Exception(f"Download failed: HTTP {resp.status}")
                # check if the file local_filename exists on the server
                if not os.path.exists(local_filename):
                    logging.error(f"❌ Download failed: HTTP {resp.status} - File not found on server.")
                    raise Exception(f"Download failed: HTTP {resp.status}")
            
            # Proceed with download
            with open(local_filename, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        logging.info(f"✅ Downloaded: {local_filename}")
        if OWNER_ID:
            await send_message(session, OWNER_ID, f"✅ File downloaded: {local_filename}")        
        
        return local_filename
    except Exception as e:
        logging.error(f"Download error: {e}")
        return None

async def send_message(session, chat_id, text):
    """
    Send a text message to a specific chat using the Telegram Bot API.
    This function allows the bot to communicate with users by sending messages.
    """
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        async with session.post(url, json=payload) as resp:
            return await resp.json()
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return None

async def process_updates(session, updates):
    """
    Process incoming updates, handle file downloads, and send responses.
    This function processes new messages or events, detects files, downloads them, and sends feedback to users.
    """
    last_update_id = None
    for update in updates.get("result", []):
        update_id = update.get("update_id")
        if update_id is not None:
            last_update_id = update_id

        message = update.get("message")
        if not message:
            continue

        chat_id = message.get("chat", {}).get("id")
        file_id = None

        if "video" in message:
            file_id = message["video"].get("file_id")
        elif "document" in message:
            file_id = message["document"].get("file_id")

        if file_id:
            logging.info(f"📦 File detected: {file_id}")
            await send_message(session, chat_id, "📥 Downloading your file...")            
            downloaded = await download_file(session, file_id)
            if downloaded:
                await send_message(session, chat_id, f"✅ Downloaded: {os.path.basename(downloaded)}")
            else:
                await send_message(session, chat_id, "❌ Failed to download the file.")
    return last_update_id

async def async_main():
    """
    Main function to start the bot, poll for updates, and process them.
    This function initializes the bot, starts polling for updates, and handles them in a loop.
    """
    offset = None
    async with aiohttp.ClientSession() as session:
        logging.info("🤖 Bot is running...")
        if OWNER_ID:
            await send_message(session, OWNER_ID, "🤖 Bot is starting up..."
                               )        

        while True:
            try:
                updates = await get_updates(session, offset)
                if updates.get("result"):
                    last_update_id = await process_updates(session, updates)
                    if last_update_id:
                        offset = last_update_id + 1
                await asyncio.sleep(1)
            except Exception as e:
                logging.error(f"Polling error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    """
    Entry point of the script. Runs the bot asynchronously.
    """
    asyncio.run(async_main())
