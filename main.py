import discord

client = discord.Client()


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
    client.run("OTMxOTMxNTUyNTcxNjA1MDQy.YeLm5A.uwvgcM9dZOkCPyY4C_vdn2mZHbc")
except discord.errors.HTTPException:
    print("Token is broken, get a new one") 