from django.shortcuts import render, get_object_or_404, redirect
from api import models, serializers
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser, Store, UserLikeStore
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime
from rest_auth.views import LoginView

def go_to_myhome(request):
    return redirect("http://localhost:8080/")

class CustomLoginView(LoginView):
    def get_response(self):
        user = get_object_or_404(CustomUser, username=self.user)
        # print(self.user)
        orginal_response = super().get_response()
        mydata = {"gender": user.gender, "age": user.age, "review_count": user.review_count, "status": "success"}
        orginal_response.data["user"].update(mydata)
        return orginal_response


# from IPython import embed

# 메서드 정리
# class UserViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """

#     def list(self, request):
#         pass
#     def create(self, request):
#         pass
#     def retrieve(self, request, pk=None):
#         pass
#     def update(self, request, pk=None):
#         pass
#     def partial_update(self, request, pk=None):
#         pass
#     def destroy(self, request, pk=None):
#         pass


# @api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
# def stores(request):
#     print(request.META.get('HTTP_AUTHORIZATION'))
#     print(request.user.is_authenticated)
#     stores = models.Store.objects.all().order_by('id')[:5]
#     store_list = serializers.StoreSerializer(stores, many=True)
#     return Response(data = store_list.data)


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination
    
    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset


class UserReviewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        content = self.request.query_params.get("content", "")
        store_name = self.request.query_params.get("store_name", "")
        # 매장명, 
        if user:
            # print(dir(models.Review.objects.filter(user_id=user).filter(content__contains=content)))
            # print(models.Review.objects.filter(user_id=user).filter(content__contains=content))
            User = models.CustomUser.objects.get(id=user)
            reviews = models.Review.objects.filter(user_id=user)
            if content:
                if store_name:
                    queryset = (
                        reviews.filter(content__contains=content)|User.review_set.filter(store_name__contains=store_name)
                    )
                else:
                    queryset = (
                        reviews.filter(content__contains=content)
                    )
            elif store_name:
                queryset = (
                    User.review_set.filter(store_name__contains=store_name)
                )
            else:
                queryset = (
                    reviews
                )
        else:
            queryset = (
                models.Review.objects.filter(content__contains=content).filter(store_name__contains=store_name)
            )            
        return queryset


class StoreReviewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        queryset = (
            models.Review.objects.all()
        )
        return queryset

    def create(self, request):
        # 리뷰를 작성하는 함수입니다.
        # if request.user.is_authenticated:
        #     data = request.data
        #     review = models.Review.objects.create(store_id=data["store"], user_id=request.user.id, content=data["content"], score=data["score"], reg_time=datetime.datetime.now())
        #     return Response("작성 성공")
        # else:
        #     return Response("작성 실패")
        data = request.data
        store = Store.objects.get(id=data["store"])
        store_name = store.store_name
        user = CustomUser.objects.get(id=data["user"])

        # 받아온 데이터를 이용해서 Review를 작성합니다.
        models.Review.objects.create(store_id=data["store"], user_id=data["user"], content=data["content"], score=data["score"], reg_time=datetime.datetime.now(), store_name=store_name)
        
        # 작성이 완료되었다면 매장과 유저의 review_count를 1씩 추가합니다.
        store.review_count += 1
        store.save()
        user.review_count += 1
        user.save()
        return Response("작성 성공")

    def update(self, request, pk=None):
        '''
        받아온 데이터에서 평점과 내용을 가져와 리뷰 객체를 수정합니다.
        '''
        review = models.Review.objects.get(id=pk)
        if request.data.get("score"):
            review.score = request.data["score"]
        if request.data.get("content"):
            review.content = request.data["content"]
        review.save()
        return Response("수정 성공")

    def destroy(self, request, pk=None):
        '''
        받아온 pk에 해당하는 리뷰를 삭제합니다.
        '''
        review = models.Review.objects.get(id=pk)
        user = models.CustomUser.objects.get(id=review.user_id)
        store = models.Store.objects.get(id=review.store_id)
        review.delete()
        user.review_count -= 1
        store.review_count -= 1

        return Response("삭제 성공")


@api_view(['GET'])
def store_reviews(self, store_id):
    serializer = serializers.ReviewSerializer(models.Review.objects.filter(store_id=store_id), many=True)
    return Response(serializer.data)



