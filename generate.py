#!/usr/bin/env python3
"""
中国 + 俄罗斯节假日日历生成器
自动生成 ICS 格式日历文件，支持订阅
"""

from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from engine.cn_exact import fetch_cn_raw, parse_cn
from engine.ru import get_russian_holidays

def generate_calendar():
    """生成包含中国和俄罗斯假期的 ICS 日历文件"""
    
    cal = Calendar()
    cal.add('prodid', '-//CN-RU Holiday Calendar//CN//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', '中国 + 俄罗斯节假日')
    cal.add('x-wr-timezone', 'UTC')
    cal.add('x-wr-caldesc', '中国和俄罗斯官方节假日日历')
    
    # 获取中国假期（当前和未来两年）
    current_year = datetime.now().year
    all_cn_holidays = {}
    
    for year in [current_year, current_year + 1, current_year + 2]:
        try:
            raw_data = fetch_cn_raw(year)
            cn_holidays, cn_workdays = parse_cn(raw_data)
            all_cn_holidays[year] = {
                'holidays': cn_holidays,
                'workdays': cn_workdays
            }
        except Exception as e:
            print(f"获取 {year} 年中国假期失败: {e}")
    
    # 获取俄罗斯假期
    ru_holidays = get_russian_holidays()
    
    # 添加中国假期到日历
    for year, data in all_cn_holidays.items():
        for holiday_date_str in data['holidays']:
            try:
                holiday_date = datetime.strptime(holiday_date_str, '%Y-%m-%d').date()
                event = Event()
                event.add('summary', '🇨🇳 中国假期')
                event.add('dtstart', holiday_date)
                event.add('dtend', holiday_date + timedelta(days=1))
                event.add('dtstamp', datetime.now(pytz.UTC))
                event.add('uid', f"cn-holiday-{holiday_date_str}@cn-ru-calendar")
                event.add('categories', 'Holiday,China')
                event.add('description', f'中国假期: {holiday_date_str}')
                event.add('transp', 'TRANSPARENT')
                cal.add_component(event)
            except Exception as e:
                print(f"添加中国假期 {holiday_date_str} 失败: {e}")
    
    # 添加俄罗斯假期到日历
    for holiday_date_str, holiday_name in ru_holidays.items():
        try:
            holiday_date = datetime.strptime(holiday_date_str, '%Y-%m-%d').date()
            event = Event()
            event.add('summary', f'🇷🇺 俄罗斯假期: {holiday_name}')
            event.add('dtstart', holiday_date)
            event.add('dtend', holiday_date + timedelta(days=1))
            event.add('dtstamp', datetime.now(pytz.UTC))
            event.add('uid', f"ru-holiday-{holiday_date_str}@cn-ru-calendar")
            event.add('categories', 'Holiday,Russia')
            event.add('description', f'俄罗斯假期: {holiday_name}')
            event.add('transp', 'TRANSPARENT')
            cal.add_component(event)
        except Exception as e:
            print(f"添加俄罗斯假期 {holiday_date_str} 失败: {e}")
    
    # 保存到文件
    with open('calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
    
    print("✅ 日历文件已生成: calendar.ics")
    print(f"📅 包含 {len(all_cn_holidays)} 年的中国假期和俄罗斯假期")

if __name__ == '__main__':
    generate_calendar()
