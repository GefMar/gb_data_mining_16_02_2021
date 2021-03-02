from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from gb_parse.items import GbAutoYoulaItem


def get_characteristics(item) -> dict:
    selector = Selector(text=item)
    return {
        "name": selector.xpath(
            '//div[contains(@class, "AdvertSpecs_label")]/text()'
        ).extract_first(),
        "value": selector.xpath(
            '//div[contains(@class, "AdvertSpecs_data")]//text()'
        ).extract_first(),
    }


def some(data: dict):
    data["new_key"] = "hello"
    return data


class AutoyoulaLoader(ItemLoader):
    default_item_class = GbAutoYoulaItem
    # url_out = TakeFirst()
    # title_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics, some)
