import threading
import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= CONFIG =================
TOKEN = "8569688371:AAHjASWCde41JtYq_9ayAqE_d19VVP-Tr4I"
CHANNEL_ID = "-1003980807358"
YOUTUBE_CHANNEL_ID = "UC71kfIKc7B0WoKFOP9xkkVg"

bot = Bot(token=TOKEN)

# ================= TELEGRAM BOT =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 LIVE ALERT TEST", callback_data="live_test")]
    ]

    await update.message.reply_text(
        "🔥 T1FXTEAM CONTROL PANEL 🔥\n\n"
        "System is ACTIVE",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "live_test":
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="🔴 TEST LIVE ALERT SENT"
        )

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /live <youtube link>")
        return

    link = context.args[0]

    message = (
        "🔴 WE ARE LIVE NOW!\n\n"
        f"{link}"
    )

    await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
    await update.message.reply_text("✅ Sent")

# ================= LIVE WATCHER (BACKGROUND) =================

last_video_id = None

def live_watcher():
    global last_video_id

    while True:
        print("Checking YouTube...")
        try:
            url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
            r = requests.get(url)
            data = r.text

            if "<yt:videoId>" in data:
                video_id = data.split("<yt:videoId>")[1].split("</yt:videoId>")[0]

                if video_id != last_video_id:
                    last_video_id = video_id

                    live_link = f"https://www.youtube.com/watch?v={video_id}"

                    bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=(
                            "🔴 AUTO LIVE DETECTED!\n\n"
                            f"{live_link}"
                        )
                    )

                    print("LIVE ALERT SENT")

        except Exception as e:
            print("Watcher error:", e)

        time.sleep(60)

# ================= START WATCHER THREAD =================
threading.Thread(target=live_watcher, daemon=True).start()

# ================= START BOT =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", live))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()