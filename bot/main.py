"""
Discord Bot

Interacts with the Discord API and fetches events from Google Calendar.
"""

import os.path
import os
import discord
from discord.ext.commands import Bot, has_permissions
from dotenv import load_dotenv
from .roles import Roles
from .scheduler import Scheduler

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot: discord.Client = Bot(command_prefix="!", intents=discord.Intents.all())

roles = Roles(bot)
scheduler = Scheduler(bot)


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
        # await bot.tree.sync()
        print("bot is ready")
        while True:
            await scheduler.send_reminders()
    except RuntimeError as err:
        print(err)


def main():
    """
    main
    """
    bot.run(TOKEN)
