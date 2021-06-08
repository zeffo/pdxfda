from datetime import datetime, timedelta, timezone


def week():
    end = datetime.now(tz=timezone(offset=-timedelta(hours=4)))
    start = end - timedelta(hours=168)
    return start, end


def month():
    end = datetime.now(tz=timezone(offset=-timedelta(hours=4)))
    start = end - timedelta(hours=730)
    return start, end


def to_datetime(val):
    return datetime.strptime(val, r"%d-%m-%Y")
