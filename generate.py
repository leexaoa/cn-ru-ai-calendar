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

def main():
    year = datetime.now().year

    # 🇨🇳 中国（精确调休）
    cn_raw = fetch_cn_raw(year)
    holidays, workdays = parse_cn(cn_raw)

    cn_events = []
    for d in holidays:
        cn_events.append({"date": d, "name": "🇨🇳 节假日"})
    for d in workdays:
        cn_events.append({"date": d, "name": "🇨🇳 补班"})

    # 🇷🇺 俄罗斯
    ru_events = fetch_ru(year)

    # 合并
    events = cn_events + ru_events

    build_ics(events)

if __name__ == "__main__":
    main()
