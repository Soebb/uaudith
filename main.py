import os, time
from pyrogram import Client, filters

BOT_TOKEN = ""
API_ID = ""
API_HASH = ""
chnl = ""

with open("merged_instagram_links.txt", "r", encoding="utf-8") as file:
    links = [line.strip() for line in file if line.strip()]

Bot = Client(
    "instaBot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)



@Bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply("started")
    for index, link in enumerate(links, start=1):
        
        await bot.send_video(chat_id=chnl, video=file_dl_path, caption=m.caption)
        os.remove(file_dl_path)


@Bot.on_message(filters.private & (filters.video | filters.document))
async def thumb_change(bot, m):
    global thumb
    msg = await m.reply("`Downloading..`")
    c_time = time.time()
    file_dl_path = await bot.download_media(message=m, progress=progress_for_pyrogram, progress_args=("Downloading file..", msg, c_time))
    await msg.delete()
    answer = await bot.ask(m.chat.id,'Now send the thumbnail' + ' or /keep to keep the previous thumb' if thumb else '', filters=filters.photo | filters.text)
    if answer.photo:
        try:
            os.remove(thumb)
        except:
            pass
        thumb = await bot.download_media(message=answer.photo)
    msg = await m.reply("`Uploading..`")
    c_time = time.time()
    if m.document:
        await bot.send_document(chat_id=m.chat.id, document=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    elif m.video:
        await bot.send_video(chat_id=m.chat.id, video=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
        
    await msg.delete()
    os.remove(file_dl_path)



Bot.run()
