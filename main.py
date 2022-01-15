import discord
import os
import logging
import os
import sqlite3
from dotenv import load_dotenv, find_dotenv
import help

client = discord.Client()
load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")

def dbConnect ():
    global dbconn, cursor
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shows (
            Title TEXT, Director TEXT, Year INT
        )
    ''')

    connection.commit()
    connection.close()
    


@client.event
async def on_ready():
    print('We have logged in a {0.user}'.format(client))
    return


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return


    # first index is the command, second is the param
    formattedlist = user_message.split(" ") #first index is the command, second is the param
    # help command (please list all commands with brief description)
    if formattedlist[0] == '$help':
        await message.channel.send(embed=help.get_help())
        return

    # global covid stats
    if formattedlist[0] == '$list':
        await message.channel.send('You do not have a list')


def main ():
    try :
        dbConnect()
        client.run(TOKEN)
    except discord.errors.HTTPException:
        print("Token is broken, get a new one")
    except Exception as e:
        print(e)

    
if __name__ == "__main__":
    main()