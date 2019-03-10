from datetime import datetime


def get_timestamp_ms():
    return int(round(datetime.now().timestamp() * 1000))


def get_timestamp_s():
    return int(round(datetime.now().timestamp()))
