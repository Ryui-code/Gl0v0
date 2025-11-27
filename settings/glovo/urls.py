from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'store', StoreViewSet, basename='store')
router.register(r'store-rating', StoreRatingViewSet, basename='store_rating')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'courier-rating', CourierRatingViewSet, basename='courier_rating')

urlpatterns = [
    path('register/', RegisterGenericAPIView.as_view(), name='register'),
    path('login/', LoginGenericAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('stores/<int:id>/', StoreDetailView.as_view(), name='store-id'),
    path('', include(router.urls))
]