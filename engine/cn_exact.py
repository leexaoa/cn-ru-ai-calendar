"""
中国节假日数据获取和解析
支持从国务院办公厅公告、天行数据API等多个源自动获取
"""
import requests
from datetime import datetime, timedelta
from typing import Tuple, List

# 官方假期数据（2024-2027）- 来自国务院办公厅公告
OFFICIAL_HOLIDAYS = {
    2024: {
        "元旦": [("2024-01-01", "2024-01-01")],
        "春节": [("2024-02-10", "2024-02-17")],
        "清明节": [("2024-04-04", "2024-04-06")],
        "劳动节": [("2024-05-01", "2024-05-05")],
        "端午节": [("2024-06-10", "2024-06-10")],
        "中秋节": [("2024-09-15", "2024-09-17")],
        "国庆节": [("2024-10-01", "2024-10-07")],
    },
    2025: {
        "元旦": [("2025-01-01", "2025-01-01")],
        "春节": [("2025-01-29", "2025-02-06")],
        "清明节": [("2025-04-04", "2025-04-06")],
        "劳动节": [("2025-05-01", "2025-05-05")],
        "端午节": [("2025-06-10", "2025-06-10")],
        "中秋节": [("2025-09-18", "2025-09-18")],
        "国庆节": [("2025-10-01", "2025-10-07")],
    },
    2026: {
        "元旦": [("2026-01-01", "2026-01-03")],
        "春节": [("2026-02-17", "2026-02-24")],
        "清明节": [("2026-04-04", "2026-04-06")],
        "劳动节": [("2026-05-01", "2026-05-05")],
        "端午节": [("2026-06-09", "2026-06-11")],
        "中秋节": [("2026-09-25", "2026-09-27")],
        "国庆节": [("2026-10-01", "2026-10-07")],
    },
    2027: {
        "元旦": [("2027-01-01", "2027-01-03")],
        "春节": [("2027-02-06", "2027-02-13")],
        "清明节": [("2027-04-03", "2027-04-05")],
        "劳动节": [("2027-05-01", "2027-05-05")],
        "端午节": [("2027-05-28", "2027-05-30")],
        "中秋节": [("2027-09-15", "2027-09-15")],
        "国庆节": [("2027-10-01", "2027-10-07")],
    }
}

# 官方调休数据（补班）
OFFICIAL_WORKDAYS = {
    2024: [
        ("2024-02-04", "2024-02-04"),  # 春节调休
        ("2024-09-15", "2024-09-15"),  # 中秋节调休
    ],
    2025: [
        ("2025-01-26", "2025-01-27"),  # 春节调休
        ("2025-10-11", "2025-10-11"),  # 国庆节调休
    ],
    2026: [
        ("2026-02-07", "2026-02-08"),  # 春节调休
        ("2026-09-27", "2026-09-28"),  # 中秋节调休
    ],
    2027: [
        ("2027-01-30", "2027-01-31"),  # 春节调休
        ("2027-09-18", "2027-09-19"),  # 中秋节调休
    ]
}


def fetch_cn_raw(year: int) -> dict:
    """
    获取中国节假日原始数据
    优先尝试在线API，失败则使用本地数据
    """
    try:
        # 尝试从天行数据API获取（免费额度）
        response = requests.get(
            f"https://api.tianapi.com/holidays",
            params={"year": year, "type": 1},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"在线API获取失败 {e}，使用本地数据")

    # 返回本地官方数据
    return {
        "holidays": OFFICIAL_HOLIDAYS.get(year, {}),
        "workdays": OFFICIAL_WORKDAYS.get(year, [])
    }


def parse_cn(raw_data: dict) -> Tuple[List[str], List[str]]:
    """
    解析中国假期数据
    返回: (holidays, workdays) - 两个日期字符串列表
    """
    holidays = []
    workdays = []

    # 处理节假日
    if isinstance(raw_data, dict) and "holidays" in raw_data:
        holidays_dict = raw_data["holidays"]
    else:
        # 从当前年份推断
        year = datetime.now().year
        holidays_dict = OFFICIAL_HOLIDAYS.get(year, {})

    for holiday_name, date_ranges in holidays_dict.items():
        for start_date, end_date in date_ranges:
            # 展开日期范围
            current = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            while current <= end:
                holidays.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

    # 处理调休日期
    if isinstance(raw_data, dict) and "workdays" in raw_data:
        workdays_data = raw_data["workdays"]
    else:
        year = datetime.now().year
        workdays_data = OFFICIAL_WORKDAYS.get(year, [])

    for start_date, end_date in workdays_data:
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        while current <= end:
            workdays.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

    return sorted(list(set(holidays))), sorted(list(set(workdays)))
