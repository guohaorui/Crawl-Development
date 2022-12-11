import scrapy
from scrapy_quote.items import ScrapyQuoteItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # def parse(self, response):
    #     divs_list = response.xpath('//div[@class="quote"]')
    #     all_data = []
    #     for div in divs_list:
    #         content = div.xpath('./span/text()').extract_first()
    #         author = div.xpath('.//small/text()').extract_first()
    #         tags = div.xpath('./div//a//text()').extract()
    #
    #         print(content)
    #         print(author)
    #         print(tags)
    #         d = {
    #             'author': author,
    #             'content': content,
    #             'tags': tags
    #         }
    #         all_data.append(d)
    #     return all_data
    def parse(self, response):
        divs_list = response.xpath('//div[@class="quote"]')
        for div in divs_list:
            content = div.xpath('./span/text()').extract_first()
            author = div.xpath('.//small/text()').extract_first()
            tags = div.xpath('./div//a//text()').extract()

            item = ScrapyQuoteItem()
            item['author'] = author
            item['content'] = content
            item['tags'] = tags

            yield item # 将item提交给管道
