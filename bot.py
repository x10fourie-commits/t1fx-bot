import time
import requests
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= CONFIG =================
TOKEN = "8569688371:AAEIOuOVwJLz8Px4GlIBTP3s7esV7PwYm5c"
CHAT_ID = "-1003980807358"
YOUTUBE_CHANNEL_ID = "UC71kfIKc7B0WoKFOP9xkkVg"

last_video_id = None

# ================= TELEGRAM HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 TEST LIVE ALERT", callback_data="test")]
    ]

    await update.message.reply_text(
        "🔥 BOT IS ONLINE",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "test":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="🔴 TEST ALERT WORKING"
        )

# ================= YOUTUBE WATCHER =================

def youtube_watcher(app):
    global last_video_id

    while True:
        try:
            url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
            r = requests.get(url, timeout=10)

            if "<yt:videoId>" in r.text:
                video_id = r.text.split("<yt:videoId>")[1].split("</yt:videoId>")[0]

                if video_id != last_video_id:
                    last_video_id = video_id
                    link = f"https://www.youtube.com/watch?v={video_id}"

                    app.create_task(
                        app.bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"🔴 NEW VIDEO LIVE!\n{link}"
                        )
                    )

                    print("LIVE ALERT SENT")

        except Exception as e:
            print("Watcher error:", e)

        time.sleep(60)

# ================= START BOT =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

threading.Thread(target=youtube_watcher, args=(app,), daemon=True).start()

app.run_polling()