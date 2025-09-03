import os
import re
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

# ================== Config ==================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

LINK_REGEX = r"(https?://|www\.|t\.me/)"

# Flask App
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "✅ Bot is alive!"

# Pyrogram Client
app = Client(
    "anti_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================== Handlers ==================
@app.on_message(filters.private & filters.command("start"))
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
                    InlineKeyboardButton("📢 Channel", url="https://t.me/link_remover_au_support"),
                    InlineKeyboardButton("💬 Support", url="https://t.me/AU_ANIMES_COMMUNITY"),
                ],
                [
                    InlineKeyboardButton("➕ Add Me", url="https://t.me/AU_LINK_REMOVER_BOT?startgroup=true"),
                ]
            ]
        )
    )

@app.on_message(filters.group & filters.text)
async def delete_links(client: Client, message: Message):
    if not re.search(LINK_REGEX, message.text):
        return
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
        await message.delete()
    except Exception as e:
        print(f"Error checking admin status: {e}")

# ================== Runner ==================
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🤖 Starting bot...")
    threading.Thread(target=run_flask).start()  # Flask background me chalega
    app.run()  # Pyrogram ek hi baar chalega
