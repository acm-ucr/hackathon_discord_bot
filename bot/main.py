"""
Discord Bot

Interacts with the Discord API and fetches events from Google Calendar.
"""

import os.path
import os
from dotenv import load_dotenv
import discord
from discord.ext.commands import Bot, has_permissions
from discord import app_commands
from .roles import Roles
from .scheduler import Scheduler
from .mentor import Mentor

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
VERIFICATION_CHANNEL_ID = os.getenv("DISCORD_VERIFICATION_CHANNEL_ID")
MENTOR_CHANNEL_ID = os.getenv("DISCORD_MENTOR_CHANNEL_ID")
ROLE_CHANNEL_ID = os.getenv("DISCORD_ROLE_CHANNEL_ID")

bot: discord.Client = Bot(command_prefix="!", intents=discord.Intents.all())

roles = Roles(bot)
scheduler = Scheduler(bot)
mentor = Mentor(bot)


@bot.tree.command(name="roles")
@has_permissions(administrator=True)
async def send_role_assignment(ctx: discord.Interaction):
    """Send Role Assignments"""
    async with ctx.channel.typing():
        await roles.send_role_assignment(ctx)


@bot.tree.command(name="find_a_mentor")
@has_permissions()
@app_commands.describe(
    location=
    "let me know where is your physical locaiton so a mentor can come find you"
)
@app_commands.describe(tech="let me know what tech stack are you using")
@app_commands.describe(additional="do you have additional notes want to add")
async def on_request_send(ctx: discord.Interaction, location: str, tech: str,
                          additional: str):
    """Mentor request"""
    await mentor.on_request_send(ctx, location, tech, additional)


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    """Add Reaction Based Role"""
    if reaction.message.author == user:
        return
    if str(reaction.message.channel.id) == VERIFICATION_CHANNEL_ID:
        await roles.on_reaction_add(reaction, user)
    elif str(reaction.message.channel.id) == MENTOR_CHANNEL_ID or str(
            reaction.message.channel.id) == ROLE_CHANNEL_ID:
        await mentor.on_reaction_add(reaction, user)


@bot.event
async def on_ready():
    """Run when the bot initially loads"""
    try:
        # sync =  await bot.tree.sync()
        # print(sync)
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
