"""Assign roles to a user based on their reaction"""
import os
from dotenv import load_dotenv
import discord

load_dotenv()

roleList = {
    "🤖": "Hacker",
}


def setup_role_assignment(bot):
    """add commands to the bot"""

    @bot.tree.command(name="roles")
    async def send_role_assignmnent(ctx: discord.Interaction):
        """send the roll assinment message"""
        text = "please react to the emoji to get your role\n"
        for emoji, role in roleList.items():
            text += f"{role} : {emoji}\n"
        message = await ctx.channel.send(text)
        for emoji in roleList:
            await message.add_reaction(emoji)

    @bot.event
    async def on_reaction_add(reaction, user):
        """assign user roles based on their reaction to the role assignment message"""
        channel = await bot.fetch_channel(os.getenv('CHANNEL_ID'))
        if reaction.message.channel.id != channel.id:
            return
        if reaction.emoji in roleList:
            server = await bot.fetch_guild(os.getenv("SERVER_ID"))
            role = discord.utils.get(server.roles,
                                     name=roleList[reaction.emoji])
            await user.add_roles(role)
