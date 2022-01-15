import discord
from dotenv import load_dotenv, find_dotenv
import os

client = discord.Client()
load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")


@client.event
async def on_ready():
    print('We have logged in a {0.user}'.format(client))
    return

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")



try :
    client.run(TOKEN)
except discord.errors.HTTPException:
    print("Token is broken, get a new one") 