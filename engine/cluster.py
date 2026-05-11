from datetime import datetime, timedelta

def to_date(d):
    return datetime.strptime(d, "%Y-%m-%d").date()


def cluster_dates(dates):
    """
    把连续日期合并成区间
    """
    if not dates:
        return []

    dates = sorted([to_date(d) for d in dates])

    clusters = []
    start = dates[0]
    prev = dates[0]

    for d in dates[1:]:
        if (d - prev).days == 1:
            prev = d
        else:
            clusters.append((start, prev))
            start = d
            prev = d

    clusters.append((start, prev))
    return clusters
