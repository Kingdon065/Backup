#! python3
# _*_ coding:utf-8 _*_
# @Author: Evil Mat
# @Date: 2020/8/24 12:27

import datetime

SHORT = 0
LONG = 1

def get_now_datetime(format=LONG, seg='-'):
    now = datetime.datetime.now()
    date_time = ''
    if format == LONG:
        date_time = now.strftime(f'%Y{seg}%m{seg}%d_%H:%M:%S')
    elif format == SHORT:
        date_time = now.strftime(f'%Y{seg}%m{seg}%d_%H:%M')
    return date_time

