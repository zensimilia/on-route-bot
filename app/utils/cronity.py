_DAYS = {
    '0':    'Воскресенье',
    '1':    'Понедельник',
    '2':    'Вторник',
    '3':    'Среда',
    '4':    'Четверг',
    '5':    'Пятница',
    '6':    'Суббота',
    '1-5':  'Рабочие дни',
    '6-0':  'Выходные дни',
    '*':    'Ежедневно'
}


def humanize(data: dict) -> str:
    """
    Convert dict with cron args to readable string.

    :param dict data: Contains 'minute', 'hour', and 'day_of_week'.
    """
    day_of_week = _DAYS.get(data['day_of_week'])
    if not day_of_week:
        days = data['day_of_week'].split('-')
        day_of_week = f"{_DAYS.get(days[0])} — {_DAYS.get(days[1])}".capitalize(
        )
    return f"{day_of_week}, в {data['hour']}:{data['minute']}"
