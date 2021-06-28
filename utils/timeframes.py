from datetime import datetime, timedelta, timezone


def week():
    end = datetime.now(tz=timezone(offset=-timedelta(hours=4)))
    start = end - timedelta(hours=168)
    return start, end


def month():
    end = datetime.now(tz=timezone(offset=-timedelta(hours=4)))
    start = end - timedelta(hours=730)
    return start, end


def to_datetime(*items):
    if len(items) == 1:
        return datetime.strptime(items[0], r"%d-%m-%Y")
    else:
        return [datetime.strptime(item, r"%d-%m-%Y") for item in items]
    
TIMEFRAMES = {'week': week, 'month': month}
