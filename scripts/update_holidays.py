#!/usr/bin/env python3
"""自动更新中国和俄罗斯假期数据到日历"""

import requests
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from pathlib import Path


def fetch_cn_holidays(year):
    """从官方holiday-cn源自动获取中国假期数据"""
    try:
        # 使用JSDelivr加速的holiday-cn数据源，自动从国务院公告抓取
        url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        cn_holidays = {}
        
        # 将官方数据转换为字典格式
        for day in data.get('days', []):
            date = day['date']
            name = day['name']
            is_off = day['isOffDay']
            
            # 只记录假日和调休日期（isOffDay为true的都是非工作日）
            if is_off:
                cn_holidays[date] = name
        
        return cn_holidays
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 获取 {year} 年中国假期失败: {e}")
        return {}


def fetch_ru_holidays():
    """从谷歌日历获取俄罗斯假期"""
    try:
        # 俄罗斯官方假期Google Calendar (俄文)
        url = "https://calendar.google.com/calendar/ical/en.russian%23holiday%40group.v.calendar.google.com/public/basic.ics"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 解析ICS内容
        cal = Calendar.from_ical(response.content)
        ru_holidays = {}
        
        for component in cal.walk():
            if component.name == "VEVENT":
                dt = component.get('dtstart')
                if dt:
                    # 转换为日期字符串 YYYY-MM-DD
                    if hasattr(dt.dt, 'date'):
                        date_str = dt.dt.date().isoformat()
                    else:
                        date_str = dt.dt.isoformat()
                    
                    summary = str(component.get('summary', 'Holiday'))
                    ru_holidays[date_str] = summary
        
        return ru_holidays
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 获取俄罗斯假期失败: {e}")
        return {}


def create_ics_calendar(cn_holidays_all, ru_holidays_all):
    """创建ICS日历文件"""
    cal = Calendar()
    cal.add('prodid', '-//CN-RU Holiday Calendar//CN//')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'China & Russia Holidays')
    cal.add('x-wr-timezone', 'Asia/Shanghai')
    cal.add('x-wr-caldesc', 'China and Russia official holidays and makeup workdays')
    
    # 添加中国假期
    for date_str, name in cn_holidays_all.items():
        event = Event()
        event.add('summary', f'🇨🇳 {name}')
        event.add('dtstart', datetime.fromisoformat(date_str).date())
        event.add('dtend', (datetime.fromisoformat(date_str) + timedelta(days=1)).date())
        event.add('uid', f'cn-{date_str}@cn-ru-calendar')
        event.add('description', f'China: {name}')
        cal.add_component(event)
    
    # 添加俄罗斯假期
    for date_str, name in ru_holidays_all.items():
        event = Event()
        event.add('summary', f'🇷🇺 {name}')
        # 处理日期格式
        try:
            event_date = datetime.fromisoformat(date_str).date()
            event.add('dtstart', event_date)
            event.add('dtend', event_date + timedelta(days=1))
        except:
            continue
        event.add('uid', f'ru-{date_str}@cn-ru-calendar')
        event.add('description', f'Russia: {name}')
        cal.add_component(event)
    
    return cal


def main():
    """主函数"""
    print("\n📅 开始生成日历...")
    print(f"📍 当前年份: {datetime.now().year}")
    
    cn_holidays_all = {}
    ru_holidays_all = {}
    
    # 获取过去1年、当前年和未来2年的假期
    years_to_fetch = [2025, 2026, 2027, 2028]
    
    for year in years_to_fetch:
        print(f"\n🔄 处理 {year} 年...")
        
        # 获取中国假期
        print(f"  🇨🇳 获取中国假期...")
        cn_holidays = fetch_cn_holidays(year)
        if cn_holidays:
            print(f"     ✅ 成功获取 {len(cn_holidays)} 条数据")
            cn_holidays_all.update(cn_holidays)
        else:
            print(f"     ❌ 获取失败或无数据")
        
        # 仅在处理第一年时获取俄罗斯假期（因为Google Calendar源是全年的）
        if year == 2025:
            print(f"  🇷🇺 获取俄罗斯假期...")
            ru_holidays = fetch_ru_holidays()
            if ru_holidays:
                print(f"     ✅ 成功获取 {len(ru_holidays)} 条数据")
                ru_holidays_all.update(ru_holidays)
            else:
                print(f"     ❌ 获取失败或无数据")
    
    # 创建并保存日历
    cal = create_ics_calendar(cn_holidays_all, ru_holidays_all)
    
    output_file = Path(__file__).parent.parent / 'calendar.ics'
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())
    
    # 统计信息
    total_cn = len(cn_holidays_all)
    total_ru = len(ru_holidays_all)
    
    print(f"\n✅ 日历文件已生成!")
    print(f"   📊 总计: {total_cn} 个中国假期 + {total_ru} 个俄罗斯假期")
    print(f"   💾 文件: {output_file}")
    print(f"   🔗 订阅链接: https://leexaoa.github.io/cn-ru-ai-calendar/calendar.ics\n")


if __name__ == '__main__':
    main()
