import holidays

def fetch_ru(year):
    ru = holidays.Russia(years=year)
    return [{"date": str(d), "name": n} for d, n in ru.items()]
