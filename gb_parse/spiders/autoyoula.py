
import scrapy
from ..loaders import AutoYoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    _xpath_selectors = {
        "brands": '//div[@class="TransportMainFilters_brandsList__2tIkv"]//a[@class="blackLink"]/@href',
        "pagination": '//div[contains(@class, "Paginator_block")]//a/@href',
        "car": '//article[contains(@class, "SerpSnippet_snippet")]//a[contains(@class, "SerpSnippet_name")]/@href',
    }

    _car_xpath = {
        "title": '//div[@data-target="advert-title"]/text()',
        "photos": '//figure[contains(@class, "PhotoGallery_photo")]//img/@src',
        "characteristics": '//div[contains(@class, "AdvertCard_specs")]/div/div[contains(@class, "AdvertSpecs_row")]'

    }

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def _get_follow_xpath(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow_xpath(response, self._xpath_selectors['brands'],
                                          self.brand_parse)

    def brand_parse(self, response, **kwargs):
        yield from self._get_follow(
            response, self._xpath_selectors["pagination"], self.brand_parse,
        )
        yield from self._get_follow(response, self._xpath_selectors["car"], self.car_parse)

    def car_parse(self, response):
        loader = AutoYoulaLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self._car_xpath.items():
            loader.add_xpath(key, value)
        yield loader.load_item()