@api_view(['POST'])
def search_store(self):
    '''
    입력 데이터
    {
        "latitude": float,
        "longitude": float,
        "words": "string" 
    }
    '''
    # 위치 정보가 없으면 오류 반환
    if not self.data.get("longitude") or not self.data.get("latitude"):
        return Response("위치 정보가 없습니다.")
    
    # 입력받은 위치 정보를 격자 번호로 변환합니다.
    location_x = int((self.data["longitude"] -124.6)/0.0009)
    location_y = int((self.data["latitude"] - 33.079772) / 0.0009)
    
    # 현 위치와 인근 격자 번호를 계산합니다.
    location = location_y + (location_x<<14)
    location2 = location_y + ((location_x+1)<<14)
    location3 = location_y + ((location_x+2)<<14)
    location4 = location_y + ((location_x-1)<<14)
    location5 = location_y + ((location_x-2)<<14)

    location6 = location_y+1 + ((location_x-1)<<14)
    location7 = location_y+1 + ((location_x)<<14)
    location8 = location_y+1 + ((location_x+1)<<14)

    location9 = location_y+2 + ((location_x)<<14)

    location10 = location_y-1 + ((location_x-1)<<14)
    location11 = location_y-1 + ((location_x)<<14)
    location12 = location_y-1 + ((location_x+1)<<14)

    location13 = location_y-2 + ((location_x)<<14)

    # 인근에 존재하는 매장들을 모두 가져옵니다.
    queryset = Store.objects.filter(
        Q(location = location)
        |Q(location = location2)
        |Q(location = location3)
        |Q(location = location4)
        |Q(location = location5)
        |Q(location = location6)
        |Q(location = location7)
        |Q(location = location8)
        |Q(location = location9)
        |Q(location = location10)
        |Q(location = location11)
        |Q(location = location12)
        |Q(location = location13)
        )

    words = []
    # 검색어를 입력받아 띄워쓰기별로 나눠줍니다.
    if self.data.get("words"):
        words = self.data["words"].split()
    
    a = []
    if words:
        # 검색어가 존재할 경우 매장목록에 대해서 반복문을 돌면서
        # 검색 단어가 포함된 매장명이나 검색 단어가 포함된 메뉴가 있을 경우
        # a라는 리스트에 해당 매장을 추가합니다.
        for store in queryset:
            # print(store.location)
            chk = 0
            for word in words:
                if store.store_name in word:
                    chk = 1
                    break
            if chk:
                a.append(store)
                continue
            for menu in store.menu_set.all():
                for word in words:
                    if word in menu.menu_name:
                        chk = 1
                        break
                if chk:
                    break
            if chk:
                a.append(store)
        # 검색어에 해당하는 매장이 담긴 a 리스트를 직렬화합니다.
        serializer = serializers.StoreSerializer(a, many=True)
    else:
        serializer = serializers.StoreSerializer(queryset, many=True)
    # 데이터를 반환합니다.
    return Response(serializer.data)


class StoreDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreDetailSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    
    @api_view(['GET'])
    def get_queryset(self):
        serializer = serializers.UserSerializer(models.CustomUser.objects.filter(review_count__gte=10), many=True)
        # print(serializer.data)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def user_delete(self):
        if self.user.is_authenticated == False:
            return Response("삭제 실패")
        else:
            user = get_object_or_404(CustomUser, username=self.user)
            user.is_active = False
            user.save()
            return Response("삭제 성공")


class StoreViewSet2(viewsets.GenericViewSet):
    serializer_class = serializers.StoreSerializer2

    @api_view(['GET'])
    def get_queryset(self, review_count):
        # review_count = self.request.query_params.get("review_count", "")
        serializer = serializers.StoreSerializer2(models.Store.objects.filter(review_count__gte=review_count), many=True)
        return Response(serializer.data)


class like_store(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LikeUserSerializer
    @api_view(['POST'])
    def get_queryset(self, user_id, store_id):        
        a = get_object_or_404(get_user_model(), pk=user_id)
        b = get_object_or_404(Store, id=store_id)
        if a.like_stores.filter(id=store_id):
            a.like_stores.remove(b)
            return Response("좋아요 취소")
        else:
            a.like_stores.add(b)
            return Response("좋아요")

    def create(self, request):
        # UserLikeStore.objects.create(customuser_id=request.user.id, store_id=request.data["store_id"])
        # like = UserLikeStore.objects.filter(customuser_id = 68632, store_id = 15)
        # like[0].delete()
        if request.user.is_authenticated:
            like = UserLikeStore.objects.filter(customuser_id = request.user.id, store_id = request.data["store_id"])
            if like:
                like[0].delete()
                return Response("좋아요 취소")
            else:
                UserLikeStore.objects.create(customuser_id=request.user.id, store_id=request.data["store_id"])
                return Response("좋아요 등록")
        else:
            return Response("비 인증 유저")

@api_view(['GET'])
def review_list(self):
    serializer = serializers.ReviewSerializer2(models.Review.objects.all(), many=True)
    # print(serializer.data)
    return Response(serializer.data)