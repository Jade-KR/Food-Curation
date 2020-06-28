from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        #필수인자
        title="Restaurant API",
        default_version="v1",
        #선택인자
        description="식당관련 API 서비스입니다.",
        # terms_of_service='https://www.google.com/policies/terms/', # 약관 예시
        contact=openapi.Contact(email="pyeonggangkim@gmail.com"),
        license=openapi.License(name="SSAFY License"), 
    )
)



router = DefaultRouter(trailing_slash=False)
router.register(r"stores", views.StoreViewSet, basename="stores")
# router.register(r"reviews/<int:user_id>", views.UserReviewSet, basename="user-review")
router.register(r"stores_detail", views.StoreDetailViewSet, basename="stores-detail")
# router.register(r"user", views.UserViewSet, basename="user")
router.register(r"user_reviews", views.UserReviewSet, basename="user-review")


router.register(r"store_reviews", views.StoreReviewSet, basename="store-review")
router.register(r"like_store", views.like_store, basename="like-store")
# router.register(r"reviews", views.ReveiwViewSet, basename="reviews")
urlpatterns = [
    # path('stores/', views.stores, name='stores'),
    path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
    path('user', views.UserViewSet.get_queryset, name='user'),
    path('store/<int:review_count>', views.StoreViewSet2.get_queryset, name='store'),
    path('user_delete/', views.UserViewSet.user_delete, name='user_delete'),
    # path('user_reviews/<int:user_id>', views.UserReviewSet.get_queryset, name='user-review'),
    path('get_store_reviews_by_store_id/<int:store_id>', views.store_reviews, name='get-store-review'),
    # path('like_store/<int:user_id>/<int:store_id>', views.like_store.get_queryset, name='like_store'),
    *router.urls,
    path('reviews', views.review_list, name="reviews"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('search_store', views.search_store, name="search_store"),
    path('go_to_myhome/', views.go_to_myhome, name="go_to_myhome"),
]