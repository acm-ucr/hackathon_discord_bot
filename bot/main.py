import datetime as dt
import os.path
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from pytz import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Function to send a message to a Discord channel
async def send_message_to_discord(message):
    channel = bot.get_channel(1124440964031852717)
    await channel.send(message)

async def fetchEvents():
    print("Fetching events...")
    # Auth stuff
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = dt.datetime.now(timezone('PST8PDT')).isoformat()
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        for event in events:
            print("Print:", event['summary'])
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_start_time = dt.datetime.fromisoformat(start).astimezone(timezone('PST8PDT'))
            current_time = dt.datetime.now(timezone('PST8PDT'))
            time_difference = (event_start_time - current_time).total_seconds()
            print(time_difference)
            await asyncio.sleep(max(time_difference - 600, 0))
            # if time_difference <= 600: 
            print("2 min before event:", time_difference)
            message = f"{event['summary']} is starting in 10 minutes!"
            await send_message_to_discord(message)

            await asyncio.sleep(550)

            # if time_difference <= 0:
            print("Event starting now:", time_difference)
            message = f"{event['summary']} is starting now!"
            await send_message_to_discord(message)

    except HttpError as error:
        print("An error occurred:", error)

@bot.event
async def on_ready():
    print("Bot is Ready and Running!")
    await fetchEvents()

async def main():
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
