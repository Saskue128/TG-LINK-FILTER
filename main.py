# main.py
import os
import re
import sys
import time
import threading
import logging
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

# ---------- Logging setup ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------- Environment vars ----------
try:
    API_ID = int(os.environ.get("API_ID", "0"))
except:
    API_ID = 0
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

if not (API_ID and API_HASH and BOT_TOKEN):
    logging.error("❌ API_ID, API_HASH or BOT_TOKEN missing in environment variables!")
    sys.exit(1)

# ---------- Link regex ----------
LINK_REGEX = r"(https?://|www\.|t\.me/)"

# ---------- Pyrogram bot ----------
bot = Client(
    "anti_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------- Handlers ----------
@bot.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await message.reply(
        "**👋 Welcome to the Anti-Link Bot!**\n\n"
        "This bot helps keep your group clean by deleting links sent by non-admin users.\n\n"
        "🔷 Only admins can share links.\n"
        "🔶 Add me to your group and make me admin to activate.\n\n"
        "**Choose an option below 👇**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📢 Updates", url="https://t.me/link_remover_au_support"),
                    InlineKeyboardButton("💬 Support", url="https://t.me/AU_ANIMES_COMMUNITY"),
                ],
                [
                    InlineKeyboardButton("➕ Add Me to Group", url="https://t.me/AU_LINK_REMOVER_BOT?startgroup=true"),
                ]
            ]
        )
    )

@bot.on_message(filters.private & filters.command("help"))
async def help_handler(client, message):
    await message.reply(
        "**🆘 Help - Link Remover Bot**\n\n"
        "🔷 Normal users agar link bhejenge → message delete hoga.\n"
        "🔶 Admins links bhej sakte hain.\n\n"
        "❗ Bas mujhe group me add karo aur admin rights do."
    )

@bot.on_message(filters.private & filters.command("about"))
async def about_handler(client, message):
    await message.reply(
        "**🤖 About this Bot**\n\n"
        "🔹 Deletes links from non-admins in groups.\n"
        "🔹 Fast and simple.\n\n"
        "👨‍💻 Developer: [@Leave_me_alone_12](https://t.me/Leave_me_alone_12)\n"
        "⚡ Powered by: [@AU_ANIMES](https://t.me/AU_ANIMES)",
        disable_web_page_preview=True
    )

@bot.on_message(filters.group & filters.text)
async def delete_links(client: Client, message: Message):
    if not message.text:
        return
    if not re.search(LINK_REGEX, message.text):
        return
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
        await message.delete()
        logging.info(f"🗑 Deleted link message from {message.from_user.id} in {message.chat.id}")
    except Exception as e:
        logging.error(f"Error checking admin status or deleting message: {e}")

# ---------- Flask dummy server ----------
web_app = Flask(__name__)

@web_app.route('/', methods=["GET"])
def home():
    return "✅ Anti-Link Bot is running! (Flask dummy server)"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)

# ---------- Runner ----------
def run_bot():
    logging.info("🤖 Bot is starting...")
    try:
        bot.start()
        me = bot.get_me()
        logging.info(f"✅ Bot started successfully as @{me.username}")
        bot.run()
    except Exception as e:
        logging.error(f"❌ Bot stopped with error: {e}", exc_info=True)

if __name__ == "__main__":
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(0.5)
    # Run Telegram bot
    run_bot()
