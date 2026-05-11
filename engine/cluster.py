"""
节假日聚类和黄金周识别
将单个日期合并成连续的日期范围，并识别黄金周
"""
from datetime import datetime, timedelta
from typing import List, Tuple


def cluster_dates(dates: List[str]) -> List[Tuple[datetime, datetime]]:
    """
    将日期列表聚类成连续的日期范围
    输入: ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-05", ...]
    输出: [
        (datetime(2024, 1, 1), datetime(2024, 1, 3)),
        (datetime(2024, 1, 5), datetime(2024, 1, 5)),
        ...
    ]
    """
    if not dates:
        return []

    # 转换为datetime对象并排序
    date_objs = sorted([datetime.strptime(d, "%Y-%m-%d") for d in dates])

    clusters = []
    start = date_objs[0]
    end = date_objs[0]

    for i in range(1, len(date_objs)):
        current = date_objs[i]
        
        # 如果日期连续（相差1天），则延续end
        if (current - end).days == 1:
            end = current
        else:
            # 日期不连续，保存当前集群，开始新集群
            clusters.append((start, end))
            start = current
            end = current

    # 添加最后一个集群
    clusters.append((start, end))

    return clusters


def is_golden_week(start: datetime, end: datetime) -> bool:
    """
    判断是否为黄金周
    黄金周标准：
    - 春节：至少7天
    - 国庆：至少7天
    - 其他连休不算黄金周
    """
    days = (end - start).days + 1
    month = start.month

    # 春节黄金周（通常2月）或国庆黄金周（通常10月）
    if days >= 7 and month in (1, 2, 10):
        return True

    return False


def format_cluster(start: datetime, end: datetime, emoji: str = "") -> str:
    """
    格式化日期范围为可读的字符串
    示例: "2024-01-01 ~ 2024-01-07"
    """
    if start == end:
        return f"{emoji} {start.strftime('%Y-%m-%d')}"
    else:
        return f"{emoji} {start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"


def get_cluster_days(start: datetime, end: datetime) -> int:
    """获取日期范围的天数"""
    return (end - start).days + 1
