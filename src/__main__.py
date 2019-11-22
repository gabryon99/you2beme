from __future__ import unicode_literals
from aiogram import Bot, Dispatcher, executor, types

import asyncio
import youtube_dl
import logging
import os

import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

# get the telegram bot token
token = os.getnv(telegram_token)
# create socket and dispacther
bot = Bot(token=token)
dispatcher = Dispatcher(bot)
# create a temp variable to hold index of audios
index_audio = 0

@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm You2beme!\nSend me a youtube link and I will convert it for you!")

@dispatcher.message_handler(regexp="^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*")
async def run_youtubedl(message: types.Message):

    global index_audio

    filename = f'audio{index_audio}'

    # set options for audio
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192'
        }],
        'logger': MyLogger(),
        'verbose': True,
        'restrictfilenames': True,
        'cachedir': u'temp/',
        'outtmpl': f'temp/{filename}.%(ext)s'
    }

    link = message['text']
    index_audio += 1

    await message.reply("🔃 Loading: converting video to m4a...")

    # Download video from youtube
    with youtube_dl.YoutubeDL(options) as ydl:
        try:
            ydl.download([link])
        except youtube_dl.utils.DownloadError as e:
            await message.reply("❌ Error: something went wrong! Try later...")
            return

    await message.reply("🔃 Loading: sending audio...")

    # Send audio to telegram
    try:
        with open(f'temp/{filename}.m4a', 'rb') as audio:
            await message.reply_audio(audio=audio, caption=f'🔉 Finish: Here your video converted to m4a!')
    except FileNotFoundError as e:
            await message.edit_reply_markup("❌ Error: something went wrong! Try later...")

    try:
        os.remove(f'temp/{filename}.m4a')
    except FileNotFoundError as e:
        return

executor.start_polling(dispatcher, skip_updates=True) 
