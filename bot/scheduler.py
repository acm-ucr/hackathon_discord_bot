import datetime as dt
import discord
from dotenv import load_dotenv
from pytz import timezone
import requests
import os.path
import os
import aiohttp
import json
import dateutil.parser
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_KEY=os.getenv('GOOGLE_CALENDAR_API_KEY')
EMAIL=os.getenv('GOOGLE_CALENDAR_EMAIL')
CHANNEL_ID=os.getenv('DISCORD_ROLE_CHANNEL_ID')

async def fetch_events(bot):
    """gets events from google calender and echo to discord"""

    print("Fetching events...")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{EMAIL}/events?key={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print("Error occurred while fetching events:", response.status)
                return

            data = await response.json()

            events = data.get('items', [])
            if not events:
                print('No events found in calendar.')
                return

            current_time = dt.datetime.now()
            future_events = []
            print("Number of events:", len(events))
            for event in events:
                start_time = dt.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
                current_time = current_time.astimezone(start_time.tzinfo)
                if start_time > current_time:
                    future_events.append(event)

            if not future_events:
                print('No upcoming future events found.')
                return

            for event in future_events:
                event_name = event['summary']
                event_start_time = event['start']['dateTime']
                event_start_time_str = event['start']['dateTime']
                event_location = event.get('location', 'No location')
                event_description = event.get('description', 'No description')
        
                # Convert the start time to the desired timezone
                pst_timezone = timezone('PST8PDT')
                event_start_time_pst = dt.datetime.fromisoformat(event_start_time).astimezone(pst_timezone)
                
                # Format the time in PST without the date
                event_start_time_formatted = event_start_time_pst.strftime('%I:%M %p')
                message = f"**{event_name}** ({event_start_time_formatted}) in **10 minutes** at **{event_location}**!\n\n{event_description}"
                print(message)
                print()
                
                # Convert the event_start_time_str to a datetime object
                event_start_time = dateutil.parser.isoparse(event_start_time_str)
                current_time = dt.datetime.now(timezone('PST8PDT'))
                print(event_start_time)
                print(current_time)
                time_difference = (event_start_time - current_time).total_seconds()
                print(time_difference)
                channel = bot.get_channel(1124440964031852717)
                await asyncio.sleep(max(time_difference - 600, 0))
                print(message)
                if time_difference <= 600:
                    print("10 min before event:", time_difference)
                await channel.send(message)
                
                message = f"**{event_name}** ({event_start_time_formatted}) is **starting now** at **{event_location}**!\n\n{event_description}"
                current_time = dt.datetime.now(timezone('PST8PDT'))
                time_difference = (event_start_time - current_time).total_seconds()
                await asyncio.sleep(time_difference)
                await channel.send(message)