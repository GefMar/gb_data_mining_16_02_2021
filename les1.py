"""
HTTP
HEADERS
BODY

GET
POST
PUT
PATCH
DELETE
INFO

STATUS CODES

1xx
2xx
3xx
4xx
5xx
"""

import time
import json
from pathlib import Path
import requests


"""
# params = {
#     "records_per_page": 50,
#     "page": 1,
# }
#
# url = "https://5ka.ru/api/v2/special_offers/"
# headers = {
#     "Accept": "application/json",
#     "User-Agent": "Mozilla/5.0
(Macintosh; Intel Mac OS X 10.16; rv:85.0)
Gecko/20100101 Firefox/85.0",
# }
# response = requests.get(url, params=params, headers=headers)
#
# html_temp = Path(__file__).parent.joinpath("temp.html")
# json_temp = Path(__file__).parent.joinpath("temp.json")
# json_temp.write_text(response.text, encoding="UTF-8")
"""


class Parse5Ka:
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10.16; rv:85.0) "
        "Gecko/20100101 Firefox/85.0",
    }

    def __init__(self, start_url: str, products_path: Path):
        self.start_url = start_url
        self.products_path = products_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.products_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    @staticmethod
    def _save(data: dict, file_path):
        jdata = json.dumps(data, ensure_ascii=False)
        file_path.write_text(jdata, encoding="UTF-8")


class CategoriesParser(Parse5Ka):
    def __init__(self, categories_url: str, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self) -> list:
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            url = f"{self.start_url}?categories={category['parent_group_code']}"
            file_path = self.products_path.joinpath(f"{category['parent_group_code']}.json")
            category["products"].extend(list(self._parse(url)))
            # for product in self._parse(url):
            #     category["products"].append(product)
            self._save(category, file_path)


def get_dir_path(dirname: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dirname)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    product_path = get_dir_path("products")
    cat_path = get_dir_path("categories")
    cat_url = "https://5ka.ru/api/v2/categories/"
    parser = Parse5Ka(url, product_path)
    cat_parser = CategoriesParser(cat_url, url, cat_path)
    cat_parser.run()
    # parser.run()
