import scrapy


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ["mg.olx.com.br"]
    start_urls = (
        'https://mg.olx.com.br/belo-horizonte-e-regiao/imoveis/aluguel',
    )

    def parse(self, response):
        items = response.xpath(
            '//div[contains(@class,"section_OLXad-list")]//li[contains'
            '(@class,"item")]'
        )
        for item in items:
            url = item.xpath(
                "//a[contains(@class,'OLXad-list-link')]/@href"
            ).extract
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()
        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        self.log(u'Imóvel URL: {0}'.format(response.url))
        item = {}
        item['url'] = response.url
        item['address'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-location")]'
            '//.)'
        ).extract_first()
        item['title'] = response.xpath(
            'normalize-space(//h1[contains(@id,"ad_title")]//.)'
        ).extract_first()
        item['price'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-price")]'
            '//span[contains(@class,"actual-price")]//.)'
        ).extract_first()
        item['details'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-description")]'
            '//.)'
        ).extract_first()
        date = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-date")]//.)'
        ).re("Inserido em: (.*).")
        item['date'] = (date and date[0]) or ''
        yield item
        #teste
