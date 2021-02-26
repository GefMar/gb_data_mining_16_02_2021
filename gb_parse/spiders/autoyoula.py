import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]
    _css_selectors = {
        "brands": "div.TransportMainFilters_brandsList__2tIkv "
        ".ColumnItemList_item__32nYI a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car": "article.SerpSnippet_snippet__3O1t2 .SerpSnippet_titleWrapper__38bZM a.blackLink",
    }

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)

    def brand_parse(self, response, *args, **kwargs):

        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)

        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)

    def car_parse(self, response):
        title = response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first()
        print(title)
