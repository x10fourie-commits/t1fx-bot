import time
import threading
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= CONFIG =================
TOKEN = "8569688371:AAEwSB1zHPPmu1Y5cITPfTXivBOukx1eXV4"
CHANNEL_ID = "-1003980807358"
YOUTUBE_CHANNEL_ID = "UC71kfIKc7B0WoKFOP9xkkVg"

last_video_id = None

# ================= START COMMAND =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 TEST LIVE ALERT", callback_data="test_live")]
    ]

    await update.message.reply_text(
        "🔥 BOT IS ACTIVE 🔥\n\nEverything is running.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= BUTTON =================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "test_live":
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="🔴 TEST LIVE ALERT WORKING"
        )

# ================= MANUAL LIVE COMMAND =================

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /live <youtube link>")
        return

    link = context.args[0]

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"🔴 LIVE NOW!\n{link}"
    )

    await update.message.reply_text("Sent ✅")

# ================= YOUTUBE WATCHER =================

def youtube_watcher(app):
    global last_video_id

    while True:
        try:
            print("Checking YouTube...")

            url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
            r = requests.get(url, timeout=10)

            if "<yt:videoId>" in r.text:
                video_id = r.text.split("<yt:videoId>")[1].split("</yt:videoId>")[0]

                if video_id != last_video_id:
                    last_video_id = video_id

                    link = f"https://www.youtube.com/watch?v={video_id}"

                    app.create_task(
                        app.bot.send_message(
                            chat_id=CHANNEL_ID,
                            text=f"🔴 AUTO LIVE DETECTED!\n{link}"
                        )
                    )

                    print("LIVE ALERT SENT")

        except Exception as e:
            print("Watcher error:", e)

        time.sleep(60)

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT STARTED")

    threading.Thread(target=youtube_watcher, args=(app,), daemon=True).start()

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()