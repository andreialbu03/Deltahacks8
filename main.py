from re import L
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


def dbCreate():
    connection = sqlite3.connect("users.db")
    connection2 = sqlite3.connect("assignments.db")
    cursor = connection.cursor()
    cursor2 = connection2.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users ( 
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            PRIMARY KEY (user_id)
        )
    ''')
    cursor2.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    connection.commit()
    connection2.commit()
    cursor.close()
    cursor2.close()
    connection.close()
    connection2.close()


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

    if user_message[0] != '$' or message.author == client.user:
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
        await displayList(message)

    # Adding items to the assignment table
    # $add name yyyy-mm-dd
    elif formattedlist[0] == '$add':
        addAssignment(formattedlist[1:], message)
        await message.channel.send(f"You have added {formattedlist[1]} to your list!")
    
    # $delete allows you to delete items from the assignment table
    elif formattedlist[0] == '$delete':
        deleteAssignment(formattedlist[1:], message)
        await message.channel.send("")

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
async def displayList(message):
    connection = sqlite3.connect("assignments.db")
    cursor = connection.cursor()

    # if cursor.execute(f"SELECT EXISTS (SELECT 1 FROM assignments WHERE user_id = {message.author.id})") is True:
    sql_query =  """SELECT * FROM assignments INNER JOIN users ON assignments.user_id = users.user_id"""
    cursor.execute(sql_query, (message.author.id, message.author.name))
    result = cursor.fetchall()
    for row in result:
        print(row)
    # else:
    #     await message.channel.send('You have nothing in your list. Please add something!')
    
    connection.commit()
    cursor.close()
    connection.close()
    
    
# Add an assignment to the db (includes name, due_date)
def addAssignment (query, message):
    connection = sqlite3.connect("assignments.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO assignments (name, due_date, user_id) VALUES (?,?,?)
    ''', (query[0], query[1]+" 23:59:59", message.author.id))

    connection.commit()
    cursor.close()
    connection.close()


# Delete an assignment id
def deleteAssignment (query, message):
    pass
    

def main ():
    try :
        dbCreate()
        client.run(TOKEN)
    except discord.errors.HTTPException:
        print("Token is broken, get a new one")
    except Exception as e:
        print(e)

    
if __name__ == "__main__":
    main()