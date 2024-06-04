
 In truth, I was challenged to bring chatGPT into a discord server channel.
 The goal was to allow the server members to be able to have a chat with the bot and have fun.
 The bot will work in multiple servers and it's possible to be used by multiple users at the same time.
 It's still a work in progress and I plan making it better.

---
> [!IMPORTANT]
> **I used this website to update the api:**
> https://github.com/openai/openai-python/discussions/742

---
# To Setup Your Discord Bot
## Step 1: Create your Discord bot

1. To create your Discord Bot, go to https://discord.com/developers/applications
2. Once the bot is created, keep the token given from bot settings.
3. Obtain your API key by visiting https://platform.openai.com/api-keys
4. Create a .env file in the same folder as the .py program
5. Add the following 2 lines in the .env file with the respective tokens.
   > DISCORD_TOKEN= add the discord bot token here.
   > OPENAI_API_KEY= add the openai API key here.
6. Invite your bot to your server via OAuth2 URL Generator

## Step 2: Running the bot on your desktop locally
1. Use the command: `python discord_api.py` to run the bot


## Step 3: Chatting with the bot in discord
1. Use the command: `hello` to start a chat
2. Use the command: `thank you` to end the chat