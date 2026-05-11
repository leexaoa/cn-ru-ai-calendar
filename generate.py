from datetime import datetime
from icalendar import Calendar, Event

from engine.cn_exact import fetch_cn_raw, parse_cn
from engine.ru import fetch_ru


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

    for d in holidays:
        events.append({
            "date": d,
            "name": "🇨🇳 法定假期"
        })

    for d in workdays:
        events.append({
            "date": d,
            "name": "🇨🇳 补班（调休）"
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
