"""Discord bot to handle hackathon server managment"""
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from .roles import Roles

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot: discord.Client = commands.Bot(command_prefix="!",
                                   intents=discord.Intents.all())

roles = Roles(bot)


@bot.tree.command(name="roles")
async def send_role_assignment(ctx: discord.Interaction):
    """Send Role Assignments"""
    async with ctx.channel.typing():
        await roles.send_role_assignment(ctx)


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    """Add Reaction Based Role"""
    await roles.on_reaction_add(reaction, user)


@bot.event
async def on_ready():
    """Run when the bot initially loads"""
    try:
        await bot.tree.sync()
    except RuntimeError as err:
        print(err)


def main():
    "Entry point for bot"
    bot.run(TOKEN)
