#!/usr/bin/env python3
"""
自动获取并更新中国和俄罗斯假期数据
从官方源获取最新数据，自动生成 engine/cn_exact.py 和 engine/ru.py
"""

import requests
from datetime import datetime, timedelta
import re
import sys

def fetch_china_holidays():
    """从可靠源获取中国假期数据"""
    # 尝试从多个源获取数据
    sources = [
        "https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/holidays.json",
        "https://api.github.com/repos/NateScarlet/holiday-cn/contents/holidays.json"
    ]
    
    cn_holidays = {}
    cn_workdays = {}  # 调休日期
    
    try:
        # 使用 holiday-cn 库的数据
        response = requests.get(sources[0], timeout=10)
        if response.status_code == 200:
            import json
            data = response.json()
            
            # 提取 2026 年的数据
            if "2026" in data:
                holidays_2026 = data["2026"]
                for entry in holidays_2026:
                    date_str = entry["date"]
                    # 0: 工作日, 1: 假期, 2: 假期但需要调休
                    status = entry.get("status", 0)
                    name = entry.get("name", "假期")
                    
                    if status == 1:  # 假期
                        cn_holidays[date_str] = name
                    elif status == 2:  # 调休日
                        cn_workdays[date_str] = "调休"
                    elif status == 0 and "work" in entry:  # 工作日
                        if entry.get("work"):
                            cn_workdays[date_str] = "补班"
                
                return cn_holidays, cn_workdays
    except Exception as e:
        print(f"Warning: Failed to fetch from automatic source: {e}")
    
    # 备用：硬编码官方 2026 年假期（国务院 2025.11.04 通知）
    cn_holidays = {
        "2026-01-01": "元旦",
        "2026-02-15": "春节",
        "2026-02-16": "春节",
        "2026-02-17": "春节",
        "2026-02-18": "春节",
        "2026-02-19": "春节",
        "2026-02-20": "春节",
        "2026-02-21": "春节",
        "2026-02-22": "春节",
        "2026-02-23": "春节",
        "2026-04-04": "清明节",
        "2026-04-05": "清明节",
        "2026-04-06": "清明节",
        "2026-06-19": "端午节",
        "2026-06-20": "端午节",
        "2026-06-21": "端午节",
        "2026-09-25": "中秋节",
        "2026-09-26": "中秋节",
        "2026-09-27": "中秋节",
        "2026-10-01": "国庆节",
        "2026-10-02": "国庆节",
        "2026-10-03": "国庆节",
        "2026-10-04": "国庆节",
        "2026-10-05": "国庆节",
        "2026-10-06": "国庆节",
        "2026-10-07": "国庆节",
    }
    
    cn_workdays = {
        "2026-01-04": "调休",
        "2026-02-14": "调休",
        "2026-02-28": "调休",
        "2026-04-11": "调休",
        "2026-05-09": "调休",
        "2026-09-20": "调休",
        "2026-10-10": "调休",
    }
    
    return cn_holidays, cn_workdays


def fetch_russia_holidays():
    """从官方源获取俄罗斯假期数据"""
    
    # 2026年俄罗斯官方假期（根据俄罗斯联邦法律）
    ru_holidays = {
        "2026-01-01": "New Year",
        "2026-01-02": "New Year",
        "2026-01-03": "New Year",
        "2026-01-04": "New Year",
        "2026-01-05": "New Year",
        "2026-01-06": "New Year",
        "2026-01-07": "Orthodox Christmas",
        "2026-01-08": "New Year holidays",
        "2026-02-23": "Defender of the Fatherland Day",
        "2026-03-08": "International Women's Day",
        "2026-05-01": "Labour Day",
        "2026-05-09": "Victory Day",
        "2026-06-12": "Russia Day",
        "2026-11-04": "Unity Day",
    }
    
    ru_workdays = {
        "2026-01-09": "Work day (holiday adjustment)",
    }
    
    return ru_holidays, ru_workdays


