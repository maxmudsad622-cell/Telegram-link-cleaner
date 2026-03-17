import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")

URL_PATTERN = re.compile(
    r'(https?://\S+|www\.\S+|t\.me/\S+|@\w+)',
    re.IGNORECASE
)

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return
    
    text = message.text or message.caption or ""
    
    if message.new_chat_members or message.left_chat_member:
        await message.delete()
        return
    
    if URL_PATTERN.search(text):
        await message.delete()
        try:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"⚠️ {message.from_user.first_name}, havolalar yuborishga ruxsat yo'q!"
            )
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, delete_links))
app.run_polling()
