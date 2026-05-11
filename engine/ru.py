"""
俄罗斯节假日数据
数据来源：俄罗斯联邦官方假期日程
自动更新于：2026-05-11 13:23:22
"""

def fetch_ru_holidays():
    """获取俄罗斯假期数据，返回 [(假期名称, 日期字符串), ...]"""
    holidays = [
        ("New Year", "2026-01-01"),
        ("New Year", "2026-01-02"),
        ("New Year", "2026-01-03"),
        ("New Year", "2026-01-04"),
        ("New Year", "2026-01-05"),
        ("New Year", "2026-01-06"),
        ("Orthodox Christmas", "2026-01-07"),
        ("New Year holidays", "2026-01-08"),
        ("Defender of the Fatherland Day", "2026-02-23"),
        ("International Women's Day", "2026-03-08"),
        ("Labour Day", "2026-05-01"),
        ("Victory Day", "2026-05-09"),
        ("Russia Day", "2026-06-12"),
        ("Unity Day", "2026-11-04"),
    ]
    return holidays


def fetch_ru_workdays():
    """获取俄罗斯调休/补班日期，返回 [(说明, 日期字符串), ...]"""
    workdays = [
        ("Work day (holiday adjustment)", "2026-01-09"),
    ]
    return workdays
