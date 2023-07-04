import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
RoleList = {
            "🤖":"Hacker",
}

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.tree.command(name="sendRoleAssignmnent")
async def sendRoleAssignmnent ( ctx: discord.Interaction) :
    channel = await bot.fetch_channel(os.getenv('CHANNEL_ID'))
    text= "please react to the emoji to get your role\n"
    for i in RoleList:
        text+=f"{RoleList[i]} : {i}\n"
    Moji = await channel.send(text)
    for i in RoleList:
        await Moji.add_reaction(i)
        
@bot.event
async def on_reaction_add(reaction, user):
    channel = await bot.fetch_channel(os.getenv('CHANNEL_ID'))
    if reaction.message.channel.id != channel.id:
        return
    if reaction.emoji in RoleList:
        server = await bot.fetch_guild(os.getenv("SERVER_ID"))
        role = discord.utils.get(server.roles, name=RoleList[reaction.emoji])
        await user.add_roles(role)
    

def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
