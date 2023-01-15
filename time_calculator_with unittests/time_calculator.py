def add_time(start: str, duration: str, *args) -> str:
    """
        The function add the duration time to the start time and return the result.
        If the result will be the next day, it show (next day) after the time.
        If the result will be more than one day later, it  show (n days later) after the time,
        where "n" is the number of days later.
        If the function is given the optional starting day of the week parameter,
        then the output display the day of the week of the result.
        The day of the week in the output appear after the time and before the number of days later.
        Below are some examples of different cases the function should handle.
    :param start: a start time in the 12-hour clock format
    :param duration: a duration time that indicates the number of hours and minutes
    :param args: (optional) a starting day of the week, case insensitive
    :return: result time in the 12-hour clock format
    """
    new_day = day = None
    days_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}

    from datetime import datetime, timedelta

    if args:
        day = args[0].capitalize()
    delta = timedelta(hours=int(duration.split(':')[0]), minutes=int(duration.split(':')[1]))
    get_time = datetime.strptime(start, "%I:%M %p")
    get_new_time = get_time + delta
    diff = get_new_time.date() - get_time.date()
    if diff.days == 1:
        if args:
            for key, value in days_dict.items():
                if value == day:
                    new_day = key + 1
            return get_new_time.strftime("%-I:%M %p") + ', ' + days_dict[new_day] + ' ' + '(next day)'
        return get_new_time.strftime("%-I:%M %p") + ' ' + '(next day)'
    elif diff.days > 1:
        if args:
            for key, value in days_dict.items():
                if value == day:
                    new_day = key + diff.days
            while new_day > 7:
                new_day -= 7
            return get_new_time.strftime("%-I:%M %p") + ', ' + days_dict[new_day] + ' ' + f'({abs(diff.days)} days later)'
        return get_new_time.strftime("%-I:%M %p") + ' ' + f'({abs(diff.days)} days later)'
    return get_new_time.strftime("%-I:%M %p") + ', ' + day if args else get_new_time.strftime("%-I:%M %p")


if __name__ == '__main__':
    add_time("3:00 PM", "3:10")
    # Returns: 6:10 PM

    add_time("11:30 AM", "2:32", "Monday")
    # Returns: 2:02 PM, Monday

    add_time("11:43 AM", "00:20")
    # Returns: 12:03 PM

    add_time("10:10 PM", "3:30")
    # Returns: 1:40 AM (next day)

    add_time("11:43 PM", "24:20", "tueSday")
    # Returns: 12:03 AM, Thursday (2 days later)

    add_time("6:30 PM", "205:12")
    # Returns: 7:42 AM (9 days later)