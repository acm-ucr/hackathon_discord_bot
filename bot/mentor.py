"""allow hacker to request for mentor and mentors to accept request"""
import os
from dotenv import load_dotenv
from discord import TextChannel, Interaction, Reaction, Member, Message, Client


class Mentor:
    """Handle mentor requests and assignments"""

    def __init__(self, bot: Client):
        load_dotenv()
        self.bot: Client = bot
        self.mentor_channel: str = os.getenv("DISCORD_MENTOR_CHANNEL_ID")
        self.mentee_channel: str = os.getenv("DISCORD_MENTEE_CHANNEL_ID")

    async def on_request_send(self, ctx: Interaction, location: str, tech: str,
                              other: str):
        """command when hacker request for a mentor"""
        mentee_channel: TextChannel = await self.bot.fetch_channel(
            self.mentee_channel)
        if str(ctx.channel.id) != self.mentee_channel:
            await ctx.response.send_message(
                f"Please send your request in {mentee_channel.mention} channel",
                ephemeral=True)
            return
        mentor_text: str = f"""{ctx.user.mention} needs assistance! Please react with a 🤚 if you are available!\n
            They are located by: {location}\n
            They are using following tech stack: {tech}\n
            Additional Notes: {"N/A" if other == "" else other}
            """
        mentee_text: str = f"""{ctx.user.mention}, you requested assistance!\n
            You are located by: {location}\n
            You are using the following tech stack: {tech}\n
            Additional Notes: {"N/A" if other == "" else other}
            """
        mentor_channel: TextChannel = await self.bot.fetch_channel(
            self.mentor_channel)
        message: Message = await mentor_channel.send(mentor_text)
        await message.add_reaction("🤚")
        await ctx.response.send_message(mentee_text, ephemeral=True)
        return

    async def on_reaction_add(self, reaction: Reaction, user: Member):
        """Send a message to the mentee when a mentor reacts on their request"""
        if reaction.emoji == "🤚":
            mentee_text: str = f"""{user.mention} has accepted your request! They are on their way to help you!\n
            If they do not come within 10 minutes you can try to contact them on Discord or send another request!"""
            mentor_text: str = f"""{user.mention}, you have accepted {reaction.message.mentions[0].mention}'s request!\n
            Please react with a ✅ when you resolve the issue"""
            await reaction.message.mentions[0].send(mentee_text)
            mentor_message: Message = await user.send(mentor_text)
            await mentor_message.add_reaction("✅")
        elif reaction.emoji == "✅":
            mentee_text: str = f"{user.mention} has resolved your issue! If your issue is not solved, please send another request!"
            await reaction.message.mentions[0].send(mentee_text)
