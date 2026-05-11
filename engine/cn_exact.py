def parse_cn(data):
    # 这个数据源直接返回的是假期日期列表
    holidays = data if isinstance(data, list) else []

    workdays = []

    return holidays, workdays
