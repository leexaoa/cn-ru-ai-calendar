"""
中国节假日数据模块
从官方holiday-cn源自动获取中国假期数据
自动更新于：2026-05-11
"""

import requests
from typing import List, Tuple


def fetch_cn_holidays(year: int) -> List[Tuple[str, str]]:
    """
    从官方holiday-cn源自动获取指定年份的中国假期数据
    
    参数：
        year: 四位数年份 (如 2026)
    
    返回：
        列表，包含 (假期名称, 日期字符串) 元组
        例如：[('元旦', '2026-01-01'), ('春节', '2026-02-17')]
    """
    try:
        # 使用JSDelivr加速的holiday-cn数据源
        # 自动从国务院公告抓取，包含调休补班信息
        url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        holidays = []
        
        # 将官方数据转换为 [(name, date_str), ...] 格式
        for day in data.get('days', []):
            date = day['date']
            name = day['name']
            is_off = day['isOffDay']
            
            # 只记录假日和调休日期（isOffDay为true的都是非工作日）
            if is_off:
                holidays.append((name, date))
        
        return holidays
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 获取 {year} 年中国假期失败: {e}")
        return []
    except Exception as e:
        print(f"  ❌ 处理 {year} 年中国假期数据失败: {e}")
        return []
