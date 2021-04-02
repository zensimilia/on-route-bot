# traffic-assistant-bot

Telegram bot will warn you about traffic jams on your route by schedule.

## Installation and run

1. Clone repo.
2. Create python virtual environment:

```
$ python -m venv env
```

3. Install packages:

```
$ pip install -r requirements.txt
```

4. Set required environment variables or fill `.env` file.

5. Run bot:

```
$ python bot.py
```

### Environment variables or `.env` file contents

```
BOT_TOKEN={bot token}
DB_FILE=store/{sqlite database filename}
DEBUG={True | False}
```

### Required python packages

-   aiogram
-   python-dotenv
-   requests
-   beautifulsoup4
-   peewee
-   SQLAlchemy
-   APScheduler
-   Pydantic

## Development and contribution

1. **Formatting**: default is `autopep8`, but `black` allowed with `-S` param (don't format quotes).
