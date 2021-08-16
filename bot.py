import os
import logging
import requests
import aiohttp
import json
import youtube_dl
from pyrogram import filters, Client, idle
from youtubesearchpython import VideosSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

# logging
bot = Client(
   "Song Downloader",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)


@bot.on_message(filters.command("start") & ~filters.edited)
async def start(_, message):
   if message.chat.type == 'private':
       await message.reply("**Hey There, I'm a song downloader bot. A bot by @Lexiebotupdate.\nUsage:** `/song [query]`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Dev", url="https://t.me/Lexiebotupdate"),
                                        InlineKeyboardButton(
                                            "Source", url="https://github.com/nithyadevindi")
                                    ]]
                            ))
   else:
      await message.reply("**Song downloader bot is online ✨**")


@bot.on_message(filters.command("song") & ~filters.edited)
async def song(_, message):
    if len(message.command) < 2:
       return await message.reply("**Usage:**\n - `/song [query]`")
    query = message.text.split(None, 1)[1]
    shed = await message.reply("🔎 Finding the song...")
    ydl_opts = {
       "format": "bestaudio[ext=m4a]",
       "geo-bypass": True,
       "nocheckcertificate": True,
       "outtmpl": "downloads/%(id)s.%(ext)s",
       }
    try:
        search = VideosSearch(query, limit = 1)
        q = search.result()
        # link = q[0]["link"]
        title = q[0]["title"]
        print(q)
        print(title)
        # thumbnail = q[0]["thumbnails"][0]["url"]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = q[0]["duration"]
        channel = q[0]["channel"]

    except Exception as e:
        await shed.edit(
            "❌ Found Nothing.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    await shed.edit("📥 Downloading...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = "@Lexiebotupdate"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await shed.edit("📤 Uploading...")
        s = await message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur, performer=channel)
        await shed.delete()
    except Exception as e:
        await shed.edit("❌ Error")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.start()
idle()
