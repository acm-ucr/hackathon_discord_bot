"""
Discord Bot

Interacts with the Discord API and fetches events from Google Calendar.
"""

import os.path
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot, has_permissions
from discord import app_commands, Intents, Interaction, Reaction, Member, Client, DMChannel
from .roles import Roles
from .scheduler import Scheduler
from .mentor import Mentor
from .welcome import Welcome

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
VERIFICATION_CHANNEL_ID = os.getenv("DISCORD_VERIFICATION_CHANNEL_ID")
MENTOR_CHANNEL_ID = os.getenv("DISCORD_MENTOR_CHANNEL_ID")
ROLE_CHANNEL_ID = os.getenv("DISCORD_ROLE_CHANNEL_ID")

bot: Client = Bot(command_prefix="!", intents=Intents.all())

roles: Roles = Roles(bot)
scheduler: Scheduler = Scheduler(bot)
mentor: Mentor = Mentor(bot)
welcome: Welcome = Welcome(bot)


@bot.event
async def on_member_join(member):
    """Runs when a new member joins the Discord"""
    await welcome.send_welcome_message(member)


@bot.tree.command(name="roles")
@has_permissions(administrator=True)
async def send_role_assignment(ctx: Interaction):
    """Send Role Assignments"""
    async with ctx.channel.typing():
        await roles.send_role_assignment(ctx)


@bot.tree.command(name="mentor")
@app_commands.describe(location="Where are you located?")
@app_commands.describe(tech="What tech stack are you using?")
@app_commands.describe(additional="Do you have additional notes to add?")
async def on_request_send(ctx: Interaction, location: str, tech: str,
                          additional: str):
    """Mentor request"""
    await mentor.on_request_send(ctx, location, tech, additional)


@bot.event
async def on_reaction_add(reaction: Reaction, user: Member):
    """Add Reaction Based Role"""
    if reaction.message.author == user:
        return
    if str(reaction.message.channel.id) in [
            ROLE_CHANNEL_ID, VERIFICATION_CHANNEL_ID
    ]:
        await roles.on_reaction_add(reaction, user)
    elif str(reaction.message.channel.id) == MENTOR_CHANNEL_ID or isinstance(
            reaction.message.channel, DMChannel):
        await mentor.on_reaction_add(reaction, user)


@bot.event
async def on_ready():
    """Run when the bot initially loads"""
    try:
        print("Bot is Ready!")
        await bot.tree.sync()
        while True:
            await scheduler.send_reminders()
    except RuntimeError as err:
        print(err)


def main():
    """
    main
    """
    bot.run(TOKEN)
