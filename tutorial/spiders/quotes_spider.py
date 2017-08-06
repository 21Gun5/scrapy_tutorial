# encoding=utf-8

import scrapy
from tutorial.items import TutorialItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quote_sel_list = response.xpath('//div[@class=\'quote\']')      #没有加extract函数处理，便还是selecor对象
        for quote_sel in quote_sel_list:
            item = TutorialItem()
            item['content'] = quote_sel.xpath('./span[@class=\'text\']/text()').extract_first()        #extract_first()取出第一个，化列表为元素
            item['author'] = quote_sel.xpath('.//small[@class=\'author\']/text()').extract_first()       #//表示选取所有子元素，不考虑位置
            item['tag_list'] = quote_sel.xpath('.//a[@class=\'tag\']/text()').extract()       #一个quote有多个tag，列表保存
            yield item
        '''
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()        #@href得到a标签href属性值
        if next_url is not None:
            next_url_full = response.urljoin(next_url)      #利用urljoin方法将相对路径转为绝对路径，原来：/page/2/，之后：http://quotes.toscrape.com/page/2/
            yield scrapy.Request(next_url_full, callback=self.parse)        #请求此url，回调函数为本身，即将此响应交由自身处理，达到递归效果；
        '''
        next_url_sel = response.xpath('//li[@class=\'next\']/a')      #传入的值为单个值，而非列表
        if len(next_url_sel) != 0:          #列表的元素个数为0时，表示为最后一页，没有下一页链接;
            yield response.follow(next_url_sel[0], callback=self.parse)        #参数可以仕selector类型，且url可以是相对路径；
