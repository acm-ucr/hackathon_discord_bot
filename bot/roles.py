"""Assign roles to a user based on their reaction"""
import os
from dotenv import load_dotenv
import discord

load_dotenv()

ROLES_LIST = {"💻": "Hacker", "📞": "Volunteer", "🧠": "Mentor"}


class Roles:
    """
    Class to handle all role based management 
    including role assignment for hackers, volunteers, 
    and mentors
    """

    def __init__(self, bot):
        self.bot = bot
        self.server: str = os.getenv("DISCORD_SERVER_ID")
        self.role_channel: str = os.getenv('DISCORD_ROLE_CHANNEL_ID')
        self.verification_channel: str = os.getenv(
            'DISCORD_VERIFICATION_CHANNEL_ID')

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
        if reaction.message.author == user:
            return
        role_channel: discord.TextChannel = await self.bot.fetch_channel(
            self.role_channel)
        verification_channel: discord.TextChannel = await self.bot.fetch_channel(
            self.verification_channel)
        if reaction.message.channel.id == role_channel.id:
            if ROLES_LIST[reaction.emoji] == "Hacker":
                server: discord.Guild = await self.bot.fetch_guild(self.server)
                role: discord.Role = discord.utils.get(
                    server.roles, name=ROLES_LIST[reaction.emoji])
                await user.add_roles(role)
            if ROLES_LIST[reaction.emoji] in ["Volunteer", "Mentor"]:
                server: discord.Guild = await self.bot.fetch_guild(self.server)
                role: discord.Role = discord.utils.get(
                    server.roles, name=ROLES_LIST[reaction.emoji])
                message: discord.Message = await verification_channel.send(
                    f"""{user.mention} is requesting access 
                    to the following role: {reaction.emoji} {role.mention}""")
                await message.add_reaction("✅")
                await message.add_reaction("❌")
        if reaction.message.channel.id == verification_channel.id:
            member: discord.Member = reaction.message.mentions[0]
            role: discord.Role = reaction.message.role_mentions[0]
            if reaction.emoji == "✅":
                await member.add_roles(role)
            elif reaction.emoji == "❌":
                await member.remove_roles(role)
