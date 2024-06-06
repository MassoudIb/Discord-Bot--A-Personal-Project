# Author : Massoud Ibrahim
# Date 2024-06-04
# In truth, I was challenged to bring chat GPT into a discord server channel with cats enthousiasts.
# The goal was to allow the server members to be able to have a chat with the bot and have fun.
# The bot can work in multiple servers and can be used by multiple users at the same time.
# https://github.com/openai/openai-python/discussions/742 used this website to update the api

import discord
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
from timer import Timer
import logging

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GUILD_ID = int(os.getenv('GUILD_ID'))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=intents)
timer = Timer()
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

jumping_cat = "<a:yayy:1158210895097380946>"
greetings = {
    "user1": f"Hello! How can I assist you today dear Meowster? {jumping_cat}",
    "user2": f"Hello! How can I assist you today dear Royal Mai's Kitty? {jumping_cat}",
    "user3": f"Hello! How can I assist you today dear Queen Mommy Meow? {jumping_cat}"
}
default_greeting = f"Hello! How can I assist you today dear Meow? {jumping_cat}"

logging.basicConfig(level=logging.INFO)

# Event that runs when the bot is ready and connected to Discord.
@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

# Just an example of how a slash command works in discord
@bot.slash_command(name="ping", description="Ping command")
async def _ping(ctx):
    await ctx.send("pong")  # Responds with "pong" when the /ping command is used.

@bot.slash_command(name="countdown", description="Start a countdown timer.")
async def countdown_command(ctx, seconds: int):
    await ctx.defer() # will give more time for processing
    message = await ctx.followup.send(f"Starting countdown for {seconds} seconds...")
    await timer.countdown(ctx.channel, seconds, message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    guild_id = message.guild.id
    user_name = str(message.author.name)
    channel = message.channel

    if message.content.lower().startswith('hello'):
        timer.conversations[(user_id, guild_id)] = {'last_interaction': datetime.utcnow()}
        await channel.send(greetings.get(user_name, default_greeting))
        logging.info(f"Greeted user {user_name} in channel {channel} of guild {guild_id}.")
        asyncio.create_task(timer.end_conversation(user_id, guild_id, channel))
        return

    if (user_id, guild_id) in timer.conversations:
        timer.conversations[(user_id, guild_id)]['last_interaction'] = datetime.utcnow()
        if message.content.lower() == 'thank you':
            del timer.conversations[(user_id, guild_id)]
            await channel.send("You're welcome! Have a great day!")
            logging.info(f"Ended conversation with {user_name} in guild {guild_id}.")
            return

        try:
            thinking_message = await channel.send("...")
            asyncio.create_task(typing_animation(thinking_message))

            response = await openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}]
            )

            reply_content = response.choices[0].message.content.strip()
            await thinking_message.edit(content=reply_content)
            logging.info(f"Sent response to user {user_name} in channel {channel} of guild {guild_id}.")
            asyncio.create_task(timer.end_conversation(user_id, guild_id, channel))
        except Exception as e:
            await channel.send(f"Error: {e}")
            logging.error(f"Error processing message from user {user_name} in channel {channel} of guild {guild_id}: {e}")

    await bot.process_commands(message)

async def typing_animation(thinking_message):
    thinking_image_url = "https://tenor.com/view/cargando-gif-10528529653265737070"
    await thinking_message.edit(content=thinking_image_url)

bot.run(DISCORD_TOKEN)