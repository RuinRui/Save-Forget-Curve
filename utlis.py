from datetime import datetime, timedelta


def get_utc8_now_datetimestr():
    utc8_datetime = datetime.now()
    utc8_datestr = datetime.strftime(utc8_datetime, "%Y-%m-%d %H:%M:%S")

    return utc8_datestr


def datetimestr_to_datetime(datestr):
    utc8_datetime = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
    return utc8_datetime


def sec_to_regular_time(sec: float):
    sec, min, hour, day = int(sec), 0, 0, 0
    if sec >= 60:
        min = sec // 60
        if min >= 60:
            hour = min // 60
            min = min % 60
            if hour >= 24:
                day = hour // 24
                hour = hour % 24

    return "%d天%d时%d分" % (day, hour, min)
