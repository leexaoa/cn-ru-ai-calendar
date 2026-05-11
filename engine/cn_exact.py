import requests

def fetch_cn_raw(year):
    url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
    return requests.get(url).json()


def parse_cn(data):
    """
    ⚠️ 当前数据源返回的是：list[str]
    """

    holidays = []

    if isinstance(data, list):
        holidays = data

    workdays = []

    return holidays, workdays


def classify(date, holidays, workdays):
    d = str(date)

    if d in workdays:
        return "workday"
    if d in holidays:
        return "holiday"
    return "normal"
