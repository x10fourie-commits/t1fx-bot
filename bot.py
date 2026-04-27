import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

YOUTUBE_CHANNEL_ID = "UC71kfIKc7B0WoKFOP9xkkVg"

bot = Bot(token=TOKEN)

last_video = None

def check_youtube():
    global last_video

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
    r = requests.get(url)

    if "yt:videoId" in r.text:
        video_id = r.text.split("yt:videoId>")[1].split("<")[0]

        if video_id != last_video:
            last_video = video_id
            link = f"https://www.youtube.com/watch?v={video_id}"

            bot.send_message(chat_id=CHAT_ID, text="🔴 LIVE / NEW VIDEO\n" + link)
            print("LIVE SENT")

while True:
    print("Checking YouTube...")
    check_youtube()
    time.sleep(60)