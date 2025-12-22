from collections import defaultdict
from rest_framework import status
from .filter import StoreFilterSet
from .permissions import StatusBasedPermission
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Store, Order, StoreRating, Cart, CourierRating

class RegisterGenericAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = JsonResponse({'detail': 'Successfully registered.'})

        response.set_cookie(
            key='auth_token',
            value=user.token,
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response

class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response = JsonResponse({'detail': 'Successfully logged in.'})

        response.set_cookie(
            key='auth_token',
            value=user.token,
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = JsonResponse({'detail': 'Successfully logged out.'})
        response.delete_cookie('auth_token')
        return response

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [StatusBasedPermission]
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['store_name', 'category']
    filterset_class = StoreFilterSet

    def get(self, request):
        stores = Store.objects.all()
        grouped = defaultdict(list)

        for i in stores:
            serialized = StoreSerializer(i, context={'request': request}).data
            grouped[i.category].append(serialized)

        return Response(grouped)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)  # если есть поле owner
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class StoreDetailView(RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'id'

class StoreRatingViewSet(viewsets.ModelViewSet):
    queryset = StoreRating.objects.all()
    serializer_class = StoreRatingSerializer
    permission_classes = [StatusBasedPermission]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [StatusBasedPermission]

    def get_queryset(self):
        return Order.objects.filter(id=self.request.user.id)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [StatusBasedPermission]

    def get_queryset(self):
        return Cart.objects.filter(id=self.request.user.id)

class CourierRatingViewSet(viewsets.ModelViewSet):
    queryset = CourierRating.objects.all()
    serializer_class = CourierRatingSerializer
    permission_classes = [StatusBasedPermission]