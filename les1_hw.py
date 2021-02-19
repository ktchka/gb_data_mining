import requests
import json
from pathlib import Path
import time


class Parse5ka:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}

    def __init__(self, start_url, save_path):
        self.start_url = start_url
        self.save_path = save_path

    def get_categories(self, url: str):
        result = list()
        categories_url = 'https://5ka.ru/api/v2/categories/'
        response = requests.get(categories_url, headers=self.headers)
        categories: dict = response.json()

        for category in categories:
            category_info = dict()
            category_info['name'] = category['parent_group_name']
            category_info['code'] = category['parent_group_code']
            result.append(category_info)

        params = {'store': '363H',
                  'records_per_page': '12',
                  'page': 1,
                  'categories': None,
                  'ordering': '',
                  'price_promo__gte': '',
                  'price_promo__lte': '',
                  'search': ''
                  }

        for category in result:
            code = int(category['code'])
            params['categories'] = code
            products = []
            tmp_url = url
            while tmp_url:
                response = self._get_response(tmp_url, params)
                if response is None:
                    break
                data: dict = response.json()
                tmp_url = data['next']
                for product in data['results']:
                    products.append(product)

            category['products'] = products
            category_path = self.save_path.joinpath(f"{category['name']}.json")
            self._save(category, category_path)

        return result

    def _get_response(self, url: str, params):
        for _ in range(3):
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_path = Path(__file__).parent.joinpath('products')
    if not save_path.exists():
        save_path.mkdir()

    parser = Parse5ka(url, save_path)
    parser.get_categories(url)
