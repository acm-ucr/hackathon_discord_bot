"""Send out announcements 10 mins before and right before event starts on google calender"""

import os
import os.path
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import requests
import pytz
from dateutil import parser
from discord import TextChannel, Client


class Scheduler:
    """
    Scheduler class which handles event reminders 
    approximately 10 minutes before the event
    and right as the event starts. Handles multiple parallel events. 
    """

    def __init__(self, bot: Client):
        self.bot: Client = bot
        load_dotenv()
        self.google_calendar_api_key = os.getenv('GOOGLE_CALENDAR_API_KEY')
        self.google_calendar_id = os.getenv('GOOGLE_CALENDAR_EMAIL')
        self.event_channel = os.getenv('DISCORD_EVENTS_CHANNEL_ID')

    def _get_current_time(self, iso: bool = False):
        if iso is True:
            return datetime.now(pytz.timezone('US/Pacific')).isoformat()
        return datetime.now(pytz.timezone('US/Pacific'))

    def _get_next_event(self) -> list:
        current_time_str: str = self._get_current_time(iso=True)
        query_params: str = f"singleEvents=true&orderBy=startTime&timeMin={current_time_str}&maxResults=10"
        url: str = f"https://www.googleapis.com/calendar/v3/calendars/{self.google_calendar_id}/events?key={self.google_calendar_api_key}&{query_params}"
        response: list = requests.get(url, timeout=5).json()["items"]

        # Filter events that are currently happening
        response: list = [
            event for event in response
            if (parser.parse(event["start"]["dateTime"]) -
                self._get_current_time()).total_seconds() > 0
        ]
        return response

    def _compute_delta(self, events) -> int:
        for event in events:
            event_date: datetime = parser.parse(event["start"]["dateTime"])
            current_time: datetime = self._get_current_time()
            delta: int = int((event_date - current_time).total_seconds())
            event["delta"]: int = delta
        return events

    async def send_reminders(self) -> None:
        """Main driver to send reminders on Discord Channels"""
        events: list = self._get_next_event()
        events: list = self._compute_delta(events)

        sleep_time: int = 3600

        for event in events:
            channel: TextChannel = await self.bot.fetch_channel(
                self.event_channel)
            if event["delta"] < 60:
                description = event['description'].split("\n")[1]
                await channel.send(
                    f"@everyone {event['summary']} happening RIGHT NOW in {event['location']}! {description}"
                )
            elif event["delta"] < 660:
                minutes: int = round(event["delta"] / 60)
                description = event['description'].split("\n")[1]
                await channel.send(
                    f"@everyone {event['summary']} happening in {minutes} MINUTES in {event['location']}! {description}"
                )
                sleep_time: int = event["delta"] - 60 
            else:
                sleep_time: int = event["delta"] - 600
                break
        await asyncio.sleep(sleep_time)
