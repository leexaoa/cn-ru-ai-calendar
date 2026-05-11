"""
中国节假日数据模块
从holiday-cn官方源获取中国法定节假日和调休补班数据
自动更新于：2026-05-11
"""

import requests
from typing import List, Tuple


def fetch_cn_holidays(year: int) -> List[Tuple[str, str]]:
    """
    从holiday-cn源获取指定年份的中国假期和调休数据
    
    参数：
        year: 四位数年份 (如 2026)
    
    返回：
        列表，包含 (假期/调休名称, 日期字符串) 元组
        例如：[('春节', '2026-02-17'), ('调休（春节）', '2026-02-14')]
    """
    try:
        url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        holidays = []
        
        # holiday-cn新版格式: {"days": [{"date": "2026-01-01", "name": "元旦", "isOffDay": true}]}
        # isOffDay: true = 假期/休息日，false = 调休补班
        
        if not data or 'days' not in data:
            return []
        
        days_data = data.get('days', [])
        
        # 处理days是列表的情况（当前holiday-cn格式）
        if isinstance(days_data, list):
            for day in days_data:
                if not isinstance(day, dict):
                    continue
                    
                date_str = day.get('date')
                name = day.get('name', '')
                is_off_day = day.get('isOffDay')  # true: 假期, false: 调休
                
                if date_str and name:
                    if is_off_day:  # 假期/休息日
                        holidays.append((name, date_str))
                    else:  # 调休补班
                        holidays.append((f"调休（{name}）", date_str))
        
        # 向后兼容处理：days是字典的情况（旧版格式）
        elif isinstance(days_data, dict):
            for date_str, day_info in days_data.items():
                if not isinstance(day_info, dict):
                    continue
                    
                name = day_info.get('name', '')
                day_type = day_info.get('type')  # 旧格式: 1=假期, 2=调休
                
                if name:
                    if day_type == 1:  # 假期
                        holidays.append((name, date_str))
                    elif day_type == 2:  # 调休补班
                        holidays.append((f"调休（{name}）", date_str))
        
        return holidays
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 获取 {year} 年中国假期失败: {e}")
        return []
    except Exception as e:
        print(f"  ❌ 处理 {year} 年中国假期数据失败: {e}")
        return []
