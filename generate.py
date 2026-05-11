"""
中国-俄罗斯节假日日历生成脚本
自动生成 iCalendar 格式的节假日日历
"""
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from engine.cn_exact import fetch_cn_raw, parse_cn
from engine.ru import fetch_ru
from engine.cluster import cluster_dates, is_golden_week


def build_ics(events, filename="calendar.ics"):
    """
    将事件列表转换为 iCalendar 格式并保存
    """
    cal = Calendar()
    cal.add('prodid', '-//CN-RU Holiday Calendar//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', '🇨🇳🇷🇺 中国-俄罗斯节假日')
    cal.add('x-wr-caldesc', '中国和俄罗斯的节假日、调休和黄金周日历')
    cal.add('x-wr-timezone', 'Asia/Shanghai')
    cal.add('refresh-interval;value=duration', 'P1M')  # 每月刷新一次
    cal.add('color', '#FF6B6B')

    for e in events:
        ev = Event()
        ev.add('summary', e['name'])
        
        # 处理日期
        start_date = datetime.strptime(e['date'], "%Y-%m-%d").date()
        end_date = start_date
        
        # 如果有 end_date，使用它
        if 'end_date' in e:
            end_date = datetime.strptime(e['end_date'], "%Y-%m-%d").date()
        
        ev.add('dtstart', start_date)
        # iCalendar 标准：dtend 应该是假期结束后的日期
        # 所以如果假期是 1-3 日，dtend 应该是 4 日
        ev.add('dtend', end_date + timedelta(days=1))
        
        # 添加描述
        if 'description' in e:
            ev.add('description', e['description'])
        
        # 标记为全天事件
        ev.add('transp', 'TRANSPARENT')  # 不显示为忙碌时间
        
        cal.add_component(ev)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"✅ 日历文件已生成: {filename}")
    print(f"📊 总事件数: {len(events)}")


def build_cn_events(holidays, workdays):
    """
    构建中国节假日事件列表
    """
    events = []

    # 连休识别
    holiday_clusters = cluster_dates(holidays)
    work_clusters = cluster_dates(workdays)

    # 假期 / 黄金周
    for start, end in holiday_clusters:
        days = (end - start).days + 1
        label = "🔱 黄金周" if is_golden_week(start, end) else "🇨🇳 连休"

        if days == 1:
            name = f"{label} {start.strftime('%m-%d')}"
        else:
            name = f"{label} {start.strftime('%m-%d')} ~ {end.strftime('%m-%d')} ({days}天)"

        events.append({
            "date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "name": name,
            "description": f"假期: {days}天"
        })

    # 补班区间
    for start, end in work_clusters:
        days = (end - start).days + 1
        
        if days == 1:
            name = f"🔴 补班 {start.strftime('%m-%d')}"
        else:
            name = f"🔴 补班 {start.strftime('%m-%d')} ~ {end.strftime('%m-%d')} ({days}天)"

        events.append({
            "date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "name": name,
            "description": f"补班: {days}天"
        })

    return events


def build_ru_events(ru_events):
    """
    构建俄罗斯节假日事件列表
    """
    events = []

    for e in ru_events:
        # 计算天数
        start = datetime.strptime(e['start_date'], "%Y-%m-%d")
        end = datetime.strptime(e['end_date'], "%Y-%m-%d")
        days = (end - start).days + 1

        events.append({
            "date": e['date'],
            "end_date": e['end_date'],
            "name": e['name'],
            "description": f"俄罗斯假期: {days}天"
        })

    return events


def main():
    """
    主函数：生成当前和未来几年的节假日日历
    """
    current_year = datetime.now().year
    years = [current_year, current_year + 1, current_year + 2]  # 当前年及后两年

    all_events = []

    print("🇨🇳 正在获取中国假期数据...")
    for year in years:
        try:
            cn_raw = fetch_cn_raw(year)
            holidays, workdays = parse_cn(cn_raw)
            cn_events = build_cn_events(holidays, workdays)
            all_events.extend(cn_events)
            print(f"  ✓ {year}年中国假期: {len(cn_events)}个事件")
        except Exception as e:
            print(f"  ✗ {year}年中国假期获取失败: {e}")

    print("🇷🇺 正在获取俄罗斯假期数据...")
    for year in years:
        try:
            ru_raw = fetch_ru(year)
            ru_events = build_ru_events(ru_raw)
            all_events.extend(ru_events)
            print(f"  ✓ {year}年俄罗斯假期: {len(ru_events)}个事件")
        except Exception as e:
            print(f"  ✗ {year}年俄罗斯假期获取失败: {e}")

    # 按日期排序
    all_events.sort(key=lambda x: x['date'])

    # 生成日历文件
    print("\n📝 正在生成 iCalendar 文件...")
    build_ics(all_events)
    print("\n✨ 完成！")


if __name__ == "__main__":
    main()
