import os
import yt_dlp
from pyrogram import Client, filters

BOT_TOKEN = ""
API_ID = ""
API_HASH = ""
Bot = Client(
    "instaBot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

INPUT_FILE = "merged_instagram_links.txt"
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    links = [line.strip() for line in file if line.strip()]
    
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),

    'format': 'best[height<=240]/best',

    'noplaylist': True,
    'download_archive': "archive.txt",

    'quiet': True,
    'no_warnings': True,
}

chnl = ""

@Bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply("started")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for index, link in enumerate(links, start=1):
            try:
                info = ydl.extract_info(link, download=True)

                if info is None:
                    print("Download failed or unavailable.")
                    continue
                if 'entries' in info:
                    entries = info['entries']
                else:
                    entries = [info]

                for video in entries:
                    if video is None:
                        continue
                    title = video.get('title', 'Unknown')

                
                await bot.send_video(chat_id=chnl, video=file_dl_path, caption=m.caption)
                os.remove(file_dl_path)
            except Exception as error:
                print(f"Error: {error}")
                continue

Bot.run()
