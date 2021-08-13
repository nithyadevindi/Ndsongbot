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
   "Lexis Song Downloader Bot",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)

@bot.on_message(filters.command("song") & ~filters.edited)
async def song(_, message):
    if len(message.command) < 2:
       return await message.reply("**Usage:**\n - ` /song [query] `")
    query = message.text.split(None, 1)[1]
    shed = await message.reply("Waiting.....")
    ydl_opts = {
       "format": "bestaudio[ext=m4a]",
       "geo-bypass": True,
       "nocheckcertificate": True,
       "outtmpl": "downloads/%(id)s.%(ext)s",
       }
    try:
        search = VideosSearch(query, limit = 1)
        q = search.result()
        title = q[0]["title"]
        print(q)
        print(title)

    except Exception as e:
        await shed.edit(
            "Check Speelings........."
        )
        print(str(e))
        return
    await shed.edit(waiting")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = "@alanonymou"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await shed.edit("wait")
        s = await message.reply_audio(@alanonymou)
        await shed.delete()
    except Exception as e:
        await shed.edit("Error")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.start()
idle()
