"""
俄罗斯节假日数据模块
从Google Calendar官方源获取俄罗斯假期数据
自动更新于：2026-05-11
"""

import requests
from icalendar import Calendar
from datetime import datetime
from typing import List, Tuple


def fetch_ru_holidays(year: int) -> List[Tuple[str, str]]:
    """
    从Google Calendar获取指定年份的俄罗斯假期数据
    
    参数：
        year: 四位数年份 (如 2026)
    
    返回：
        列表，包含 (假期名称, 日期字符串) 元组
        例如：[('New Year', '2026-01-01'), ('Orthodox Christmas', '2026-01-07')]
    """
    try:
        # 俄罗斯官方假期Google Calendar
        url = "https://calendar.google.com/calendar/ical/en.russian%23holiday%40group.v.calendar.google.com/public/basic.ics"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 解析ICS格式内容
        cal = Calendar.from_ical(response.content)
        holidays = []
        
        for component in cal.walk():
            if component.name == "VEVENT":
                dt = component.get('dtstart')
                if dt:
                    # 转换为日期字符串 YYYY-MM-DD
                    if hasattr(dt.dt, 'date'):
                        date_str = dt.dt.date().isoformat()
                    else:
                        date_str = dt.dt.isoformat()
                    
                    # 只保留指定年份的假期
                    if date_str.startswith(str(year)):
                        summary = str(component.get('summary', 'Holiday'))
                        holidays.append((summary, date_str))
        
        return holidays
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 获取 {year} 年俄罗斯假期失败: {e}")
        return []
    except Exception as e:
        print(f"  ❌ 处理 {year} 年俄罗斯假期数据失败: {e}")
        return []
