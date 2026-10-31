import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

BOT_TOKEN = ""
API_ID = 12345
API_HASH = ""

Bot = Client(
    "instaBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

chnl = ""

DOWNLOAD_DIR = "downloads"
INPUT_FILE = "merged_instagram_links.txt"
ARCHIVE_FILE = "archive.txt"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    links = [line.strip() for line in file if line.strip()]


ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),

    'format': 'best[height<=240]/best[height<=360]',

    'ignoreerrors': True,
    'noplaylist': True,

    'download_archive': ARCHIVE_FILE,

    'quiet': True,
    'no_warnings': True,

    'sleep_interval_requests': 2,
    'sleep_interval': 4,
    'max_sleep_interval': 10,

    'retries': 10,
    'fragment_retries': 10,
}


# دانلود هر لینک
def download_link(link):

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(link, download=True)

        if not info:
            return []

        entries = info.get('entries') or [info]

        results = []

        for video in entries:

            if video is None:
                continue

            description = video.get(
                'description',
                'No description available'
            )

            filepath = (
                video.get('filepath')
                or ydl.prepare_filename(video)
            )

            results.append({
                'description': description,
                'filepath': filepath
            })

        return results


# جلوگیری از اجرای هم‌زمان چند عملیات دانلود
download_lock = asyncio.Lock()


@Bot.on_message(filters.command(["start"]))
async def start(bot, m):

    if download_lock.locked():
        await m.reply("Download process is already running.")
        return

    async with download_lock:

        await m.reply("Started!")

        total = len(links)

        for index, link in enumerate(links, start=1):

            print(f"\n[{index}/{total}] Processing: {link}")

            try:

                results = await asyncio.to_thread(
                    download_link,
                    link
                )

                if not results:
                    print("Download failed or unavailable.")
                    continue

                for video in results:

                    file_dl_path = video['filepath']
                    description = video['description']

                    if not os.path.isfile(file_dl_path):
                        print(f"File not found: {file_dl_path}")
                        continue

                    caption = (
                        f"{index}\n"
                        f"{link}\n"
                        f"{description}"
                    )[:1024]

                    try:

                        await bot.send_video(
                            chat_id=chnl,
                            video=file_dl_path,
                            caption=caption
                        )

                        print("\nUpload successful!")
                        print(f"Description: {description}")
                        print(f"URL: {link}")
                        print(f"File Path: {file_dl_path}")

                        os.remove(file_dl_path)

                    except Exception as error:
                        print(f"Telegram upload error: {error}")

            except Exception as error:
                print(f"Download error: {error}")
                continue

        await m.reply("All links processed!")


Bot.run()
