"""
Discord Bot

Interacts with the Discord API and fetches events from Google Calendar.
"""

from .roles import Roles
from .scheduler import fetch_events
import os.path
import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# from .roles import Roles

# from .scheduler import fetch_events

bot: discord.Client = Bot(command_prefix="!", intents=discord.Intents.all())

roles = Roles(bot)


@bot.tree.command(name="roles")
@has_permissions(administrator=True)
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
    await fetch_events(bot)


async def main():
    """
    main
    """
    await bot.start(TOKEN)


# if __name__ == '__main__': (this causes " coroutine 'main' was never awaited" runtime error)
asyncio.run(main())
