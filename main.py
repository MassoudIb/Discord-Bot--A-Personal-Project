# Author : Massoud Ibrahim
# Date 2024-09-20
# The main.py will initialize and run the bot.

import os
from discord_api import bot
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)