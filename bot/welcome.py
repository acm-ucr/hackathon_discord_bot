import os
from dotenv import load_dotenv
from discord import Client, TextChannel, Member


class Welcome:

    def __init__(self, bot: Client):
        load_dotenv()
        self.bot: Client = bot
        self.welcome_channel: str = os.getenv("DISCORD_WELCOME_CHANNEL_ID")
        self.info_desk_channel: str = os.getenv("DISCORD_INFO_DESK_CHANNEL_ID")
        self.introduction_channel: str = os.getenv(
            "DISCORD_INTRODUCTION_CHANNEL_ID")
        self.hackathon: str = os.getenv("HACKATHON_NAME")
        pass

    async def send_welcome_message(self, member: Member):
        welcome_channel: TextChannel = await self.bot.fetch_channel(
            self.welcome_channel)
        await welcome_channel.send(
            f"Hello {member.mention}! Welcome to {self.hackathon}!\nCheck out the <#{self.info_desk_channel}> to get started and introduce yourself in <#{self.introduction_channel}>!"
        )
