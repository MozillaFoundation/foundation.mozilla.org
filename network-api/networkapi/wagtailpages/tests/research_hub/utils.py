import datetime


def days_ago(n: int):
    return datetime.date.today() - datetime.timedelta(days=n)
