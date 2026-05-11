from ics import Calendar, Event

cal = Calendar()

ru = [
    ("🇷🇺 New Year", "2026-01-01"),
    ("🇷🇺 Victory Day", "2026-05-09"),
]

cn = [
    ("🇨🇳 Spring Festival", "2026-02-17"),
    ("🇨🇳 National Day", "2026-10-01"),
]

def add(name, day):
    e = Event()
    e.name = name
    e.begin = day
    e.make_all_day()
    cal.events.add(e)

for i in ru:
    add(i[0], i[1])

for i in cn:
    add(i[0], i[1])

with open("calendar.ics", "w") as f:
    f.writelines(cal)
