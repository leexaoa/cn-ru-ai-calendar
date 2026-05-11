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
        
        # holiday-cn的数据格式包含days列表，每个day有date、type和name
        # type: 0=工作日, 1=假期, 2=调休补班
        for day in data.get('days', []):
            date_str = day.get('date')
            day_type = day.get('type')
            name = day.get('name', '')
            
            # 处理假期 (type=1)
            if day_type == 1:
                if not name or name == '':
                    name = '假期'
                holidays.append((name, date_str))
            
            # 处理调休补班 (type=2)
            elif day_type == 2:
                if not name or name == '':
                    name = '调休补班'
                else:
                    # 在原名称后添加调休标记
                    name = f"调休（{name}）"
                holidays.append((name, date_str))
        
        return holidays
    
    except requests.exceptions.RequestException as e:
        return []
    except Exception as e:
        return []
