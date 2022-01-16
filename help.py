import discord

def get_help():
    helpEmbed = discord.Embed(title = "Help", description = "Scheduler helps you keep track of your busy life!", colour=discord.Colour.blue())
    helpEmbed \
        .add_field(name = "$list", value = "List all of your current assignments", inline=False) \
        .add_field(name = "$add <name> <mm/dd/yyyy>", value = "Add a new assignment to your list", inline=False) \
        .add_field(name = "$delete <name>", value = "Delete a new assignment from your list", inline=False)
    
    return helpEmbed
    