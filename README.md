
 I was challenged to bring chatGPT into a discord server channel.
 The goal was to allow the server members to be able to have a chat with the bot and have fun.
 The bot can work in multiple servers and can be used by multiple users simultaneously.
 It's still a work in progress.

### Chatting with the bot
![image](https://github.com/MassoudIb/Discord-Bot--A-Personal-Project/blob/7c3b6c1fb2c933a92df331df10f5d45f1cbce31f/GIFS/hello_Conversation.gif)

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
1. Use the command: `python main.py` to run the bot


## Step 3: Chatting with the bot in Discord
1. Use the command: `hello` to start a chat
2. Use the command: `thank you` to end the chat

## Step 4: Using the Slash Commands
1. Use the command: `/Weather <city> ` to get the weather info of any city worldwide
2. Use the command: `/calc <expression>` to evaluate a mathematical expression
3. Use the command: `/countdown <number in seconds>` to start a timer
4. Use the command: `/draw <prompt>` to get an 1024x1024 image corresponding to your prompt

### Example Using Draw Command
![image](https://github.com/MassoudIb/Discord-Bot--A-Personal-Project/blob/7c3b6c1fb2c933a92df331df10f5d45f1cbce31f/GIFS/cat_drawing.gif)

## Step 5: Record Conversations and Translate from Any Language to English
1. Use the command: `!join` for the bot to join the Voice Channel you are connected to.
2. Use the command: `!record` for the bot to start recording you.
3. Use the command: `!stop` for the bot to stop recording and process the audio.
4. Use the command: `!leave` for the bot to leave the Voice Chat.