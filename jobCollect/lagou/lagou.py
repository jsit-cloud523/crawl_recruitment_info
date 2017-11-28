import random
import ua
from lxml import etree
import requests
import time
import global_var
import re
import logging


class Lagou:

    def __init__(self):
        self.url = 'https://www.lagou.com'
        self.headers = {
            'User-Agent': random.choice(ua.ua_pool),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': '1',
        }

    '''
    {'技术'：	{'后端开发'：{'java': 'https://www.lagou.com/zhaopin/java','C++': '...',...}}
    			{'移动开发': {...}}
    			.
    			.
    			.
    			.
    			.
    }
    .
    .
    .
    .
    '''
    def get_all_positions(self):
        s = requests.Session()
        response = s.get(self.url, headers=self.headers)
        selector = etree.HTML(response.text)
        top_cat_dict = {}
        for i in range(0, 7):

            '''
            以【技术】大类举例说明
            【后端开发】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[1]/dt/span
                2级分类【后端开发】下面的3级分类
                【Java   】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[1]/dd/a[1]
                【C++    】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[1]/dd/a[2]
                【PHP    】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[1]/dd/a[3]
            【移动开发】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[2]/dt/span
                2级分类【移动开发】下面的3级分类
                【HTML5  】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[2]/dd/a[1]
                【Android】：//*[@id="sidebar"]/div/div[1]/div[2]/dl[2]/dd/a[2]
            ……
            以【产品】大类举例说明
            【产品经理】：        //*[@id="sidebar"]/div/div[2]/div[2]/dl[1]/dt/span
                2级分类【产品经理】下面的3级分类
                【产品经理    】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[1]/dd/a[1]
                【网页产品经理】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[1]/dd/a[2]
                【移动产品经理】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[1]/dd/a[3]
            【产品设计师】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[2]/dt/span
                2级分类【产品设计师】下面的3级分类
                【网页产品设计师】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[2]/dd/a[1]
                【无线产品设计师】：//*[@id="sidebar"]/div/div[2]/div[2]/dl[2]/dd/a[2]    

                  对比结果 //*[@id="sidebar"]/div/div[2]/div[2]/dl[1]/dt/span
                                                     |            |   |
            代表1级大类中序号--------------------------            |   |
            代表2级分类中序号---------------------------------------   |
            dt代表2级分类，dd代表3级分类--------------------------------
            '''
            top_cat = selector.xpath('//*[@id="sidebar"]/div/div[' + str(i + 1) + ']/div[1]/div/h2/text()')[0]
            # 技术 产品 设计 运营 市场与销售 职能 金融
            top_cat_str = str(top_cat).strip()
            '''
            ['后端开发', '移动开发', '前端开发', '人工智能', '测试', '运维', 'DBA', '高端职位', '项目管理', '硬件开发', '企业软件']
            ['产品经理', '产品设计师', '高端职位']
            ['视觉设计', '交互设计', '用户研究', '高端职位']
            ['运营', '编辑', '客服', '高端职位']
            ['市场/营销', '公关', '销售', '供应链', '采购', '投资', '高端职位']
            ['人力资源', '行政', '财务', '法务', '高端职位']
            ['投融资', '风控', '审计税务', '高端职位']
            '''
            grade2_cat_list = selector.xpath('//*[@id="sidebar"]/div/div[' + str(i + 1) + ']/div[2]/dl/dt/span/text()')
            categories_dict_list = []
            # grade2_cat_list = ['后端开发', '移动开发', '前端开发', '人工智能', '测试', '运维', 'DBA', '高端职位', '项目管理', '硬件开发', '企业软件']
            # grade2_cat_dict:{'高端职位': {'CTO': 'https://www.lagou.com/zhaopin/CTO/',......}, '移动开发': {......}, ......}
            grade2_cat_dict = {}
            for j in range(0, len(grade2_cat_list)):
                # jobname_list = ['Java', 'C++', 'PHP', '数据挖掘', '搜索算法', '精准推荐', 'C', 'C#', '全栈工程师', '.NET', 'Hadoop', 'Python', 'Delphi', 'VB', 'Perl', 'Ruby', '
                jobname_list = selector.xpath(
                    '//*[@id="sidebar"]/div/div[' + str(i + 1) + ']/div[2]/dl[' + str(j + 1) + ']/dd/a/text()')
                link_list = selector.xpath(
                    '//*[@id="sidebar"]/div/div[' + str(i + 1) + ']/div[2]/dl[' + str(j + 1) + ']/dd/a/@href')
                '''
               key: 后端开发
               value: {'ASP': 'https://www.lagou.com/zhaopin/asp/', 'C#': 'https://www.lagou.com/zhaopin/C%23/', '全栈工程师': 'https://www.lagou.com/zhaopin/quanzhangongchengshi/', '.NET': 'https://www.lagou.com/zhaopin/.NET/', 'Java': 'https://www.lagou.com/zhaopin/Java/', 'Hadoop': 'https://www.lagou.com/zhaopin/Hadoop/', 'Perl': 'https://www.lagou.com/zhaopin/Perl/', 'PHP': 'https://www.lagou.com/zhaopin/PHP/', 'C': 'https://www.lagou.com/zhaopin/C/', 'Shell': 'https://www.lagou.com/zhaopin/shell/', '搜索算法': 'https://www.lagou.com/zhaopin/sousuosuanfa/', '
               '''
                grade2_cat_dict[grade2_cat_list[j]] = dict(zip(jobname_list, link_list))
            top_cat_dict[top_cat_str] = grade2_cat_dict
        return top_cat_dict


    def transtime(self, str):
        p = re.match(r'(\d{1,2}:\d{1,2})发布', str)
        if p:
            return time.strftime('%Y-%m-%d',time.localtime(time.time())) + " " + p.group(1)
        else:
            return str

    def getJobListPerPage(self, url, s):
        # s = requests.Session()

        headers = {
            'User-Agent': random.choice(ua.ua_pool),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': '1',
        }
        response = s.get(url, headers=headers)
        print(response.cookies)
        print(response.request.headers)
        selector = etree.HTML(response.text)


        position_list = selector.xpath('//*[@id="s_position_list"]/ul/li')
        '''
        position_name: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3
        address: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/span
        format_time: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/span
        money: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[2]/div/span
        requirement: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[2]/div/text()
        company_name: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[2]/div[1]/a
        industry: //*[@id="s_position_list"]/ul/li[1]/div[1]/div[2]/div[2]
        label: //*[@id="s_position_list"]/ul/li[1]/div[2]/div[1]
        strengs: //*[@id="s_position_list"]/ul/li[1]/div[2]/div[2]
        '''
        listPerPage = []
        for node in position_list:
            listPerJob = []
            position_name = node.xpath('div[1]/div[1]/div[1]/a/h3/text()')[0]
            # 唯一标识
            position_id = node.xpath('./@data-positionid')[0]
            address = node.xpath('string(div[1]/div[1]/div[1]/a/span)')
            format_time = node.xpath('div[1]/div[1]/div[1]/span/text()')[0]
            money = node.xpath('div[1]/div[1]/div[2]/div/span/text()')[0]
            requirement = node.xpath('div[1]/div[1]/div[2]/div/text()')[2].strip()
            company_name = node.xpath('div[1]/div[2]/div[1]/a/text()')[0]
            industry = node.xpath('div[1]/div[2]/div[2]/text()')[0].strip()
            label = node.xpath('div[2]/div[1]/span/text()')
            strengs = node.xpath('div[2]/div[2]/text()')[0]
            listPerJob.append(position_name)
            listPerJob.append(position_id)
            listPerJob.append(address)
            # 将"10:11发布"格式化为"2017-11-27 10:11"
            listPerJob.append(self.transtime(format_time))
            listPerJob.append(money)
            listPerJob.append(requirement)
            listPerJob.append(company_name)
            listPerJob.append(industry)
            listPerJob.append(str(label))
            listPerJob.append(strengs)
            listPerJob.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            listPerPage.append(listPerJob)



        # 找下一页的链接
        next_url = selector.xpath('//a[text()="下一页"]/@href')
        headers['Referer'] = url
        if len(next_url) != 0:
            next_url = next_url[0]
            page_num = global_var.get_value("PAGE_NUM_PROCESSING")
            print("当前第" + str(page_num) + "页爬取成功")
            yield listPerPage
            if next_url == 'javascript:;':
                global_var.set_value("isLastPage", True)
                print("最后一页了。。。。")
                return
            else:
                global_var.set_value("PAGE_NUM_PROCESSING", page_num + 1)
                print("下一页链接：" + next_url)
                # self.getJobListPerPage(next_url, s)
                # return listPerPage

                joblistgen = self.getJobListPerPage(next_url, s)
                for joblist in joblistgen:
                    yield joblist
        else:
            no_position = selector.xpath('//div[text()="暂时没有符合该搜索条件的职位"]')
            if no_position:
                logging.info("no position: " + url)
            else:
                # print(response.text)
                print("被检测出来了。。。。")
                return






