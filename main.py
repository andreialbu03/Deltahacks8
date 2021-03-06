import asyncio
from email import message
from re import L
import discord
import os
import logging
import os
import sqlite3
from dotenv import load_dotenv, find_dotenv
import help
from datetime import datetime
import sched, time

"""
The reason you are only getting bot, is because you are missing intents. You have to enable intents from the application page for your bot, and also enable intents in your code
"""
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
pfp_path = "pfp.png"
fp = open(pfp_path, 'rb')
pfp = fp.read()

load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")

def dbCreate():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.executescript(''' 
        CREATE TABLE IF NOT EXISTS users ( 
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            PRIMARY KEY (user_id)
        );
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
    ''')

    connection.commit()
    cursor.close()
    connection.close()


@client.event
async def on_ready():
    print('We have logged in a {0.user}'.format(client))
    await client.user.edit(avatar=pfp)
    return


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if len(user_message)==0 or user_message[0] != '$' or message.author == client.user:
        return

    addUser(message)

    # first index is the command, second is the param
    formattedlist = user_message.split(" ") #first index is the command, second is the param
    
    # help command (please list all commands with brief description)
    if formattedlist[0] == '$help':
        await message.channel.send(embed=help.get_help())

    # User's to-do list
    elif formattedlist[0] == '$list':
        #await message.channel.send('You currently do not have a to-do list')
        await displayList(message.author.name, message.author.id)

    # Adding items to the assignment table
    # $add name yyyy-mm-dd
    elif formattedlist[0] == '$add':
        addAssignment(formattedlist[1:], message)
        await message.channel.send(f"You have added {formattedlist[1]} to your list!")
    
    # $delete allows you to delete items from the assignment table
    elif formattedlist[0] == '$delete':
        deleteAssignment(formattedlist[1:], message)
        await message.channel.send(f"You have deleted {formattedlist[1]} from your list!")

    else:
        await message.channel.send('That command does not exist!')


# Checks if user exists in db, else add them to db
def addUser(message):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    if cursor.execute(f"SELECT EXISTS (SELECT 1 FROM users WHERE user_id = {message.author.id})") is False:
        sql_query =  """INSERT INTO users (user_id, name) VALUES (?,?)"""
        cursor.execute(sql_query, (message.author.id, message.author.name))
    
    connection.commit()
    cursor.close()
    connection.close()


@client.event 
async def displayList(name, user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # if cursor.execute(f"SELECT EXISTS (SELECT 1 FROM assignments WHERE user_id = {message.author.id})") is True:
    cursor.execute(f"SELECT * FROM assignments WHERE user_id={user_id}")
    result = cursor.fetchall()
    desc = []
    for row in result:
        print(row)
        desc.append(row[1:3])

    # Sort by lowest highest priority
    desc.sort(key=lambda row: datetime.strptime(row[1], "%m/%d/%Y"))

    embed = discord.Embed(
        title="Assignments",
        colour=discord.Colour.blue()
    )

    embed \
        .set_thumbnail(url="https://store-images.microsoft.com/image/apps.52799.9007199266242703.8cfbff59-6913-4d81-a0ea-d80eca6e999e.32f4abfb-ea86-4bdb-9520-5868179da613?w=498&h=408&q=90&mode=scale&format=jpg&background=%230078D7&padding=0.0.0.0") \
        .set_author(name=f"{name}'s Schedule", icon_url="https://store-images.microsoft.com/image/apps.52799.9007199266242703.8cfbff59-6913-4d81-a0ea-d80eca6e999e.32f4abfb-ea86-4bdb-9520-5868179da613?w=498&h=408&q=90&mode=scale&format=jpg&background=%230078D7&padding=0.0.0.0")
    
    for name, due_date in desc:
        embed.add_field(name=name, value=due_date)

    # else:
    #     await message.channel.send('You have nothing in your list. Please add something!')
    
    connection.commit()
    cursor.close()
    connection.close()

    channel = client.get_channel(932059195925213214)
    await channel.send(embed=embed)

    
# Add an assignment to the db (includes name, due_date)
def addAssignment (query, message):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO assignments (name, due_date, user_id) VALUES (?,?,?)
    ''', (query[0], query[1], message.author.id))

    connection.commit()
    cursor.close()
    connection.close()


# Delete an assignment id
def deleteAssignment (query, message):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM assignments
        WHERE name = ? AND user_id = ?
    ''', (query[0], message.author.id))

    connection.commit()
    cursor.close()
    connection.close()
    

# Notify the user that their homework is going to be due
# https://stackoverflow.com/questions/65808190/get-all-members-discord-py
async def notifier ():
    while True:
        for guild in client.guilds:
            for member in guild.members:
                if any(x is None for x in [member.display_name, member.id]):
                    raise Exception("well crap member.name and member.user_id don't exist what are they")
                elif member.display_name!="Scheduler":
                    channel = client.get_channel(932059195925213214)
                    await channel.send("NOTIFYING CHANNEL")
                    await displayList(member.display_name, member.id)
        
        # adjust timer to go every few other seconds
        await asyncio.sleep(60)


def main ():
    try:
        dbCreate()
        # may cause an error since main is not async
        client.loop.create_task(notifier())
        client.run(TOKEN)
    except discord.errors.HTTPException as e:
        print("Token is broken, get a new one")
        print(e)
    except Exception as e:
        print(e)

    
if __name__ == "__main__":
    main()