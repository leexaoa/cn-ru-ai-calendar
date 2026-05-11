#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from datetime import datetime, timedelta
import urllib.request
import urllib.error

def fetch_cn_holidays():
    """获取中国假期数据（根据国务院2025年11月4日官方通知）"""
    
    # 2026年中国官方假期
    cn_holidays = {
        # 元旦：1月1日（周四）至3日（周六）放假调休，共3天
        "2026-01-01": "元旦",
        "2026-01-02": "元旦",
        "2026-01-03": "元旦",
        # 春节：2月15日（农历腊月二十八、周日）至23日（农历正月初七、周一）放假调休，共9天
        "2026-02-15": "春节",
        "2026-02-16": "春节",
        "2026-02-17": "春节",
        "2026-02-18": "春节",
        "2026-02-19": "春节",
        "2026-02-20": "春节",
        "2026-02-21": "春节",
        "2026-02-22": "春节",
        "2026-02-23": "春节",
        # 清明节：4月4日（周六）至6日（周一）放假，共3天
        "2026-04-04": "清明节",
        "2026-04-05": "清明节",
        "2026-04-06": "清明节",
        # 劳动节：5月1日（周五）至5日（周二）放假调休，共5天
        "2026-05-01": "劳动节",
        "2026-05-02": "劳动节",
        "2026-05-03": "劳动节",
        "2026-05-04": "劳动节",
        "2026-05-05": "劳动节",
        # 端午节：6月19日（周五）至21日（周日）放假，共3天
        "2026-06-19": "端午节",
        "2026-06-20": "端午节",
        "2026-06-21": "端午节",
        # 中秋节：9月25日（周五）至27日（周日）放假，共3天
        "2026-09-25": "中秋节",
        "2026-09-26": "中秋节",
        "2026-09-27": "中秋节",
        # 国庆节：10月1日（周四）至7日（周三）放假调休，共7天
        "2026-10-01": "国庆节",
        "2026-10-02": "国庆节",
        "2026-10-03": "国庆节",
        "2026-10-04": "国庆节",
        "2026-10-05": "国庆节",
        "2026-10-06": "国庆节",
        "2026-10-07": "国庆节",
    }
    
    # 调休补班工作日
    cn_workdays = {
        # 元旦：1月4日（周日）上班
        "2026-01-04": "调休补班（元旦）",
        # 春节：2月14日（周六）、2月28日（周六）上班
        "2026-02-14": "调休补班（春节）",
        "2026-02-28": "调休补班（春节）",
        # 劳动节：5月9日（周六）上班
        "2026-05-09": "调休补班（劳动节）",
        # 国庆节：9月20日（周日）、10月10日（周六）上班
        "2026-09-20": "调休补班（国庆节）",
        "2026-10-10": "调休补班（国庆节）",
    }
    
    return cn_holidays, cn_workdays

def fetch_russia_holidays():
    """从Google Calendar获取俄罗斯假期数据"""
    
    try:
        # 尝试从Google Calendar获取俄罗斯假期
        url = "https://calendar.google.com/calendar/ical/en.russian%23holiday%40group.v.calendar.google.com/public/basic.ics"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
        
        # 解析ICS格式的假期数据
        ru_holidays = {}
        ru_workdays = {}
        
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if line.startswith('DTSTART;VALUE=DATE:'):
                date_str = line.replace('DTSTART;VALUE=DATE:', '')
                # 格式转换: 20260101 -> 2026-01-01
                if len(date_str) >= 8:
                    formatted_date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    
                    # 查找对应的SUMMARY（假期名称）
                    summary = ""
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith('DTSTART') and not lines[j].startswith('BEGIN:'):
                        if lines[j].startswith('SUMMARY:'):
                            summary = lines[j].replace('SUMMARY:', '')
                            break
                        j += 1
                    
                    if summary and "holiday" not in summary.lower():
                        # 这可能是工作日
                        ru_workdays[formatted_date] = summary
                    elif summary:
                        ru_holidays[formatted_date] = summary
            
            i += 1
        
        # 如果成功获取到假期数据
        if ru_holidays:
            return ru_holidays, ru_workdays
    
    except Exception as e:
        print(f"⚠️  从Google Calendar获取俄罗斯假期失败: {e}")
    
    # 降级到静态数据
    ru_holidays = {
        # 2026年俄罗斯官方假期
        "2026-01-01": "New Year",
        "2026-01-02": "New Year",
        "2026-01-03": "New Year",
        "2026-01-04": "New Year",
        "2026-01-05": "New Year",
        "2026-01-06": "New Year",
        "2026-01-07": "Orthodox Christmas",
        "2026-01-08": "New Year holidays",
        "2026-02-23": "Defender of the Fatherland Day",
        "2026-03-08": "International Women's Day",
        "2026-05-01": "Labour Day",
        "2026-05-09": "Victory Day",
        "2026-06-12": "Russia Day",
        "2026-11-04": "Unity Day",
    }
    
    ru_workdays = {}
    
    return ru_holidays, ru_workdays

def get_all_holidays():
    """获取所有假期数据"""
    cn_holidays, cn_workdays = fetch_cn_holidays()
    ru_holidays, ru_workdays = fetch_russia_holidays()
    
    return {
        'cn_holidays': cn_holidays,
        'cn_workdays': cn_workdays,
        'ru_holidays': ru_holidays,
        'ru_workdays': ru_workdays,
    }
