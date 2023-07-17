"""allow hacker to request for mentor and mentors to accept request"""
import os
from dotenv import load_dotenv
from discord import TextChannel, Interaction, Reaction, Member, Message, Client

load_dotenv()


class Mentor:
    """handle mentor request and assinemnt"""

    def __init__(self, bot):
        self.bot: Client = bot
        self.mentor_channel: str = os.getenv("DISCORD_MENTOR_CHANNEL_ID")
        self.mentee_channel: str = os.getenv("DISCORD_MENTEE_CHANNEL_ID")

    async def on_request_send(self, ctx: Interaction, location: str, tech: str,
                              other: str):
        """command when hacker request for a mentor"""
        if str(ctx.channel.id) != self.mentee_channel:
            await ctx.response.send_message(
                "please send your request in mentee channel", ephemeral=True)
            return
        mentor_text: str = f"{ctx.user.mention} needs help with {tech} please react 🤚 if you can \nlocation: {location}\n{ ''if other=='' else f'additional notes:{other}'}"
        mentee_text: str = f"{ctx.user.mention}, you requested help with {tech} \nlocation: {location}\n{ ''if other=='' else f'additional notes:{other}'}"
        mentor_channel: TextChannel = await self.bot.fetch_channel(
            self.mentor_channel)
        message: Message = await mentor_channel.send(mentor_text)
        await message.add_reaction("🤚")
        await ctx.response.send_message(mentee_text)
        return

    async def on_reaction_add(self, reaction: Reaction, user: Member):
        """send a message to mentee when a mentor react on their request"""
        mentee_channel: TextChannel = await self.bot.fetch_channel(
            self.mentee_channel)
        mentor_channel: TextChannel = await self.bot.fetch_channel(
            self.mentor_channel)
        if reaction.emoji == "🤚":
            mentee_text: str = f"{user.mention} has accepted your request, they are on their way to help you! If they do not come in 10 mins you can try contact the on discord or send another request"
            mentor_text: str = f"{user.mention}, you have accepted {reaction.message.mentions[0].mention} 's request, react ✅ when you resolve the issues"
            await mentee_channel.send(mentee_text)
            mentor_message: Message = await mentor_channel.send(mentor_text)
            await mentor_message.add_reaction("✅")
        elif reaction.emoji == "✅":
            mentee_text: str = f"{user.mention} has reslved your issue"
            await mentee_channel.send(mentee_text)
