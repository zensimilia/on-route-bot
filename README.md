# traffic-assistant-bot

Telegram bot will warn you about traffic jams on your route by schedule.

## Installation and run

1. Clone repo.
2. Create python virtual environment and activete it:

    ```console
    python -m venv env
    source ./env/bin/activate
    ```

    > On Windows machines virtual env activates by command `env\Scripts\activate`

3. Install required python modules:

    ```console
    pip install -r requirements.txt
    ```

4. Set required [environment variables](#environment-variables) or fill in _.env_ file.

5. Run bot:

    ```console
    python bot.py
    ```

## Configure

### Environment variables

- **BOT_TOKEN** - (str) Auth token to connect Bot to Telegram services.
- **DB_FILE** - (str) Sqlite database filename with relative path. Default: _store/data.sqlite_.
- **DEBUG** - (bool) Display debugging information in terminal session. Default: _False_.
- **LOG_CONFIG** - (dict) [Configuring](https://docs.python.org/3/library/logging.config.html) the logging module from a dictionary for `dictConfig()` function. Default: see `DEFAULT_CONFIG` in _utils/log.py_.

## Minimal requirements

Any OS with version of **Python** >= 3.8.
Hardware specs: 1 core CPU, 512 Mb of RAM.

- beautifulsoup4
- python-dotenv
- apscheduler
- sqlalchemy
- aiogram
- pydantic
- requests

## Docker

Soon...

## Development and contribution

- **Formatting**: default is `autopep8`, but `black` allowed with _-S_ param (don't format single quotes).

- **Linting**: before commit check your code by `pylint`. Config at _.pylintrc_ file.
