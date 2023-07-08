"""Discord bot to handle hackathon server managment"""
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from .roles import Roles

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot: discord.Client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

roles = Roles(bot)

@bot.tree.command(name="roles")
async def send_role_assignment(ctx: discord.Interaction):
    await roles.send_role_assignment(ctx)

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    await roles.on_reaction_add(reaction, user)

@bot.event
async def on_ready():
    """run once when bot starts"""
    try:
        await bot.tree.sync()
    except RuntimeError as err:
        print(err)


def main():
    "main function"
    bot.run(TOKEN)
