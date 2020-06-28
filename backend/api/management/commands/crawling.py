from api import models
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from api import models

class Command(BaseCommand):
    def _initialize(self):
        search_base = "https://openapi.naver.com/v1/search/webkr.xml?query=다이닝코드+"
        search_opt = "&display=10&start=1"
        base = "https://www.diningcode.com/profile.php"
        headers={
                    "X-Naver-Client-Id": "HzusvK5FvwGA_OcXs0xZ",
                    "X-Naver-Client-Secret": "o7Hh0ooCxL",
                }
        stores = models.Store.objects.all()
        for i in range(3691, len(stores)):
            store = stores[i]
            print(store.id)
            # print(store)
            # continue
            add = store.address
            store_name = store.store_name
            add = add.replace(' ', '+')
            store_name = store_name.replace(' ', '+')
            url = search_base+add+'+'+store_name+search_opt
            res = requests.get(url, headers=headers).text.split(base)
            # print(res)
            if len(res) >= 2:
                q = res[1].split("</link>")[0]
                print(q)
                soup = BeautifulSoup(requests.get(base+q).text, 'html.parser')
                a = soup.select('.btn-gallery-open > img')
                print(a)
                if a:
                    img = ''
                    img = a[0].attrs['src']
                    print(img)
                    models.StoreImage.objects.create(store=store, url=img)
        # print(models.CustomUser.objects.all())
        
        # res = requests.get("https://openapi.naver.com/v1/search/webkr.xml?query=다이닝코드+서울특별시+용산구+이태원동+118-9+Battered+Sole&display=10&start=1", headers=headers).text.split(base)
        
        
        # if len(res) >2:
        #     res = res[2].split("</link>")
        #     print(requests.get(res[0]).text)

        # soup = BeautifulSoup(requests.get("https://openapi.naver.com/v1/search/webkr.xml?query=다이닝코드+서울특별시+용산구+이태원동+118-9+Battered+Sole&display=10&start=1", headers=headers).text, 'html.parser')
        # a = soup.select('title > link')
        # print(a)
    def handle(self, *args, **kwargs):
        self._initialize()