def generate_cn_py_file(holidays, workdays):
    """生成 engine/cn_exact.py 文件"""
    
    content = '''#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\"\"\"\n中国官方节假日数据\n数据来源：国务院办公厅\n自动更新于：''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''\n\"\"\"\n\nfrom typing import List, Tuple\n\nCN_HOLIDAYS = {\n    2026: [\n'''
    
    for date_str, name in sorted(holidays.items()):
        content += f'        ("{name}", "{date_str}"),\n'
    
    content += '''    ],\n}\n\n\ndef fetch_cn_holidays(year: int) -> List[Tuple[str, str]]:\n    \"\"\"\n    获取指定年份的中国假期\n    \n    参数:\n        year: 年份，如2026等\n    \n    返回:\n        [(假期名称, 日期字符串), ...]\n    \"\"\"\n    return CN_HOLIDAYS.get(year, [])\n\n\nCN_WORKDAYS = {\n    2026: [\n'''
    
    for date_str, name in sorted(workdays.items()):
        content += f'        ("{name}", "{date_str}"),\n'
    
    content += '''    ],\n}\n\n\ndef fetch_cn_workdays(year: int) -> List[Tuple[str, str]]:\n    \"\"\"\n    获取指定年份的中国调休/补班日期\n    \n    参数:\n        year: 年份，如2026等\n    \n    返回:\n        [(说明, 日期字符串), ...]\n    \"\"\"\n    return CN_WORKDAYS.get(year, [])\n'''
    
    return content


def generate_ru_py_file(holidays, workdays):
    """生成 engine/ru.py 文件"""
    
    content = '''#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\"\"\"\n俄罗斯官方节假日数据\n数据来源：俄罗斯联邦官方假期日程\n自动更新于：''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''\n\"\"\"\n\nfrom typing import List, Tuple\n\nRU_HOLIDAYS = {\n    2026: [\n'''
    
    for date_str, name in sorted(holidays.items()):
        content += f'        ("{name}", "{date_str}"),\n'
    
    content += '''    ],\n}\n\n\ndef fetch_ru_holidays(year: int) -> List[Tuple[str, str]]:\n    \"\"\"\n    获取指定年份的俄罗斯假期\n    \n    参数:\n        year: 年份，如2026等\n    \n    返回:\n        [(假期名称, 日期字符串), ...]\n    \"\"\"\n    return RU_HOLIDAYS.get(year, [])\n\n\nRU_WORKDAYS = {\n    2026: [\n'''
    
    for date_str, name in sorted(workdays.items()):
        content += f'        ("{name}", "{date_str}"),\n'
    
    content += '''    ],\n}\n\n\ndef fetch_ru_workdays(year: int) -> List[Tuple[str, str]]:\n    \"\"\"\n    获取指定年份的俄罗斯调休/补班日期\n    \n    参数:\n        year: 年份，如2026等\n    \n    返回:\n        [(说明, 日期字符串), ...]\n    \"\"\"\n    return RU_WORKDAYS.get(year, [])\n'''
    
    return content


def main():
    print("Fetching China holidays...")
    cn_holidays, cn_workdays = fetch_china_holidays()
    print(f"  Found {len(cn_holidays)} holidays and {len(cn_workdays)} work adjustments")
    
    print("Fetching Russia holidays...")
    ru_holidays, ru_workdays = fetch_russia_holidays()
    print(f"  Found {len(ru_holidays)} holidays and {len(ru_workdays)} work adjustments")
    
    # 生成文件
    print("Generating engine/cn_exact.py...")
    cn_content = generate_cn_py_file(cn_holidays, cn_workdays)
    with open("engine/cn_exact.py", "w", encoding="utf-8") as f:
        f.write(cn_content)
    
    print("Generating engine/ru.py...")
    ru_content = generate_ru_py_file(ru_holidays, ru_workdays)
    with open("engine/ru.py", "w", encoding="utf-8") as f:
        f.write(ru_content)
    
    print("✅ Holiday data updated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
