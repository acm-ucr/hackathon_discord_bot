"""Assign roles to a user based on their reaction"""
import os
from dotenv import load_dotenv
import discord

load_dotenv()

ROLES_LIST = {
    "🤖": "Hacker",
}


class Roles:
    """Class to handle all role based management including role assignment for hackers, volunteers, and mentors"""

    def __init__(self, bot):
        self.bot = bot
        self.server: str = os.getenv("DISCORD_SERVER_ID")
        self.channel: str = os.getenv('DISCORD_CHANNEL_ID')

    async def send_role_assignment(self, ctx: discord.Interaction):
        """send the roll assinment message"""
        text: str = "please react to the emoji to get your role\n"
        for emoji, role in ROLES_LIST.items():
            text += f"{role} : {emoji}\n"
        message: discord.Message = await ctx.channel.send(text)
        for emoji in ROLES_LIST:
            await message.add_reaction(emoji)

    async def on_reaction_add(self, reaction: discord.Reaction,
                              user: discord.Member):
        """assign user roles based on their reaction to the role assignment message"""
        channel: discord.TextChannel = await self.bot.fetch_channel(
            self.channel)
        if reaction.message.channel.id == channel.id:
            if reaction.emoji in ROLES_LIST:
                server: discord.Guild = await self.bot.fetch_guild(self.server)
                role: discord.Role = discord.utils.get(
                    server.roles, name=ROLES_LIST[reaction.emoji])
                await user.add_roles(role)
