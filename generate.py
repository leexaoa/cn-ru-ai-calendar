from datetime import datetime
from icalendar import Calendar, Event

from engine.cn_exact import fetch_cn_raw, parse_cn
from engine.ru import fetch_ru
from engine.cluster import cluster_dates, is_golden_week


def build_ics(events):
    cal = Calendar()

    for e in events:
        ev = Event()
        ev.add("summary", e["name"])
        ev.add("dtstart", datetime.strptime(e["date"], "%Y-%m-%d").date())
        ev.add("dtend", datetime.strptime(e["date"], "%Y-%m-%d").date())
        cal.add_component(ev)

    with open("calendar.ics", "wb") as f:
        f.write(cal.to_ical())


def build_cn_events(holidays, workdays):
    events = []

    # 🧠 连休识别
    holiday_clusters = cluster_dates(holidays)
    work_clusters = cluster_dates(workdays)

    # 🟢 假期 / 黄金周
    for start, end in holiday_clusters:
        label = "黄金周" if is_golden_week(start, end) else "连休"

        events.append({
            "date": start.strftime("%Y-%m-%d"),
            "name": f"🇨🇳 {label} {start} → {end}"
        })

    # 🔴 补班区间
    for start, end in work_clusters:
        events.append({
            "date": start.strftime("%Y-%m-%d"),
            "name": f"🇨🇳 补班区间 {start} → {end}"
        })

    return events


def main():
    year = datetime.now().year

    # 🇨🇳 中国调休数据
    cn_raw = fetch_cn_raw(year)
    holidays, workdays = parse_cn(cn_raw)

    cn_events = build_cn_events(holidays, workdays)

    # 🇷🇺 俄罗斯节日
    ru_events = fetch_ru(year)

    # 合并
    events = cn_events + ru_events

    build_ics(events)


if __name__ == "__main__":
    main()
