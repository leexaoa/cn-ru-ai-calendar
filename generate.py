#!/usr/bin/env python3
"""
生成中国和俄罗斯节假日的 iCalendar 文件
"""
import sys
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from engine.cn_exact import fetch_cn_raw, parse_cn
from engine.ru import fetch_ru_holidays

def generate_calendar(year=None):
    """生成日历文件"""
    if year is None:
        year = datetime.now().year
    
    # 创建日历对象
    cal = Calendar()
    cal.add('prodid', '-//CN-RU Holiday Calendar//leexaoa//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'China & Russia Holidays')
    cal.add('x-wr-caldesc', 'Chinese and Russian holidays calendar')
    cal.add('x-wr-timezone', 'Asia/Shanghai')

    # 获取中国假期
    print(f"[INFO] 获取 {year} 年中国假期...")
    cn_raw = fetch_cn_raw(year)
    cn_holidays, cn_workdays = parse_cn(cn_raw)
    print(f"[INFO] 中国假期数: {len(cn_holidays)}")
    print(f"[INFO] 中国调休数: {len(cn_workdays)}")

    # 获取俄罗斯假期
    print(f"[INFO] 获取 {year} 年俄罗斯假期...")
    ru_holidays = fetch_ru_holidays(year)
    print(f"[INFO] 俄罗斯假期数: {len(ru_holidays)}")

    # 添加中国假期到日历
    for date_str in cn_holidays:
        event = Event()
        event.add('summary', '🇨🇳 Chinese Holiday')
        event.add('dtstart', datetime.strptime(date_str, '%Y-%m-%d').date())
        event.add('dtend', (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).date())
        event.add('categories', 'China Holiday')
        event.add('description', 'China National Holiday')
        event.add('transp', 'TRANSPARENT')
        cal.add_component(event)

    # 添加中国调休到日历
    for date_str in cn_workdays:
        event = Event()
        event.add('summary', '⚠️ 补班 (Working Day)')
        event.add('dtstart', datetime.strptime(date_str, '%Y-%m-%d').date())
        event.add('dtend', (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).date())
        event.add('categories', 'China Workday')
        event.add('description', 'Make-up Working Day')
        event.add('transp', 'OPAQUE')
        cal.add_component(event)

    # 添加俄罗斯假期到日历
    for holiday_name, date_str in ru_holidays:
        event = Event()
        event.add('summary', f'🇷🇺 {holiday_name}')
        event.add('dtstart', datetime.strptime(date_str, '%Y-%m-%d').date())
        event.add('dtend', (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).date())
        event.add('categories', 'Russia Holiday')
        event.add('description', f'Russian Holiday: {holiday_name}')
        event.add('transp', 'TRANSPARENT')
        cal.add_component(event)

    # 保存到文件
    with open('calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"\n[SUCCESS] 日历已生成: calendar.ics")
    print(f"[INFO] 共添加事件数: {len(cn_holidays) + len(cn_workdays) + len(ru_holidays)}")

if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year
    generate_calendar(year)
