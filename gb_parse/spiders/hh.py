import scrapy
from ..loaders import HHloader


class HHSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://kazan.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=88&customDomain=1"]

    _xpath_selectors = {
        "pagination": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
        "vacancy_urls": '//a[@data-qa="vacancy-serp__vacancy-title"]/@href'
    }

    _vacancy_xpath = {
        "title": '//h1[@data-qa="vacancy-title"]/text()',
        "salary": '//p[@class="vacancy-salary"]//text()',
        "description": '//div[@data-qa="vacancy-description"]//text()',
        "skills": '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/text()',
        "company_url": '//a[@data-qa="vacancy-company-name"]/@href'
    }

    def _get_follow_xpath(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow_xpath(response, self._xpath_selectors['pagination'],
                                          self.parse)
        yield from self._get_follow_xpath(response, self._xpath_selectors['vacancy_urls'],
                                          self.vacancy_parse)

    def vacancy_parse(self, response):
        loader = HHloader(response=response)
        loader.add_value('url', response.url)
        for key, value in self._vacancy_xpath.items():
            loader.add_xpath(key, value)
        yield loader.load_item()
