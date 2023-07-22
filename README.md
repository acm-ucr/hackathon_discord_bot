# UCR Hackathon Discord Bot
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Developers
Lead Developer: [Divyank Shah](https://github.com/shahdivyank)<br/>
Developers: [Menthy Wu](https://github.com/menthy-wu), [Sachin Chopra](https://github.com/SafeDuck)

## Python
UCR Hackathon Discord Bot runs on Python Version 3.10 and higher. Please ensure you have Python installed. 

## Poetry 
This project is built using [Poetry](https://python-poetry.org), a Python package and dependency manager. Please ensure you have Poetry installed using the [official installation guide](https://python-poetry.org/docs/#installation). You can also install Poetry via the following command:
```bash
# Linux, MacOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -
```

The following environment variables are required and must be stored in an `.env` file:
```env
DISCORD_BOT_TOKEN=
DISCORD_SERVER_ID=

DISCORD_VERIFICATION_CHANNEL_ID=
DISCORD_EVENTS_CHANNEL_ID=
DISCORD_ROLE_CHANNEL_ID=
DISCORD_MENTOR_CHANNEL_ID=
DISCORD_MENTEE_CHANNEL_ID=
DISCORD_WELCOME_CHANNEL_ID=
DISCORD_INFO_DESK_CHANNEL_ID=
DISCORD_INTRODUCTION_CHANNEL_ID=

GOOGLE_CALENDAR_EMAIL=
GOOGLE_CALENDAR_API_KEY=

HACKATHON_NAME=
```

## Commands

### Dependencies
```bash
# Install dependencies
poetry install

# Add dependency
poetry add <dependency>

# Remove dependency
poetry remove <dependency>
```

### Running the Bot Locally
```bash
poetry run bot
```

### Formatting Code via YAPF
```bash
# Rewrite code recursively with proper formatting
poetry run yapf -ir bot

# Show formatting differences recursively
poetry run yapf -dr bot
```

### Formatting Code via Pylint
```bash
poetry run pylint bot
```

### Build the Bot
```bash
poetry build
```
