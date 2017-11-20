# -*- coding=utf-8 -*-
import scrapy
import logging
import json

'''
在51job上搜索python关键词的全国大部分地区的招聘信息
'''
class Www51jobSpider(scrapy.Spider):
    name = 'www51job'
    allowed_domains = ['51job.com']
    start_urls = [
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=030200%2C040000%2C010000%2C020000%2C180200&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=200200%2C080200%2C070200%2C090200%2C060000&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=030800%2C230300%2C230200%2C070300%2C250200&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=190200%2C150200%2C080300%2C170200%2C050000&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=120300%2C120200%2C220200%2C240200%2C110200&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1'
        '&jobarea=070400%2C070500%2C070900%2C071100%2C01&keyword=python'
        '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'
    ]

    def parse(self, response):
        for item in response.xpath('//*[@id="resultList"]/div[@class="el"]'):
            yield dict(job_name=item.xpath('p/span/a/text()').extract_first().strip(),
                       company=item.xpath('span[@class="t2"]/a/text()').extract_first(),
                       location=item.xpath('span[@class="t3"]/text()').extract_first(),
                       salary=item.xpath('span[@class="t4"]/text()').extract_first(),
                       pub_date=item.xpath('span[@class="t5"]/text()').extract_first())
        next_page = response.xpath('//a[text()="下一页"]/@href')\
            .extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)