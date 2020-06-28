from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        '''
        데이터프레임을 읽어옵니다.
        '''
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        '''
        기존의 dataframe pkl파일을 읽어와서 DB에 저장합니다.
        '''

        print("[*] Loading data...")
        # dataframe pkl 파일을 읽어오는 _load_dataframes함수를 실행합니다.
        dataframes = self._load_dataframes()

        # 데이터 중 빈 값들을 0.0으로 입력해 줍니다.
        dataframes["stores"] = dataframes["stores"].fillna(0.0)
        dataframes["menues"]["price"]=dataframes["menues"]["price"].fillna(0.0).astype(int)
        
        print("[*] Delete all data...")
        # DB에 저장된 정보를 모두 지워 초기화해 줍니다.
        models.Store.objects.all().delete()
        models.CustomUser.objects.all().delete()
        models.Review.objects.all().delete()
        models.Menu.objects.all().delete()
        print("[+] Done")

        print("[*] Initializing stores...")
        # DB에 데이터를 작성합니다.

        stores = dataframes["stores"]
        # 데이터프레임에서 매장 정보를 가져옵니다.

        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                area=store.area,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category=store.category,
                # latitude와 longitude을 바탕으로 격자 값을 계산하여 location에 입력합니다.
                # 맨 왼쪽 아래가 0번이고 맨 오른쪽 위가 가장 큰 값을 가지는 형태입니다.
                location=int((store.latitude - 33.079772) / 0.0009) + (int((store.longitude -124.6)/0.0009)<<14) if store.longitude != 0.0 else 0,
                # 매장에 작성된 리뷰 갯수를 입력합니다.
                # 머신러닝에서 DB 데이터를 활용하기 위해 미리 계산해 칼럼에 입력합니다.
                review_count=dataframes["reviews"]["store"][dataframes["reviews"]["store"]==store.id].count()
            )
            for store in stores.itertuples()
        ]
        # 벌크데이터 리스트를 만들고 모델에 입력합니다.
        models.Store.objects.bulk_create(stores_bulk)
        print("[+] Done")

        print("[*] Initializing users...")
        # store와 거의 동일.
        users = dataframes["users"]
        users_bulk = [
            models.CustomUser(
                id=user.id,
                username=user.id,
                gender=user.gender,
                age=user.age,
                # 유저가 작성한 리뷰 갯수를 입력합니다.
                # 머신러닝에서 DB 데이터를 활용하기 위해 미리 계산해 칼럼에 입력합니다.
                review_count=dataframes["reviews"]["user"][dataframes["reviews"]["user"]==user.id].count()
            )
            for user in users.itertuples()
        ]
        models.CustomUser.objects.bulk_create(users_bulk)
        print("[+] Done")

        print("[*] Initializing menues...")
        menues = dataframes["menues"]
        menues_bulk = [
            models.Menu(
                id=menu.id,
                store_id=menu.store,
                menu_name=menu.menu_name,
                price=menu.price,
            )
            for menu in menues.itertuples()
        ]
        models.Menu.objects.bulk_create(menues_bulk)
        print("[+] Done")

        print("[*] Initializing reviews...")
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                store_id=review.store,
                store_name=models.Store.objects.get(id=review.store).store_name,
                user_id=review.user,
                score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for review in reviews.itertuples()
        ]
        models.Review.objects.bulk_create(reviews_bulk)
        print("[+] Done")

    def handle(self, *args, **kwargs):
        # python manage.py initialize를 실행하면 가장 먼저 들어오는 부분
        # _initialize함수를 실행한다.
        self._initialize()
