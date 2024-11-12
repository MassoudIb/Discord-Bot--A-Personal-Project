# Author : Massoud Ibrahim
# Date 2024-06-04
# I was challenged to bring chat GPT into a discord server channel with cats enthousiasts.
# The goal was to allow the server members to be able to have a chat with the bot and have fun.
# The bot can work in multiple servers and can be used by multiple users at the same time.
# https://github.com/openai/openai-python/discussions/742 I used this website to update the api
# discord_api.py file will handle the commands registration and bot events handling.

import discord
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
from timer import Timer
from weather import get_weather
from calculator import eval_expression
from dalle import generate_image
from translate import translate, transcribe
import logging

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=intents)
timer = Timer()
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

conversation_history = {}
recordings = {}

# That's the way this specific emoji is defined in our discord server
jumping_cat = "<a:yayy:xyz>"
greetings = {
    "user1": f"Hello! How can I assist you today dear Meowster? {jumping_cat}",
    "user2": f"Hello! How can I assist you today dear Royal Mai's Kitty? {jumping_cat}",
    "user3": f"Hello! How can I assist you today dear Queen Mommy Meow? {jumping_cat}"
}
default_greeting = f"Hello! How can I assist you today dear Meow? {jumping_cat}"

logging.basicConfig(level=logging.INFO)

def trim_conversation_history(history, max_length=4096):
    total_length = sum(len(msg['content']) for msg in history)
    while total_length > max_length:
        total_length -= len(history.pop(0)['content'])


@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

@bot.slash_command(name='calc', description="Evaluates a mathematical expression. Usage: /calc <expression>")
async def calc_command(ctx, *, expression: str):
    await ctx.defer()  # will give more time for processing
    result = eval_expression(expression)
    embed = discord.Embed(
        description= f"The result of `{expression}` is {result}",
        color=0x89CFF0
    )
    await ctx.followup.send(embed=embed)

@bot.slash_command(name="countdown", description="Start a countdown timer.")
async def countdown_command(ctx, seconds: int):
    await ctx.defer()
    message = await ctx.followup.send(f"Starting countdown for {seconds} seconds...")
    await timer.countdown(ctx, seconds, message)

@bot.slash_command(name="weather", description="Get the current weather for a specified city.")
async def weather_command(ctx, city: str):
    await ctx.defer()
    result = await get_weather(city)
    if result:
        weather_info, emoji, color = result
        embed = discord.Embed(
            title=f"Weather in {city}",
            description=f"{emoji} "+ "  " + f"{weather_info}",
            color=color
        )

        await ctx.followup.send(embed=embed)
    else:
        await ctx.followup.send(f"Could not retrieve weather information for {city}. Please check the city name and try again.")

@bot.slash_command(name="draw", description="Generate an image using /draw <prompt>.")
async def draw(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        image_url = await generate_image(prompt)
        embed = discord.Embed(title="Generated Image", description=prompt, color=0x00FF00)
        embed.set_image(url=image_url)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

@bot.command(name="join", help="Join a voice channel")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send(f"You are not connected to a voice channel {jumping_cat}")

@bot.command(name="leave", help="Leave a voice channel")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send(f"I am not in a voice channel {jumping_cat}")

@bot.command(name="record", help="Record audio from the voice channel")
async def record(ctx):
    if ctx.voice_client:
        vc = ctx.voice_client
        recordings[ctx.guild.id] = vc
        vc.start_recording(
            MP3Sink(), on_record_complete, ctx
        )

        await ctx.send(f"Recording started! {jumping_cat}")
    else:
        await ctx.send(f"I am not in a voice channel {jumping_cat}")

@bot.command(name="stop", help="Stop recording audio from the voice channel")
async def stop_record(ctx):
    if ctx.guild.id in recordings:
        vc = recordings[ctx.guild.id]
        vc.stop_recording()
        del recordings[ctx.guild.id]
        await ctx.send(f"Recording stopped! {jumping_cat}")
    else:
        await ctx.send("No active recording found!")

async def on_record_complete(sink, ctx):
    filename = list(sink.audio_data.keys())[0]
    audio_path = f"./{filename}.mp3"
    with open(audio_path, "wb") as f:
        f.write(sink.audio_data[filename].file.read())

    await ctx.send(f"Processing audio")
    await ctx.send("<a:work_cat:xyz>")
    translation = await translate(audio_path)
    transcript = await transcribe(audio_path)
    embed = discord.Embed(
        title="Translation Audio to English",
        description=f":loud_sound: : `{transcript}` \n :pencil: : `{translation}`",
        color=0xFFA500
    )
    await ctx.send(embed=embed)
    # Clean up the audio file
    os.remove(audio_path)

async def send_embed_response(channel, content, color):
    embed = discord.Embed(description=content, color=color)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    guild_id = message.guild.id
    user_name = str(message.author.name)
    channel = message.channel
    user_key = (user_id, guild_id)

    if message.content.lower().startswith('hello'):
        timer.conversations[user_key] = {'last_interaction': datetime.utcnow()}
        conversation_history[user_key] = [{'role': 'user', 'content': message.content}]
        await channel.send(greetings.get(user_name, default_greeting))
        logging.info(f"Greeted user {user_name} in channel {channel} of guild {guild_id}.")
        asyncio.create_task(timer.end_conversation(user_id, guild_id, channel))
        return

    if user_key in timer.conversations:
        if user_key in conversation_history:
            conversation_history[user_key].append({'role': 'user', 'content': message.content})
            trim_conversation_history(conversation_history[user_key])
            timer.conversations[user_key]['last_interaction'] = datetime.utcnow()
            if message.content.lower() == 'thank you':
                del timer.conversations[(user_id, guild_id)]
                await channel.send(f"You're welcome! Have a great day! {jumping_cat}")
                logging.info(f"Ended conversation with {user_name} in guild {guild_id}.")
                return

        try:
            thinking_message = await channel.send("...")
            asyncio.create_task(typing_animation(thinking_message))

            response = await openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history[user_key]
            )

            reply_content = response.choices[0].message.content.strip()
            conversation_history[user_key].append({'role': 'assistant', 'content': reply_content})

            logging.info(f"Sent response to user {user_name} in channel {channel} of guild {guild_id}.")
            asyncio.create_task(timer.end_conversation(user_id, guild_id, channel))

            await send_embed_response(channel, reply_content, discord.Color.green())
            await thinking_message.delete()

        except Exception as e:
            await channel.send(f"Error: {e}")
            logging.error(f"Error processing message from user {user_name} in channel {channel} of guild {guild_id}: {e}")

    await bot.process_commands(message)

async def typing_animation(thinking_message):
    thinking_image_url = "https://tenor.com/view/cargando-gif-10528529653265737070"
    await thinking_message.edit(content=thinking_image_url)

