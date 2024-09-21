# Author : Massoud Ibrahim
# Date 2024-06-04
# timer.py file has the functions required for /countdown command.

import asyncio
from datetime import datetime, timedelta
import logging

class Timer:
    def __init__(self):
        self.conversations = {}

    async def end_conversation(self, user_id, guild_id, channel):
        await asyncio.sleep(180)
        if (user_id, guild_id) in self.conversations:
            last_interaction_time = self.conversations[(user_id, guild_id)]['last_interaction']
            if datetime.utcnow() - last_interaction_time >= timedelta(minutes=3):
                del self.conversations[(user_id, guild_id)]
                await channel.send("Ending conversation due to inactivity <:cat_evil:1158210003501596713>")
                logging.info(f"Ended conversation with {user_id} in guild {guild_id} due to inactivity.")

    async def countdown(self, channel, seconds, message):
        hourglass_emoji = ':hourglass_flowing_sand:'
        numbers_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':zero:']

        for i in range(seconds, 0, -1):
            remaining_time = f"{hourglass_emoji} "
            for digit in str(i):
                if digit.isdigit():
                    emoji_index = int(digit) - 1
                    remaining_time += numbers_emojis[emoji_index]
            await asyncio.sleep(1)
            await message.edit(content=remaining_time)
        await message.edit(content=f":hourglass: Countdown finished!")
