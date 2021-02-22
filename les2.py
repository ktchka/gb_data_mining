import requests
from pathlib import Path
import bs4
from urllib.parse import urljoin
import pymongo
import datetime as dt


class MagnitParse:
    months = {"янв": 1,
              "фев": 2,
              "мар": 3,
              "апр": 4,
              "май": 5,
              "мая": 5,
              "июн": 6,
              "июл": 7,
              "авг": 8,
              "сен": 9,
              "окт": 10,
              "ноя": 11,
              "дек": 12,
              }

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client['data_mining_15_02_2021']
        self.collection = self.db['magnit_products']

    def _get_response(self, url):
        # TODO: написать обработку ошибки
        return requests.get(url)

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': "сatalogue__main"})
        for prod_a in catalog.find_all('a', recursive=False):
            product_data = self._parse(prod_a)
            self._save(product_data)

    def _get_template(self):
        return {
            'url': lambda a: urljoin(self.start_url, a.attrs.get('href', '')),
            'product_name': lambda a: a.find('div', attrs={'class': "card-sale__title"}).text,
            'promo_name': lambda a: a.find('div', attrs={'class': "card-sale__name"}).text,
            "old_price": lambda a: float(".".join(
                i for i in a.find("div", attrs={"class": "label__price_old"}).text.split()
            )),
            "new_price": lambda a: float(".".join(
                i for i in a.find('div', attrs={"class": "label__price_new"}).text.split()
            )),
            "image_url": lambda a: urljoin(self.start_url, a.find("img").attrs.get("data-src")),
            "date_from": lambda a: self.__get_time(
                a.find('div', attrs={'class': "card-sale__date"}).text
            )[0],
            "date_to": lambda a: self.__get_time(
                a.find('div', attrs={"class": "card-sale__date"}).text
            )[1]
        }

    def __get_time(self, string):
        dates = string.replace('с ', '', 1).replace('\n', '').split('до')
        result = []
        for date in dates:
            temporary = date.split()
            result.append((
                dt.datetime(
                    year=dt.datetime.now().year,
                    day=int(temporary[0]),
                    month=self.months[temporary[1][:3]]
                )
            ))
        return result

    def _parse(self, product_a):
        data = {}
        for key, func in self._get_template().items():
            try:
                data[key] = func(product_a)
            except (AttributeError, ValueError):
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)


def get_save_path(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == '__main__':
    url = "https://magnit.ru/promo/"
    save_path = get_save_path('magnit_product')
    db_client = pymongo.MongoClient('mongodb://localhost:27017')
    parser = MagnitParse(url, db_client)
    parser.run()
