"""Discord bot to handle hackathon server managment"""
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from .roles import setup_role_assignment

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


setup_role_assignment(bot)

@bot.event
async def on_ready():
    """run once when bot starts"""
    try:
        await bot.tree.sync()
    except RuntimeError as err:
        print(err)

def main():
    "main function"
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
