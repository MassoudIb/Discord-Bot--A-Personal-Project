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
from datetime import datetime, timedelta
import logging

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

conversations = {}

# If you have specific users that you want to greet with a unique way
greetings = {
    "user1": "Hello! How can I assist you today dear Meowster? <:catgun:1158210278828281916>",
    "user2": "Hello! How can I assist you today dear Royal Mai's Kitty? <a:whitekit:1158210827690709113>",
    "user3": "Hello! How can I assist you today dear Queen Mommy Meow? <a:whitekit:1158210827690709113>"
}

default_greeting = "Hello! How can I assist you today dear Meow? <a:yayy:1158210895097380946>"

logging.basicConfig(level=logging.INFO)

async def end_conversation(user_id, guild_id, channel):
    await asyncio.sleep(120)
    if (user_id, guild_id) in conversations:
        last_interaction_time = conversations[(user_id, guild_id)]['last_interaction']
        if datetime.utcnow() - last_interaction_time >= timedelta(minutes=2):
            del conversations[(user_id, guild_id)]
            await channel.send("Ending conversation due to inactivity <:cat_evil:1158210003501596713>")
            logging.info(f"Ended conversation with {user_id} in guild {guild_id} due to inactivity.")

async def typing_animation(thinking_message):
    thinking_image_url = "https://tenor.com/view/cargando-gif-10528529653265737070"
    await thinking_message.edit(content=thinking_image_url)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    guild_id = message.guild.id
    user_name = str(message.author)
    channel = message.channel

    if message.content.lower().startswith('hello'):
        conversations[(user_id, guild_id)] = {'last_interaction': datetime.utcnow()}

        if user_name in greetings:
            greeting = greetings[user_name]
        else:
            greeting = default_greeting

        await channel.send(greeting)
        logging.info(f"Greeted user {user_name} in channel {channel} of guild {guild_id}.")
        asyncio.create_task(end_conversation(user_id, guild_id, channel))
        return

    if (user_id, guild_id) in conversations:
        conversations[(user_id, guild_id)]['last_interaction'] = datetime.utcnow()
        if message.content.lower() == 'thank you':
            del conversations[(user_id, guild_id)]
            await channel.send("You're welcome! Have a great day!")
            logging.info(f"Ended conversation with {user_name} in guild {guild_id}.")
            return

        try:
            thinking_message = await channel.send("...")
            await typing_animation(thinking_message)

            response = await openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}]
            )

            reply_content = response.choices[0].message.content.strip()
            await thinking_message.edit(content=reply_content)
            logging.info(f"Sent response to user {user_name} in channel {channel} of guild {guild_id}.")
            asyncio.create_task(end_conversation(user_id, guild_id, channel))
        except Exception as e:
            await channel.send(f"Error: {e}")
            logging.error(f"Error processing message from user {user_name} in channel {channel} of guild {guild_id}: {e}")


client.run(DISCORD_TOKEN)