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
from timer import Timer
import logging

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class ChatBot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.timer = Timer()
        self.openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.greetings = {
            "user1": "Hello! How can I assist you today dear Meowster? <:catgun:1158210278828281916>",
            "user2": "Hello! How can I assist you today dear Royal Mai's Kitty? <a:whitekit:1158210827690709113>",
            "user3": "Hello! How can I assist you today dear Queen Mommy Meow? <a:whitekit:1158210827690709113>"
        }
        self.default_greeting = "Hello! How can I assist you today dear Meow? <a:yayy:1158210895097380946>"

        logging.basicConfig(level=logging.INFO)

        @self.client.event
        async def on_ready():
            print('Logged on as', self.client.user)

        @self.client.event
        async def on_message(message):
            await self.handle_message(message)

    async def typing_animation(self, thinking_message):
        thinking_image_url = "https://tenor.com/view/cargando-gif-10528529653265737070"
        await thinking_message.edit(content=thinking_image_url)

    async def handle_message(self, message):
        if message.author == self.client.user:
            return

        user_id = message.author.id
        guild_id = message.guild.id
        user_name = str(message.author)
        channel = message.channel

        if message.content.lower().startswith('hello'):
            self.timer.conversations[(user_id, guild_id)] = {'last_interaction': datetime.utcnow()}
            greeting = self.greetings.get(user_name, self.default_greeting)
            await channel.send(greeting)
            logging.info(f"Greeted user {user_name} in channel {channel} of guild {guild_id}.")
            asyncio.create_task(self.timer.end_conversation(user_id, guild_id, channel))
            return

        if (user_id, guild_id) in self.timer.conversations:
            self.timer.conversations[(user_id, guild_id)]['last_interaction'] = datetime.utcnow()
            if message.content.lower() == 'thank you':
                del self.timer.conversations[(user_id, guild_id)]
                await channel.send("You're welcome! Have a great day!")
                logging.info(f"Ended conversation with {user_name} in guild {guild_id}.")
                return

            if message.content.lower().startswith('/countdown'):
                try:
                    seconds = int(message.content.split()[1])
                    asyncio.create_task(self.timer.countdown(channel, seconds))
                except (IndexError, ValueError):
                    await channel.send("Please provide the number of seconds for the countdown, e.g., /countdown 10")
                return

            try:
                self.thinking_done = False
                thinking_message = await channel.send("...")
                asyncio.create_task(self.typing_animation(thinking_message))

                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message.content}]
                )

                self.thinking_done = True
                reply_content = response.choices[0].message.content.strip()
                await thinking_message.edit(content=reply_content)
                logging.info(f"Sent response to user {user_name} in channel {channel} of guild {guild_id}.")
                asyncio.create_task(self.timer.end_conversation(user_id, guild_id, channel))
            except Exception as e:
                await channel.send(f"Error: {e}")
                logging.error(
                    f"Error processing message from user {user_name} in channel {channel} of guild {guild_id}: {e}")

    def run(self):
        self.client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    chat_bot = ChatBot()
    chat_bot.run()
