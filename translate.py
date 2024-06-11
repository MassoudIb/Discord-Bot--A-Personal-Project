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