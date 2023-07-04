"""Discord bot to handle hackathon server managment"""
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
RoleList = {
    "🤖": "Hacker",
}


@bot.event
async def on_ready():
    """run once when bot starts"""
    try:
        await bot.tree.sync()
    except RuntimeError as err:
        print(err)


@bot.tree.command(name="roles")
async def send_role_assignmnent(ctx: discord.Interaction):
    """send the roll assinment message"""
    text = "please react to the emoji to get your role\n"
    for emoji, role in RoleList.items():
        text += f"{role} : {emoji}\n"
    message = await ctx.channel.send(text)
    for emoji in RoleList:
        await message.add_reaction(emoji)


@bot.event
async def on_reaction_add(reaction, user):
    """assign user roles based on their reaction to the role assignment message"""
    channel = await bot.fetch_channel(os.getenv('CHANNEL_ID'))
    if reaction.message.channel.id != channel.id:
        return
    if reaction.emoji in RoleList:
        server = await bot.fetch_guild(os.getenv("SERVER_ID"))
        role = discord.utils.get(server.roles, name=RoleList[reaction.emoji])
        await user.add_roles(role)


def main():
    "main function"
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
