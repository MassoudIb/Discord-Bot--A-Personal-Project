# Author : Massoud Ibrahim
# Date 2024-06-04
# translate .py file has the functions required for combination of commands :
# 1) !join   : will allow the bot to join the Voice Channel.
# 2) !record : will ask the bot to start recording.
# 3) !stop   : will ask the bot to stop recording.
# 4) !leave  : will ask the bot to leave the Voice Channel.

#pip install discord.py discord.py[voice] openai aiohttp
# Also required to install ffmpeg and put it in environment variables C:\bin\ffmpeg.exe

from openai import OpenAI

client = OpenAI()

async def translate(audio_path):
    with open(audio_path, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
    return translation.text

async def transcribe(audio_path):
    with open(audio_path, "rb") as audio_file:
         transcript = client.audio.transcriptions.create(
             model="whisper-1",
             file=audio_file
         )

    return transcript.text