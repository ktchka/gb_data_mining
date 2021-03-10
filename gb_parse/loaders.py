from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose
from .items import GbAutoYoulaItem, HHItem


def get_characteristics(item):
    selector = Selector(text=item)
    data = {
        'name': selector.xpath(
            "//div[contains(@class, 'AdvertSpecs_label')]/text()").extract_first(),
        'value': selector.xpath(
            "//div[contains(@class, 'AdvertSpecs_data')]//text()").extract_first()
    }
    return data


class AutoYoulaLoader(ItemLoader):
    default_item_class = GbAutoYoulaItem
    url_out = TakeFirst()
    title_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)


class HHloader(ItemLoader):
    default_item_class = HHItem
    url_out = TakeFirst()
    title_out = TakeFirst()
    description_out = TakeFirst()
    salary_out = TakeFirst()
