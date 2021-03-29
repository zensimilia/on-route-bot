from app.types import DayOfWeek


def humanize(data: dict) -> str:
    """ Convert dict with cron args to readable string.

    :param data: Contains 'minute', 'hour', and 'day_of_week'.
    """
    day = DayOfWeek.by_cron(data['day_of_week'])

    return f"{day.title}, в {data['hour']}:{data['minute']}"
