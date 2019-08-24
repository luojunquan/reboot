#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 21:52
# @Author  : luoxiaojian
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import psutil
import time
import MySQLdb as mysql

# db = mysql.connect(user="root", passwd="Admin123!", db="tiantian", host="10.0.2.15")
# db.autocommit(True)
# cur = db.cursor()

def getinfo():
    mem = psutil.virtual_memory()
    memtotal = mem.total
    memfree = mem.free
    mempercent = mem.percent
    memused = mem.used
    cpu = psutil.cpu_percent(1)
    print(memtotal, memfree, memused, mempercent, cpu)

getinfo()
# if __name__ == "__main__":
#     while True:
#         try:
#             memtotal, memfree, memused, mempercent, cpu = getinfo()
#             t = int(time.time())
#             sql = 'insert into stat (mem_free,mem_usage,mem_total,mempercent,cpu,time) value (%s,%s,%s,%s,%s,%s)' % (
#             memfree, memused, memtotal, mempercent, cpu, t)
#             cur.execute(sql)
#             time.sleep(10)
#         except Exception as e:
#             print(e)
