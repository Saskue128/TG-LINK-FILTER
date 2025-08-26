# main.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from flask import Flask
import threading
import re
import os
import time
import sys

# ---------- Environment vars ----------
try:
    API_ID = int(os.environ.get("API_ID", "0"))
except:
    API_ID = 0
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

if not (API_ID and API_HASH and BOT_TOKEN):
    print("ERROR: API_ID, API_HASH or BOT_TOKEN missing in environment variables.", file=sys.stderr)
    # don't exit here; still start flask so Render sees a port (helps debugging)
    
# ---------- Link regex ----------
LINK_REGEX = r"(https?://|www\.|t\.me/)"

# ---------- Pyrogram bot ----------
bot = Client(
    "anti_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

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
                    InlineKeyboardButton("📢 Join Our Channel for update", url="https://t.me/link_remover_au_support"),
                    InlineKeyboardButton("💬 Support Group", url="https://t.me/AU_ANIMES_COMMUNITY"),
                ],
                [
                    InlineKeyboardButton("➕ Add Me to Your Group", url="https://t.me/AU_LINK_REMOVER_BOT?startgroup=true"),
                ]
            ]
        )
    )

@bot.on_message(filters.private & filters.command("help"))
async def help_handler(client, message):
    await message.reply(
        "**🆘 Help - Link Remover Bot**\n\n"
        "👋 Main ek simple sa **Link Remover Bot** hoon.\n\n"
        "🔷 Jab koi normal user group me link bhejta hai, to main us message ko **automatic delete** kar deta hoon.\n"
        "🔶 Lekin group ke **admins** ko link bhejne ki full permission hai.\n\n"
        "❗ Bas mujhe apne group me **add** karo aur **admin** bana do. Baaki sab main sambhal lunga. 😎"
    )

@bot.on_message(filters.private & filters.command("about"))
async def about_handler(client, message):
    await message.reply(
        "**🤖 About this Bot**\n\n"
        "This is an advanced anti-link Telegram bot built using Pyrogram.\n\n"
        "🔹 Deletes links from non-admins in groups.\n"
        "🔹 Clean, fast, and easy to use.\n"
        "🔹 Designed to protect your group from spam.\n\n"
        "👨‍💻 Developer: [@Leave_me_alone_12](https://t.me/Leave_me_alone_12)\n"
        "⚡️ Powered by: [@AU_ANIMES](https://t.me/AU_ANIMES)",
        disable_web_page_preview=True
    )

@bot.on_message(filters.group & filters.text)
async def delete_links(client: Client, message: Message):
    # Agar message me link nahi hai to return
    if not message.text:
        return
    if not re.search(LINK_REGEX, message.text):
        return
    try:
        # check karte hain user admin hai ya nahi
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
        await message.delete()
    except Exception as e:
        # Logging error to stdout/stderr so Render logs me dikhe
        print(f"Error checking admin status or deleting message: {e}", file=sys.stderr)

# ---------- Flask dummy server ----------
web_app = Flask(__name__)

@web_app.route('/', methods=["GET"])
def home():
    return "Anti-Link Bot is running! (Flask dummy server)"

def run_flask():
    # Render provides PORT env var
    port = int(os.environ.get("PORT", 5000))
    # use 0.0.0.0 so Render can bind externally
    web_app.run(host="0.0.0.0", port=port)

# ---------- Runner ----------
def run_bot():
    print("🤖 Bot is starting...", flush=True)
    try:
        # This will block and run the bot
        bot.run()
    except Exception as e:
        print(f"Bot stopped with error: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Start Flask in a daemon thread so it doesn't block
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    # small sleep to let flask bind the port fast (optional)
    time.sleep(0.5)
    # Run the bot (blocking)
    run_bot()
