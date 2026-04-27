import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "PUT_NEW_TOKEN_HERE"
CHANNEL_ID = "-1003980807358"
YOUTUBE_CHANNEL_ID = "UC71kfIKc7B0WoKFOP9xkkVg"

last_video_id = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔴 LIVE TEST", callback_data="live_test")]]

    await update.message.reply_text(
        "🔥 T1FX BOT ACTIVE",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "live_test":
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="🔴 TEST LIVE ALERT"
        )


def check_youtube(bot):
    global last_video_id

    while True:
        try:
            url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
            r = requests.get(url)

            if "<yt:videoId>" in r.text:
                video_id = r.text.split("<yt:videoId>")[1].split("</yt:videoId>")[0]

                if video_id != last_video_id:
                    last_video_id = video_id

                    link = f"https://www.youtube.com/watch?v={video_id}"

                    bot.loop.create_task(
                        bot.bot.send_message(
                            chat_id=CHANNEL_ID,
                            text=f"🔴 AUTO LIVE DETECTED\n{link}"
                        )
                    )

                    print("LIVE ALERT SENT")

        except Exception as e:
            print("Error:", e)

        time.sleep(60)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("button", button_handler))
app.add_handler(CallbackQueryHandler(button_handler))

# start watcher properly
import threading
threading.Thread(target=check_youtube, args=(app,), daemon=True).start()

app.run_polling()