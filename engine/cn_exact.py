import requests

def fetch_cn_raw(year):
    url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
    return requests.get(url).json()


def parse_cn(data):
    """
    返回：
    holidays = 放假日
    workdays = 补班日
    """

    holidays = []
    workdays = []

    # 数据结构是 list of dict
    for item in data:
        date = item.get("date")

        # 放假日
        if item.get("isOffDay") is True:
            holidays.append(date)

        # 补班日（关键）
        if item.get("isWorkDay") is True:
            workdays.append(date)

    return holidays, workdays


def classify(date, holidays, workdays):
    """
    精确判断某一天状态
    """
    d = str(date)

    if d in workdays:
        return "workday"   # 补班
    if d in holidays:
        return "holiday"   # 放假
    return "normal"
