# -*- coding: utf-8 -*-
import pymysql
import sys
import logging



def insert(job):
    logging.basicConfig(level=logging.DEBUG)
    conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='000000',db='spiderjob')
    cur = conn.cursor()
    cur.execute("select * from lagou where position_id=%s", job[1])
    if cur.fetchone():  # 库中已经有数据
        logging.info("data exists---" + "data id:" + job[1])
    else:  # 库中没有数据
        logging.info("new data---" + "data id:" + job[1])
        ret = cur.execute("insert into lagou(position_name, position_id, address, format_time, money,"
                          "requirement, company_name, industry, label, strengs, create_time)"
                          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [x.encode('utf-8') for x in job])
    conn.commit()
    cur.close()
    conn.close()
    # print(ret)
