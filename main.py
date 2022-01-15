import discord
import os
import logging
import os
import psycopg2
from configparser import ConfigParser


client = discord.Client()
config = ConfigParser()
config.read('config.cfg')
DISCORD_TOKEN = config["DISCORD"]["TOKEN"]
COCK_TOKEN = config["COCKROACH"]["TOKEN"]


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


def main ():
    try :
        client.run(DISCORD_TOKEN)
    except discord.errors.HTTPException:
        print("Token is broken, get a new one")



    
if __name__ == "__main__":
    main()
