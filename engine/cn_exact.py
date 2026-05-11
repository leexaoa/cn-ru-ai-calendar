import requests

def fetch_cn_raw(year):
    url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
    return requests.get(url).json()

def parse_cn(data):
    holidays = []
    workdays = []

    for item in data:
        if item.get("isOffDay"):
            holidays.append(item["date"])
        if item.get("isWorkDay"):
            workdays.append(item["date"])

    return holidays, workdays
