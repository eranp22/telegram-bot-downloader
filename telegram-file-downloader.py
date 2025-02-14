import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # Your Telegram ID to receive startup message
SESSION_NAME = os.getenv("SESSION_NAME", "bot_session")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "downloads")

# Ensure download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Logging Configuration
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize the Telegram Bot Client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def progress_callback(received_bytes, total_bytes, progress_message):
    """ Show real-time download progress in MB and % """
    percent = (received_bytes / total_bytes) * 100
    received_mb = received_bytes / (1024 * 1024)
    total_mb = total_bytes / (1024 * 1024)
    
    progress_text = f"⬇️ Downloading: {received_mb:.2f}/{total_mb:.2f} MB ({percent:.2f}%)"
    await progress_message.edit(progress_text)

@client.on(events.NewMessage)
async def handle_media(event):
    if event.message.file:
        try:
            # Get file name
            file_name = "unknown_file"
            if event.message.media and event.message.media.document and event.message.media.document.attributes:
                for attr in event.message.media.document.attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        file_name = attr.file_name

            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            # Send progress message
            progress_message = await event.reply("⏳ Starting download...")

            # Download with progress callback
            await event.message.download_media(file_path, progress_callback=lambda r, t: progress_callback(r, t, progress_message))

            # Notify user after completion
            await progress_message.edit(f"✅ Download complete: {file_name}")
            logging.info(f"Success: {file_name} downloaded.")

        except Exception as e:
            await event.reply("❌ An error occurred while processing the file.")
            logging.error(f"Error: {str(e)}")

async def send_startup_message():
    """ Send a startup message to the bot owner when the bot starts """
    try:
        await client.send_message(OWNER_ID, "✅ Bot is running and ready to receive files!")
        logging.info("Startup message sent to owner.")
    except Exception as e:
        logging.error(f"Failed to send startup message: {str(e)}")

async def main():
    await send_startup_message()
    print("Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
