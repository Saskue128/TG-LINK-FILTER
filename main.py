from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
import re, os

API_ID = int(os.getenv("24696910"))
API_HASH = os.getenv("e1481c43ffade210467184b95fcc5d6f")
BOT_TOKEN = os.getenv("7644137923:AAHA-5XvyZ_SOF3x1vKW33IEgNU05-kYll0")

LINK_REGEX = r"(https?://|www\.|t\.me/)"

app = Client(
    "anti_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

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
                    InlineKeyboardButton("📢 Join Our Channel for update", url="https://t.me/link_remover_au_support"),
                    InlineKeyboardButton("💬 Support Group", url="https://t.me/AU_ANIMES_COMMUNITY"),
                ],
                [
                    InlineKeyboardButton("➕ Add Me to Your Group", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true"),
                ]
            ]
        )
    )

@app.on_message(filters.private & filters.command("help"))
async def help_handler(client, message):
    await message.reply(
        "**🆘 Help - Link Remover Bot**\n\n"
        "👋 Main ek simple sa **Link Remover Bot** hoon.\n\n"
        "🔷 Jab koi normal user group me link bhejta hai, to main us message ko **automatic delete** kar deta hoon.\n"
        "🔶 Lekin group ke **admins** ko link bhejne ki full permission hai.\n\n"
        "❗ Bas mujhe apne group me **add** karo aur **admin** bana do. Baaki sab main sambhal lunga. 😎"
    )

@app.on_message(filters.private & filters.command("about"))
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

print("🤖 Bot is running...")
app.run()
