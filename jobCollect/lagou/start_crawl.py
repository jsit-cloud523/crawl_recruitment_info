# -*- coding: utf-8 -*-
import requests
from lxml import etree
import sys
import random
import time
import global_var
import ua
from lagou import Lagou
import db


# # url = 'https://www.lagou.com'
# headers = {
#     'User-Agent': random.choice(ua.ua_pool),
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Host': 'www.lagou.com',
#     'Upgrade-Insecure-Requests': '1',
# }
# # s = requests.Session()
# # response = s.get(url, headers=headers)
# # selector = etree.HTML(response.text)
def process_one_cat(url, cat_list):
    PAGE_NUM_PROCESSING = 1
    global_var._init()
    global_var.set_value("PAGE_NUM_PROCESSING", PAGE_NUM_PROCESSING)
    global_var.set_value("isLastPage", False)
    while True:
        page_num = global_var.get_value('PAGE_NUM_PROCESSING')
        tmp_url = url + str(page_num) + "/"
        # getJobList(tmp_url)
        print("while True main:" + tmp_url)
        s = requests.Session()
        lg = Lagou()
        pagegen = lg.getJobListPerPage(tmp_url, s)
        for item in pagegen:
            time_wait = 1 + float(random.randint(1, 100)) / 20
            time.sleep(time_wait)
            print("休息时间：" + str(time_wait))
            for job in item:
                db.insert(job, cat_list)
        print("跳出生成器")
        print("休息5秒钟")
        time.sleep(5)

        if global_var.get_value("isLastPage"):
            print("----------爬取结束---------，共" + str(global_var.get_value('PAGE_NUM_PROCESSING')) + "页")
            break

lg = Lagou()
top_cat_dict = lg.get_all_positions()

for top_cat_key in top_cat_dict:
    # print(top_cat_key + ":" + top_cat_dict[top_cat_key])
    grade2_cat_dict = top_cat_dict[top_cat_key]
    for grade2_key in grade2_cat_dict:
        # print(grade2_key + ":" + grade2_cat_dict[grade2_key])
        grade3_cat_dict = grade2_cat_dict[grade2_key]

        for grade3_key in grade3_cat_dict:
            url = grade3_cat_dict[grade3_key]
            print(top_cat_key)
            print(grade2_key)
            print(grade3_key)
            cat_list = [top_cat_key, grade2_key, grade3_key]
            process_one_cat(url, cat_list)










